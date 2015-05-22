import logging
import asyncio


@asyncio.coroutine
def sockets_emitted(signal, msg):
    level, msg = msg
    log = logging.getLogger('sockets')
    if hasattr(log, level):
        getattr(log, level)(msg)
