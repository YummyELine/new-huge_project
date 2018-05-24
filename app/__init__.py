# coding:utf8
from flask import Flask ,render_template,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
# from app.exts import db
import app.config
import os

app = Flask(__name__)
app.config.from_object(config)
# db.init_app(app)
db = SQLAlchemy(app)
# app.debug = True

from app.home_cn import home_cn as home_cn_blueprint
from app.home import home as home_blueprint
from app.admin import admin as admin_blueprint


app.register_blueprint(home_cn_blueprint, url_prefix = "/cn")
app.register_blueprint(home_blueprint)
app.register_blueprint(admin_blueprint, url_prefix = "/admin")


# 404错误页面
@app.errorhandler(404)
def page_not_found(error):
    return render_template("home_cn/404.html"), 404



