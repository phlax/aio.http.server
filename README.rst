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
Install with:

.. code:: bash

	  pip install aio.http.server


Configuration
-------------

Example configuration for a hello world server

.. code:: ini

	  [server/test]
	  factory = aio.http.server.factory
	  protocol = my.example.protocol_factory
	  port = 8080


And the corresponding protocol_factory

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


Running
-------

Run with the aio command

.. code:: bash

	  aio run
