import json
import sqlite3
import threading
import time
import uuid
from .security import Fault, digest


def uid():
    return uuid.uuid4().hex


class Store:
    def __init__(self, path, sanitizer):
        self.lock = threading.RLock()
        self.clean = sanitizer
        self.db = sqlite3.connect(path, check_same_thread=False)
        self.db.row_factory = sqlite3.Row
        self.db.executescript('''
          PRAGMA journal_mode=WAL;
          CREATE TABLE IF NOT EXISTS runs(id TEXT PRIMARY KEY, body TEXT NOT NULL);
          CREATE TABLE IF NOT EXISTS approvals(id TEXT PRIMARY KEY, body TEXT NOT NULL);
          CREATE TABLE IF NOT EXISTS events(seq INTEGER PRIMARY KEY AUTOINCREMENT, run_id TEXT, body TEXT NOT NULL, hash TEXT NOT NULL);
          CREATE TRIGGER IF NOT EXISTS immutable_events_update BEFORE UPDATE ON events BEGIN SELECT RAISE(ABORT, 'immutable audit'); END;
          CREATE TRIGGER IF NOT EXISTS immutable_events_delete BEFORE DELETE ON events BEGIN SELECT RAISE(ABORT, 'immutable audit'); END;
        ''')
        # Never automatically resume ambiguous remote actions after a crash.
        for r in self.list('runs'):
            if r['state'] in ('collecting_context', 'planning', 'executing', 'verifying'):
                r.update(state='partial', error='Service restarted during work. Inspect external effects before retrying.')
                self.put('runs', r)
                self.event(r['id'], 'run_interrupted', r['error'])

    def put(self, table, obj):
        assert table in ('runs', 'approvals')
        with self.lock, self.db:
            self.db.execute(f'INSERT OR REPLACE INTO {table} VALUES (?,?)', (obj['id'], json.dumps(self.clean(obj))))

    def get(self, table, id):
        assert table in ('runs', 'approvals')
        with self.lock:
            row = self.db.execute(f'SELECT body FROM {table} WHERE id=?', (id,)).fetchone()
        if not row:
            raise Fault('NOT_FOUND', 'Record not found.', 404)
        return json.loads(row[0])

    def list(self, table):
        assert table in ('runs', 'approvals')
        with self.lock:
            return [json.loads(r[0]) for r in self.db.execute(f'SELECT body FROM {table} ORDER BY rowid DESC')]

    def event(self, run_id, kind, message, **details):
        with self.lock, self.db:
            prev = self.db.execute('SELECT hash FROM events ORDER BY seq DESC LIMIT 1').fetchone()
            event = self.clean(dict(event_id=uid(), run_id=run_id, request_id=uid(), timestamp=time.time(), actor='local-operator', type=kind, message=message, schema_version=1, previous_hash=prev[0] if prev else '', **details))
            h = digest(event)
            self.db.execute('INSERT INTO events(run_id,body,hash) VALUES (?,?,?)', (run_id, json.dumps(event), h))
            return event

    def events(self, run_id):
        with self.lock:
            return [dict(json.loads(r[0]), hash=r[1]) for r in self.db.execute('SELECT body,hash FROM events WHERE run_id=? ORDER BY seq', (run_id,))]

    def audit_valid(self):
        with self.lock:
            rows = self.db.execute('SELECT body,hash FROM events ORDER BY seq').fetchall()
        previous = ''
        for row in rows:
            obj = json.loads(row[0])
            if obj['previous_hash'] != previous or digest(obj) != row[1]:
                return False
            previous = row[1]
        return True

