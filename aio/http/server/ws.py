import json
import asyncio

import aiohttp

from aio.app import signals

import logging
log = logging.getLogger("aio.ws.request")


@asyncio.coroutine
def schedule_sockets_ping():
    yield from signals.emit("sockets-ping", None)


@asyncio.coroutine
def handle_ws(request):
    resp = aiohttp.web.WebSocketResponse()
    resp.start(request)
    while True:
        msg = yield from resp.receive()
        log.debug(msg)
        if msg.tp == aiohttp.MsgType.text:
            if msg.data == "HELO":
                log.info('adding socket: %s' % resp)
                request.app['sockets'].append(resp)
            else:
                # print ("got message %s" % msg.data)
                data = json.loads(msg.data)
                command = data[0]
                args = data[1:]
                yield from signals.emit('socket-%s' % command, args)
                # print ("handled message %s" % (msg.data))
        else:
            break
    log.info('removing socket: %s' % resp)
    request.app['sockets'].remove(resp)
    return resp
