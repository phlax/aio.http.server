aio.http.server
===============

HTTP server for the aio_ asyncio framework

.. _aio: https://github.com/phlax/aio


Build status
------------

.. image:: https://travis-ci.org/phlax/aio.http.server.svg?branch=master
	       :target: https://travis-ci.org/phlax/aio.http.server


Installation
------------

Requires python >= 3.4

Install with:

.. code:: bash

	  pip install aio.http.server


Quick start - Hello world http server
-------------------------------------

Create a web server that says hello

Save the following into a file "hello.conf"

.. code:: ini
	  
	  [server/my_server]
	  factory = aio.http.server.factory
	  port = 8080
	  protocol = my_example.protocol_factory	  

	  
And save the following into a file named my_example.py
	  
.. code:: python

	  import asyncio
	  import aiohttp

	  @asyncio.coroutine
	  def protocol_factory(name):
	      loop = asyncio.get_event_loop()
	      webapp = aiohttp.web.Application(loop=loop)

	      @asyncio.coroutine
	      def handle_hello_world(webapp):
	          return aiohttp.web.Response(body=b"Hello, world")

	      webapp.router.add_route("GET", "/", handle_hello_world)
	      return webapp.make_handler()
	      	     	      

Run with the aio run command

.. code:: bash

	  aio run -c hello.conf

	  
