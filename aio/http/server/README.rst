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
  >>> from aio.testing import aiofuturetest
  
  >>> def run_http_server():
  ...     yield from runner(['run'], config_string=config)
  ... 
  ...     @asyncio.coroutine
  ...     def call_http_server():
  ...         result = yield from (
  ...             yield from aiohttp.request(
  ...                "GET", "http://localhost:7070")).read()  
  ...         print(result)
  ... 
  ...     return call_http_server

  >>> aiofuturetest(run_http_server, sleep=1)()
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

  >>> def http_protocol_factory(name):
  ...     loop = asyncio.get_event_loop()
  ...     webapp = aiohttp.web.Application(loop=loop)
  ...     webapp['name'] = name
  ... 
  ...     def handle_hello_world(webapp):
  ...         return aiohttp.web.Response(body=b"Hello, world")
  ... 
  ...     webapp.router.add_route("GET", "/", asyncio.coroutine(handle_hello_world))
  ...     return webapp.make_handler()

  >>> aio.http.server.tests._example_http_protocol = asyncio.coroutine(http_protocol_factory)
  
  >>> def run_http_server():
  ...     yield from runner(['run'], config_string=config_with_protocol)
  ... 
  ...     @asyncio.coroutine
  ...     def call_http_server():
  ...         result = yield from (
  ...             yield from aiohttp.request(
  ...                "GET", "http://localhost:7070")).read()
  ... 
  ...         print(result)
  ... 
  ...     return call_http_server
  

  >>> aiofuturetest(run_http_server, sleep=1)()  
  b'Hello, world'
