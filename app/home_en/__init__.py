# coding:utf8
from flask import Blueprint
home_en = Blueprint("home_en", __name__)
import app.home_en.views
