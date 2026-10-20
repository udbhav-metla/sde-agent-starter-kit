"""Provider contracts use test doubles; these do not claim live account access."""
import json
from types import SimpleNamespace
import httpx
import pytest
from sde_agent.config import Settings
from sde_agent.providers import GitHub, bedrock_plan, DEMO_FILES
from sde_agent.security import Fault
from sde_agent.sandbox import run_checks


def test_github_write_requires_explicit_scope():
    provider=GitHub(Settings(repositories=('owner/repo',), github_token='test-token', github_write=False))
    try:
        with pytest.raises(Fault, match='not enabled'):
            provider.publish('owner/repo', {})
    finally:
        provider.client.close()


def test_github_publish_exact_parameters():
    settings=Settings(repositories=('owner/repo',),github_token='scoped-test-token',github_write=True)
    provider=GitHub(settings)
    calls=[]
    def respond(request):
        body=json.loads(request.content) if request.content else None
        calls.append((request.method,request.url.path,body))
        if request.url.path.endswith('/git/commits/base-sha'):
            data={'tree':{'sha':'base-tree'}}
        elif request.url.path.endswith('/git/trees'):
            data={'sha':'new-tree'}
        elif request.url.path.endswith('/git/commits'):
            data={'sha':'new-commit'}
        elif request.url.path.endswith('/git/refs'):
            data={'ref':'refs/heads/sde/fix-123'}
        else:
            data={'number':7,'html_url':'https://github.com/owner/repo/pull/7','draft':True}
        return httpx.Response(200,json=data)
    provider.client.close()
    provider.client=httpx.Client(base_url='https://api.github.com',transport=httpx.MockTransport(respond))
    try:
        result=provider.publish('owner/repo',dict(base_commit='base-sha',base_branch='main',branch='sde/fix-123',title='Fix edge case',body='Reviewed evidence',changes=[{'path':'handler.py','before':'a','after':'b'}]))
        assert result['draft']
        assert calls[1][2]['tree'][0]['content']=='b'
        assert calls[2][2]['parents']==['base-sha']
        assert calls[3][2]=={'ref':'refs/heads/sde/fix-123','sha':'new-commit'}
        assert calls[4][2]=={'title':'Fix edge case','body':'Reviewed evidence','head':'sde/fix-123','base':'main','draft':True}
        assert len(calls)==5
    finally:
        provider.client.close()


def test_github_unavailable_is_not_empty_context():
    provider=GitHub(Settings(repositories=('owner/repo',),github_token=''))
    provider.client.close()
    provider.client=httpx.Client(base_url='https://api.github.com',transport=httpx.MockTransport(lambda r:httpx.Response(404,json={'message':'Not Found'})))
    try:
        with pytest.raises(Fault,match='HTTP 404'):
            provider.context('owner/repo','https://github.com/owner/repo/issues/1')
    finally:
        provider.client.close()


def test_github_issue_repository_mismatch():
    provider=GitHub(Settings(repositories=('owner/repo',)))
    try:
        with pytest.raises(Fault,match='matching'):
            provider.context('owner/repo','https://github.com/attacker/other/issues/1')
    finally:
        provider.client.close()


def test_bedrock_missing_configuration():
    with pytest.raises(Fault,match='Configure BEDROCK_MODEL_ID'):
        bedrock_plan(Settings(model_id=''),{},'')


def test_bedrock_converse_contract(monkeypatch):
    captured={}
    def converse(**kwargs):
        captured.update(kwargs)
        return {'output':{'message':{'content':[{'text':json.dumps({'summary':'Small fix','changes':[]})}]}},'ResponseMetadata':{'RequestId':'test-aws-request-id'},'usage':{'inputTokens':20,'outputTokens':12}}
    monkeypatch.setattr('boto3.client',lambda *a,**k:SimpleNamespace(converse=converse))
    result,evidence=bedrock_plan(Settings(model_id='test-model',region='us-east-1'),{'files':DEMO_FILES},'preserve API')
    assert captured['modelId']=='test-model'
    assert captured['inferenceConfig']['maxTokens']==4096
    assert 'UNTRUSTED DATA' in captured['system'][0]['text']
    assert evidence['request_id']=='test-aws-request-id'
    assert evidence['service']=='Amazon Bedrock Converse'
    assert result['summary']=='Small fix'


def test_no_tests_is_not_verification(tmp_path):
    result=run_checks(Settings(data_dir=tmp_path),{'handler.py':'def identity(x):\n    return x\n'},trusted_fixture=True)
    assert result['exit_code'] in (0, 5)  # unittest versions differ for empty discovery.
    assert result['tests']==0 and not result['passed']


def test_timeout_terminates_executor(tmp_path):
    settings=Settings(data_dir=tmp_path,test_timeout=1)
    result=run_checks(settings,{'test_slow.py':'import time\nimport unittest\nclass Slow(unittest.TestCase):\n    def test_wait(self):\n        time.sleep(30)\n'},trusted_fixture=True)
    assert result['error']=='TIMEOUT'
    assert not result['passed'] and result['duration_seconds']<5
