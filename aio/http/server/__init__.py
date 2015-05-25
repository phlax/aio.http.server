import asyncio
import inspect

import aiohttp.web
import aio.app

import logging
log = logging.getLogger("aio.http")


@aio.app.server.protocol
def protocol(name):
    loop = asyncio.get_event_loop()
    http_app = aiohttp.web.Application(loop=loop)
    http_app['name'] = name
    return http_app.make_handler()


@aio.app.server.factory
def factory(name, proto, address, port):
    loop = asyncio.get_event_loop()
    _protocol = proto or protocol

    if inspect.isclass(_protocol) and issubclass(_protocol, asyncio.Protocol):
        pass
    else:
        _protocol = yield from _protocol(name)

    srv = yield from loop.create_server(_protocol, address, port)
    log.debug(
        "Server(%s) started at http://%s:%s" % (
            name, address or '*', port))
    return srv


def redirect(path, permanent=False):
    return aiohttp.web.HTTPFound(path)
