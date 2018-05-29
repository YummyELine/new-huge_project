# coding:utf8

from datetime import datetime
from exts import db

# # # _________________________
# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from datetime import datetime
#
# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://root:root03228396@127.0.0.1:3306/newhuge"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# db = SQLAlchemy(app)

# # # ---------------------------

# 关于我们
class About(db.Model):
    __tablename__ = "about"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 标题
    info = db.Column(db.Text)  # 简介
    info_en = db.Column(db.Text)  # 简介英语
    is_enable = db.Column(db.SmallInteger)  # 是否启用，1为启用， 0为不启用
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间

    def __repr__(self):
        return "<About {}>".format(self.name)



# 关于我们
class Contact(db.Model):
    __tablename__ = "contact"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 标题
    info = db.Column(db.Text)  # 简介
    info_en = db.Column(db.Text)  # 简介英语
    is_enable = db.Column(db.SmallInteger)  # 是否启用，1为启用， 0为不启用
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间

    def __repr__(self):
        return "<Contact {}>".format(self.name)


# 标签
class Tag(db.Model):
    __tablename__ = "tag"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 标题
    name_en = db.Column(db.String(100), unique=True)  # 标题英语
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间
    product = db.relationship("Product", backref='tag')  # 产品外键键值关联

    def __repr__(self):
        return "<Tag {}>".format(self.name)


# 产品管理
class Product(db.Model):
    __tablename__ = "product"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    title = db.Column(db.String(255), unique=True)  # 标题
    title_en = db.Column(db.String(255), unique=True)  # 标题英语
    info = db.Column(db.Text)  # 简介
    info_en = db.Column(db.Text)  # 简介英语
    logo = db.Column(db.String(255), unique=True)  # 封面
    playnum = db.Column(db.BigInteger)  # 播放量
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))  # 所属标签
    release_time = db.Column(db.Date)  # 上映时间
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间

    def __repr__(self):
        return "<Product {}>".format(self.title)


# 预告
class Preview(db.Model):
    __tablename__ = "preview"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    title = db.Column(db.String(255), unique=True)  # 标题
    logo = db.Column(db.String(255), unique=True)  # 封面
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间
    
    def __repr__(self):
        return "<Preview {}>".format(self.title)




# 权限
class Auth(db.Model):
    __tablename__ = "auth"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 名称
    url = db.Column(db.String(255), unique=True)  # 地址
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)
    
    def __repr__(self):
        return "<Auth {}>".format(self.name)


# 角色
class Role(db.Model):
    __tablename__ = "role"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 名称
    auths = db.Column(db.String(600))  # 地址
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)
    admins = db.relationship("Admin", backref='role')  # 管理员外键关系关联
    
    def __repr__(self):
        return "<Role {}>".format(self.name)


# 管理员
class Admin(db.Model):
    __tablename__ = "admin"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 管理员账号# unique 唯一约束
    pwd = db.Column(db.String(100))  # 管理员密码
    is_super = db.Column(db.SmallInteger)  # 是否为超级管理员，0为超级管理员
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))  # 所属角色
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)
    adminlogs = db.relationship("Adminlog", backref='admin')  # 管理员登录日志外键关系关联
    oplogs = db.relationship("Oplog", backref='admin')  # 管理员操作日志外键关系关联
    
    def __repr__(self):
        return "<Admin {}>".format(self.name)
    
    # 验证哈希加密的密码是否正确
    def check_pwd(self, pwd):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.pwd, pwd)


# 管理员登录日志
class Adminlog(db.Model):
    __tablename__ = "adminlog"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))  # 所属会员
    ip = db.Column(db.String(100))  # 登录IP
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 登录时间
    
    def __repr__(self):
        return "<Adminlog {}>".format(self.id)


# 操作日志
class Oplog(db.Model):
    __tablename__ = "Oplog"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))  # 所属会员
    ip = db.Column(db.String(100))  # 登录IP
    reason = db.Column(db.String(600))  # 操作原因
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 登录时间
    
    def __repr__(self):
        return "<Oplog {}>".format(self.id)


if __name__ == '__main__':
    # pass
    db.create_all()
    # 测试数据
    # role = Role(
    #     name="超级管理员",
    #     auths= ''
    # )
    # db.session.add(role)
    # db.session.commit()

# from werkzeug.security import generate_password_hash
#
# admin = Admin(
#     name='immovie',
#     pwd=generate_password_hash('immovie'),
#     is_super=0,
#     role_id=1
# )
# db.session.add(admin)
# db.session.commit()
