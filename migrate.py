# coding:utf8

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import app
from app import db

from app.models import User,Userlog,Tag,Movie,Preview,Comment,Moviecol,Auth,Role,Admin,Adminlog,Oplog


# python manage.py db init  第一次执行
# python manage.py db migrate 都要执行
# python manage.py db upgrade 都要执行
# 模型 -> 迁移文件 -> 表
manager = Manager(app)

# 使用Migrate绑定app和db
migrate = Migrate(app, db)

# 添加迁移脚本的命令到manager中
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
	manager.run()