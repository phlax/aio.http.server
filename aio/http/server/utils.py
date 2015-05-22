
from datetime import datetime
import asyncio

import aio.app


@asyncio.coroutine
def get_socket_logs():
    logfile = aio.app.config['aio']['socket_log']
    with open(logfile) as lf:
        res = []
        for l in lf.readlines():
            if not l.strip():
                continue
            parts = l.strip().split(' ')
            dparts = parts[0].split('-') + parts[1].split(',')[0].split(':')
            t = datetime(*[int(d) for d in dparts])
            msg = ' '.join(
                [x.strip("'")
                 for x in ' '.join(parts[2:]).strip("[]").split(",")])
            res.append([t.strftime("%d/%m %H:%M"), msg])

    return reversed(res)
