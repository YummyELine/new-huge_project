#!/usr/bin/env python
# encoding:utf-8

from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from manage import create_app
import os

app = create_app()

http_server = HTTPServer(WSGIContainer(app), ssl_options={
    "certfile": os.path.join(os.path.abspath("ca"), "server.crt"),
    "keyfile": os.path.join(os.path.abspath("ca"), "server.key"),
    })
http_server.listen(443)
IOLoop.instance().start()
