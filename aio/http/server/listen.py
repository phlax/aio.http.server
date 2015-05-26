import logging

import aio.app


@aio.app.signal.listener
def sockets_emitted(signal):
    level, msg = signal.data
    log = logging.getLogger('sockets')
    if hasattr(log, level):
        getattr(log, level)(msg)
