import asyncio
from unittest.mock import AsyncMock
import pytest

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import account_nuker

class DummyResponse:
    def __init__(self, status, data=None):
        self.status = status
        self._data = data or {}

    async def json(self):
        return self._data

class DummyRequest:
    def __init__(self, response):
        self._response = response

    async def __aenter__(self):
        return self._response

    async def __aexit__(self, exc_type, exc, tb):
        pass

class DummySession:
    def __init__(self):
        self.delete_calls = 0

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        pass

    def get(self, url, headers=None):
        return DummyRequest(DummyResponse(200, [{"id": "1"}]))

    def delete(self, url, headers=None):
        self.delete_calls += 1
        if self.delete_calls == 1:
            return DummyRequest(DummyResponse(420, {"retry_after": 0}))
        return DummyRequest(DummyResponse(204))

@pytest.mark.asyncio
async def test_close_all_dms_handles_rate_limit(mocker):
    session = DummySession()
    mocker.patch('aiohttp.ClientSession', return_value=session)
    mocker.patch('asyncio.sleep', AsyncMock())
    mocker.patch('account_nuker.tqdm', lambda it, **k: it)

    await account_nuker.close_all_dms("token")
    assert session.delete_calls >= 2

