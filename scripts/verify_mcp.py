"""Actual SDK-client interoperability check. Requires a running local service."""
import asyncio
import json
import os
import httpx
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client


async def verify():
    base = os.getenv('SDE_BASE_URL', 'http://127.0.0.1:8000')
    token = os.environ['SDE_API_TOKEN']
    async with httpx.AsyncClient(headers={'Authorization': 'Bearer ' + token}, timeout=30) as client:
        response = await client.post(base + '/api/runs', json={'repository':'demo/empty-input','issue_url':'demo://empty-input/184','mode':'plan_only'})
        response.raise_for_status()
        id = response.json()['data']['id']
        for _ in range(100):
            run = (await client.get(base + '/api/runs/' + id)).json()['data']
            if run['state'] == 'completed':
                break
            await asyncio.sleep(.05)
        else:
            raise AssertionError('Plan did not complete')
        results = []
        for _ in range(2):
            async with streamable_http_client(base + '/mcp/', http_client=client) as (read, write, _):
                async with ClientSession(read, write) as session:
                    initialized = await session.initialize()
                    tools = await session.list_tools()
                    assert len(tools.tools) == 7
                    issue = await session.call_tool('get_issue', {'run_id': id})
                    assert not issue.isError
                    assert 'Empty input' in str(issue)
                    source = await session.call_tool('search_repository', {'run_id': id, 'query': 'items[0]'})
                    assert not source.isError and 'handler.py' in str(source)
                    rejected = await session.call_tool('read_file', {'run_id': id, 'path': '../.env'})
                    assert rejected.isError
                    results.append({'protocol':initialized.protocolVersion,'tools':len(tools.tools),'get_issue':'passed','provenance_search':'passed','path_escape':'rejected'})
        print(json.dumps({'status':'passed','transport':'Streamable HTTP, JSON responses, stateless','sdk':'mcp 1.30.0','connect_and_reconnect':results}, indent=2))


if __name__ == '__main__':
    asyncio.run(verify())
