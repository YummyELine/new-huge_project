# coding:utf8
from flask import Blueprint
home_cn = Blueprint("home_cn", __name__)
import app.home_cn.views
