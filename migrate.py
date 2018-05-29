# coding:utf8

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from manage import create_app
from exts import db

app = create_app()
from app.models import Tag,Preview,Auth,Role,Admin,Adminlog,Oplog,Product,About,Contact


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