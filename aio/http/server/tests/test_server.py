import asyncio

import aiohttp

from aio.testing import aiofuturetest
from aio.app.testing import AioAppTestCase
import aio.app
from aio.app.runner import runner

HTTP_CONFIG = """
[server/test]
factory = aio.http.server.factory
port = 7070
"""

HTTP_PROTOCOL_CONFIG = """
[server/test]
factory = aio.http.server.factory
protocol = aio.http.server.tests.test_server.test_protocol_factory
address = 0.0.0.0
port = 7070
"""


@asyncio.coroutine
def test_protocol_factory(name):
    loop = asyncio.get_event_loop()
    webapp = aiohttp.web.Application(loop=loop)
    webapp['name'] = name

    @asyncio.coroutine
    def handle_hello_world(webapp):
        return aiohttp.web.Response(body=b"Hello, world")

    webapp.router.add_route("GET", "/", handle_hello_world)
    return webapp.make_handler()


class HttpServerTestCase(AioAppTestCase):

    @aiofuturetest(sleep=2)
    def test_http_server(self):

        yield from runner(
            ['run'], config_string=HTTP_CONFIG)

        @asyncio.coroutine
        def _test():
            self.assertTrue(
                "test" in aio.app.servers)
            response = yield from aiohttp.request(
                'GET', "http://localhost:7070")
            self.assertEqual(
                response.status, 404)
            body = yield from response.read()

            self.assertEqual(
                body, b"404: Not Found")

        return _test

    @aiofuturetest(sleep=2)
    def test_http_server_protocol(self):

        yield from runner(
            ['run'],
            config_string=HTTP_PROTOCOL_CONFIG)

        @asyncio.coroutine
        def _test_cb():
            self.assertTrue(
                "test" in aio.app.servers)
            response = yield from aiohttp.request(
                'GET', "http://localhost:7070")
            self.assertEqual(
                response.status, 200)
            body = yield from response.read()

            self.assertEqual(
                body, b"Hello, world")

        return _test_cb
