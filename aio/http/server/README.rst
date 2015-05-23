aio.http.server usage
=====================


Configuration
-------------

Create a server config with the aio.http.server.factory factory and suppressing normal output

>>> config = """
... [aio]
... log_level = ERROR
... 
... [server/test]
... factory: aio.http.server.factory
... port: 7070
... """  


Running an http server
----------------------

By default the http server will respond with a 404 as there are no routes set up

>>> import asyncio
>>> import aiohttp
>>> from aio.app.runner import runner
>>> import aio.testing

>>> @aio.testing.run_forever(sleep=1)
... def run_http_server():
...     yield from runner(['run'], config_string=config)
... 
...     def call_http_server():
...         result = yield from (
...             yield from aiohttp.request(
...                "GET", "http://localhost:7070")).read()  
...         print(result)
... 
...     return call_http_server

>>> run_http_server()
b'404: Not Found'

The server object is accessible from the aio.app.servers[{name}] var

>>> import aio.app
  
>>> aio.app.servers['test']
<Server sockets=[<socket.socket...laddr=('0.0.0.0', 7070)...]>

Lets clear the app

>>> aio.app.clear()
  

Running the server with a custom protocol
-----------------------------------------

If you specify a protocol in the "server/" config, the http server will use that function as a protocol factory.

The function should be a coroutine and is called with the name of the server

>>> config_with_protocol = """
... [aio]
... log_level = ERROR
... 
... [server/test]
... factory = aio.http.server.factory
... protocol = aio.http.server.tests._example_http_protocol
... port = 7070
... """  

>>> @asyncio.coroutine
... def http_protocol_factory(name):
...     loop = asyncio.get_event_loop()
...     http_app = aiohttp.web.Application(loop=loop)
...     http_app['name'] = name
... 
...     @asyncio.coroutine  
...     def handle_hello_world(http_app):
...         return aiohttp.web.Response(body=b"Hello, world")
... 
...     http_app.router.add_route("GET", "/", handle_hello_world)
...     return http_app.make_handler()

>>> aio.http.server.tests._example_http_protocol = http_protocol_factory

>>> @aio.testing.run_forever(sleep=1)
... def run_http_server():
...     yield from runner(['run'], config_string=config_with_protocol)
... 
...     def call_http_server():
...         result = yield from (
...             yield from aiohttp.request(
...                "GET", "http://localhost:7070")).read()
... 
...         print(result)
... 
...     return call_http_server
  
>>> run_http_server()
b'Hello, world'
