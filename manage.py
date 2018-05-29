# coding:utf8

from flask import Flask, render_template
from app.home_cn import home_cn as home_cn_blueprint
from app.home_en import home_en as home_en_blueprint
from app.home import home as home_blueprint
from app.admin import admin as admin_blueprint
from app.ueditor import bp as ueditor_blueprint
from exts import db
import config

from flask_wtf import CSRFProtect


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    
    app.register_blueprint(home_cn_blueprint, url_prefix="/cn")
    app.register_blueprint(home_en_blueprint, url_prefix="/en")
    app.register_blueprint(home_blueprint)
    app.register_blueprint(admin_blueprint, url_prefix="/admin")
    app.register_blueprint(ueditor_blueprint)
    
    db.init_app(app)
    CSRFProtect(app)
    
    # 404错误页面
    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("home_cn/404.html"), 404
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run()
