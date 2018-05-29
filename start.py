#!/usr/bin/env python
# encoding:utf-8

from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from manage import create_app

app =create_app()
http_server = HTTPServer(WSGIContainer(app))
http_server.listen(80)
IOLoop.instance().start()
