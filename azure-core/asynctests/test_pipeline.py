#--------------------------------------------------------------------------
#
# Copyright (c) Microsoft Corporation. All rights reserved.
#
# The MIT License (MIT)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the ""Software""), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED *AS IS*, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
#--------------------------------------------------------------------------
import sys

from azure.core.pipeline.transport import (
    _TransportRequest,
)

# TODO: copy these?
# from msrest.universal_http.async_requests import (
#     AsyncRequestsHTTPSender,
#     AsyncTrioRequestsHTTPSender,
# )
# from msrest.pipeline.async_requests import AsyncPipelineRequestsHTTPSender

from azure.core.pipeline.async_abc import AsyncPipeline
from azure.core.pipeline.transport.async_abc import (
    AsyncHTTPSender,
    SansIOHTTPPolicy
)

from azure.core.configuration import Configuration
from azure.core.pipeline.aiohttp import AioHTTPSender
from azure.core.pipeline.policies.universal import UserAgentPolicy

import trio

import pytest


@pytest.mark.asyncio
async def test_sans_io_exception():
    class BrokenSender(AsyncHTTPSender):
        async def send(self, request, **config):
            raise ValueError("Broken")

        async def __aexit__(self, exc_type, exc_value, traceback):
            """Raise any exception triggered within the runtime context."""
            return None

    pipeline = AsyncPipeline([SansIOHTTPPolicy()], BrokenSender())

    req = _TransportRequest('GET', '/')
    with pytest.raises(ValueError):
        await pipeline.run(req)

    class SwapExec(SansIOHTTPPolicy):
        def on_exception(self, requests, **kwargs):
            exc_type, exc_value, exc_traceback = sys.exc_info()
            raise NotImplementedError(exc_value)

    pipeline = AsyncPipeline([SwapExec()], BrokenSender())
    with pytest.raises(NotImplementedError):
        await pipeline.run(req)


@pytest.mark.asyncio
async def test_basic_aiohttp():

    request = _TransportRequest("GET", "http://bing.com")
    policies = [
        UserAgentPolicy("myusergant")
    ]
    async with AsyncPipeline(policies) as pipeline:
        response = await pipeline.run(request)

    assert pipeline._sender.driver._session.closed
    assert response.http_response.status_code == 200

@pytest.mark.skip("TODO: need AsyncPipelineRequestsHTTPSender")
@pytest.mark.asyncio
async def test_basic_async_requests():

    request = _TransportRequest("GET", "http://bing.com")
    policies = [
        UserAgentPolicy("myusergant")
    ]
    async with AsyncPipeline(policies, AsyncPipelineRequestsHTTPSender()) as pipeline:
        response = await pipeline.run(request)

    assert response.http_response.status_code == 200

@pytest.mark.skip("TODO: need AsyncPipelineRequestsHTTPSender and AsyncRequestsHTTPSender")
@pytest.mark.asyncio
async def test_conf_async_requests():

    conf = Configuration("http://bing.com/")
    request = _TransportRequest("GET", "http://bing.com/")
    policies = [
        UserAgentPolicy("myusergant")
    ]
    async with AsyncPipeline(policies, AsyncPipelineRequestsHTTPSender(AsyncRequestsHTTPSender(conf))) as pipeline:
        response = await pipeline.run(request)

    assert response.http_response.status_code == 200

@pytest.mark.skip("TODO: need AsyncPipelineRequestsHTTPSender and AsyncTrioRequestsHTTPSender")
def test_conf_async_trio_requests():

    async def do():
        conf = Configuration("http://bing.com/")
        request = _TransportRequest("GET", "http://bing.com/")
        policies = [
            UserAgentPolicy("myusergant")
        ]
        async with AsyncPipeline(policies, AsyncPipelineRequestsHTTPSender(AsyncTrioRequestsHTTPSender(conf))) as pipeline:
            return await pipeline.run(request)

    response = trio.run(do)
    assert response.http_response.status_code == 200