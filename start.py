#!/usr/bin/env python
# encoding:utf-8

from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from manage import create_app
import os

app = create_app()

http_server = HTTPServer(WSGIContainer(app), ssl_options={
    "certfile": os.path.join(os.path.abspath("ca"), "1_www.new-huge.cn_bundle.crt"),
    "keyfile": os.path.join(os.path.abspath("ca"), "2_www.new-huge.cn.key"),
    })
http_server.listen(80)
IOLoop.instance().start()
