import asyncio

import aiohttp.web

import logging
log = logging.getLogger("aio.http")


@asyncio.coroutine
def protocol(name):
    loop = asyncio.get_event_loop()
    http_app = aiohttp.web.Application(loop=loop)
    http_app['name'] = name
    return http_app.make_handler()


@asyncio.coroutine
def factory(name, proto, address, port):
    loop = asyncio.get_event_loop()
    protocol_factory = proto or protocol
    srv = yield from loop.create_server(
        (yield from protocol_factory(name)), address, port)
    log.debug(
        "Server(%s) started at http://%s:%s" % (
            name, address or '*', port))
    return srv


def redirect(path, permanent=False):
    return aiohttp.web.HTTPFound(path)
