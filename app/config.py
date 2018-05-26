#!/usr/bin/env python
# encoding:utf-8
import os

DEBUG = True

SECRET_KEY = os.urandom(24)

# 定义上传路径
UP_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), "static/uploads/")
FC_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), "static/uploads/users/")

# dialect+driver://username:password@host:port/database

DIALECT = 'mysql'
DRIVER = 'mysqlconnector'
USERNAME = 'root'
PASSWORD = 'root03228396'
HOST = '127.0.0.1'
PORT = '3306'
DATABASE = 'newhuge'

SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT, DRIVER, USERNAME,
                                                                       PASSWORD, HOST, PORT, DATABASE)
UEDITOR_UPLOAD_PATH = os.path.join(os.path.dirname(__file__),'images')

SQLALCHEMY_TRACK_MODIFICATIONS = False
