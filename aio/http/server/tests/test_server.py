import asyncio

import aiohttp

import aio.testing
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
protocol = aio.http.server.tests.test_server.test_protocol
address = 0.0.0.0
port = 7070
"""


@aio.app.server.protocol
def test_protocol(name):
    loop = asyncio.get_event_loop()
    webapp = aiohttp.web.Application(loop=loop)
    webapp['name'] = name

    @asyncio.coroutine
    def handle_hello_world(webapp):
        return aiohttp.web.Response(body=b"Hello, world")

    webapp.router.add_route("GET", "/", handle_hello_world)
    return webapp.make_handler()


class HttpServerTestCase(AioAppTestCase):

    @aio.testing.run_forever(sleep=2)
    def test_http_server(self):

        yield from runner(
            ['run'], config_string=HTTP_CONFIG)

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

    @aio.testing.run_forever(sleep=2)
    def test_http_server_protocol(self):

        yield from runner(
            ['run'],
            config_string=HTTP_PROTOCOL_CONFIG)

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
