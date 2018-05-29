# coding:utf8
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, TextAreaField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, ValidationError, EqualTo
from app.models import Admin

# tags = Tag.query.all()
# auth_list = Auth.query.all()
# role_list = Role.query.all()


# 登录表单
class LoginForm(FlaskForm):
    """管理员登录表单"""
    account = StringField(
        label="账号",
        validators=[
            DataRequired("请输入账号！")
            ],
        description="账号",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入账号！",
            "required": "required"  # 字段必填
            }
        
        )
    pwd = PasswordField(
        label="密码",
        validators=[
            DataRequired("请输入密码！")
            ],
        description="密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入密码！",
            # "required": "required"  # 字段必填
            }
        
        )
    submit = SubmitField(
        '登录',
        render_kw={
            "class": "btn btn-primary btn-block btn-flat",
            }
        )
    
    def validate_account(self, field):
        account = field.data
        admin = Admin.query.filter_by(name=account).count()
        if admin == 0:
            raise ValidationError("账号不存在！")


# 标签表单
class TagForm(FlaskForm):
    name = StringField(
        label="标签",
        validators=[
            DataRequired("请输入标签！")
            ],
        description="标签",
        render_kw={
            "class": "form-control",
            "id": "input_name",
            "placeholder": "请输入标签名称！",
            "required": "required"  # 字段必填
            }
        
        )
    name_en = StringField(
        label="英语标签",
        validators=[
            DataRequired("请输入英语标签！")
            ],
        description="英语标签",
        render_kw={
            "class": "form-control",
            "id": "input_name",
            "placeholder": "请输入英语标签名称！",
            "required": "required"  # 字段必填
            }
        
        )
    submit = SubmitField(
        '添加',
        render_kw={
            "class": "btn btn-primary",
            }
        )
    submit1 = SubmitField(
        '编辑',
        render_kw={
            "class": "btn btn-primary",
            }
        )


# 关于表单
class AboutForm(FlaskForm):
    name = StringField(
        label="名称",
        validators=[
            DataRequired("请输入名称！")
            ],
        description="名称",
        render_kw={
            "class": "form-control",
            "id": "input_name",
            "placeholder": "请输入标名称！",
            "required": "required"  # 字段必填
            }
        
        )
    info = TextAreaField(
        label="详细介绍",
        validators=[
            DataRequired("请输入详细介绍！")
            ],
        description="详细介绍",
        render_kw={
            'id': "input_info"
            }
        )
    info_en = TextAreaField(
        label="英语详细介绍",
        validators=[
            DataRequired("请输入英语详细介绍！")
            ],
        description="英语详细介绍",
        render_kw={
            'id': "input_info_en"
            }
        )
    submit = SubmitField(
        '添加',
        render_kw={
            "class": "btn btn-primary",
            }
        )
    submit1 = SubmitField(
        '修改',
        render_kw={
            "class": "btn btn-primary",
            }
        )
    
    
# 关于表单
class ContactForm(FlaskForm):
    name = StringField(
        label="名称",
        validators=[
            DataRequired("请输入名称！")
            ],
        description="名称",
        render_kw={
            "class": "form-control",
            "id": "input_name",
            "placeholder": "请输入名称！",
            "required": "required"  # 字段必填
            }
        
        )
    info = TextAreaField(
        label="详细介绍",
        validators=[
            DataRequired("请输入详细介绍！")
            ],
        description="详细介绍",
        render_kw={
            'id': "input_info"
            }
        )
    info_en = TextAreaField(
        label="英语详细介绍",
        validators=[
            DataRequired("请输入英语详细介绍！")
            ],
        description="英语详细介绍",
        render_kw={
            'id': "input_info_en"
            }
        )
    submit = SubmitField(
        '添加',
        render_kw={
            "class": "btn btn-primary",
            }
        )
    submit1 = SubmitField(
        '修改',
        render_kw={
            "class": "btn btn-primary",
            }
        )


# 电影表单--产品
class ProductForm(FlaskForm):
    title = StringField(
        label="产品",
        validators=[
            DataRequired("请输入产品标题！")
            ],
        description="产品",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入产品标题！",
            "required": "required"  # 字段必填
            }
        
        )
    title_en = StringField(
        label="产品（英语）",
        validators=[
            DataRequired("请输入产品（英语）标题！")
            ],
        description="产品（英语）",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入产品（英语）标题！",
            "required": "required"  # 字段必填
            }
        
        )
    
    info = TextAreaField(
        label="详细介绍",
        validators=[
            DataRequired("请输入详细介绍！")
            ],
        description="详细介绍",
        render_kw={
            'id': "input_info"
            }
        )
    info_en = TextAreaField(
        label="英语详细介绍",
        validators=[
            DataRequired("请输入英语详细介绍！")
            ],
        description="英语详细介绍",
        render_kw={
            'id': "input_info_en"
            }
        )
    
    logo = FileField(
        label="封面",
        validators=[
            DataRequired("请上传封面！")
            ],
        description="封面",
        )
    
    tag_id = SelectField(
        label="标签",
        validators=[
            DataRequired("请选择标签！")
            ],
        coerce=int,
        # choices=[(v.id, v.name) for v in tags],
        description="标签",
        render_kw={
            "class": "form-control",
            }
        )
    
    release_time = StringField(
        label="上架时间",
        validators=[
            DataRequired("请输入上架时间！")
            ],
        description="上架时间",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入上架时间！",
            "id": "input_release_time"
            }
        )
    submit = SubmitField(
        '添加',
        render_kw={
            "class": "btn btn-primary",
            }
        )
    submit1 = SubmitField(
        '修改',
        render_kw={
            "class": "btn btn-primary",
            }
        )


# 上映预告表单
class PreviewForm(FlaskForm):
    title = StringField(
        label="预告标题",
        validators=[
            DataRequired("请输入预告标题！")
            ],
        description="预告标题",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入预告标题！",
            "required": "required"  # 字段必填
            }
        )
    logo = FileField(
        label="预告封面",
        validators=[
            DataRequired("请上传预告封面！")
            ],
        description="预告封面",
        )
    submit = SubmitField(
        '添加',
        render_kw={
            "class": "btn btn-primary",
            }
        )
    submit1 = SubmitField(
        '编辑',
        render_kw={
            "class": "btn btn-primary",
            }
        )


class PwdForm(FlaskForm):
    old_pwd = PasswordField(
        label="旧密码",
        validators=[
            DataRequired("请输入旧密码！")
            ],
        description="旧密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入旧密码！",
            }
        
        )
    new_pwd = PasswordField(
        label="新密码",
        validators=[
            DataRequired("请输入新密码！")
            ],
        description="新密码",
        render_kw={
            "class": "form-control",
            "placeholder": "新请输入密码！",
            }
        )
    submit = SubmitField(
        '编辑',
        render_kw={
            "class": "btn btn-primary",
            }
        )
    
    def validate_old_pwd(self, field):
        from flask import session
        pwd = field.data
        name = session["admin"]
        admin = Admin.query.filter_by(name=name).first()
        if not admin.check_pwd(pwd):
            raise ValidationError("旧密码错误！")


class AuthForm(FlaskForm):
    name = StringField(
        label="权限名称",
        validators=[
            DataRequired("请输入权限名称！")
            ],
        description="权限名称",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入权限名称！",
            }
        )
    url = StringField(
        label="权限地址",
        validators=[
            DataRequired("请输入权限地址！")
            ],
        description="权限地址",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入权限地址！",
            }
        )
    submit = SubmitField(
        '添加',
        render_kw={
            "class": "btn btn-primary",
            }
        )
    submit1 = SubmitField(
        '修改',
        render_kw={
            "class": "btn btn-primary",
            }
        )


class RoleForm(FlaskForm):
    name = StringField(
        label="角色名称",
        validators=[
            DataRequired("请输入角色名称！")
            ],
        description="角色名称",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入角色名称！",
            }
        )
    auths = SelectMultipleField(
        label="权限列表",
        validators=[
            DataRequired("请输入权限名称！")
            ],
        coerce=int,
        # choices=[(v.id, v.name) for v in auth_list],
        description="权限名称",
        render_kw={
            "class": "form-control",
            }
        )
    submit = SubmitField(
        '添加',
        render_kw={
            "class": "btn btn-primary",
            }
        )
    submit1 = SubmitField(
        '修改',
        render_kw={
            "class": "btn btn-primary",
            }
        )


class AdminForm(FlaskForm):
    name = StringField(
        label="管理员名称",
        validators=[
            DataRequired("请输入管理员名称！")
            ],
        description="管理员名称",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入管理员名称！",
            }
        )
    pwd = PasswordField(
        label="管理员密码",
        validators=[
            DataRequired("请输入管理员密码！")
            ],
        description="管理员密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入管理员密码！",
            }
        )
    repwd = PasswordField(
        label="管理员重复密码",
        validators=[
            DataRequired("请输入管理员重复密码！"),
            EqualTo('pwd', message="两次密码不一致！")
            ],
        description="管理员重复密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入管理员重复密码！",
            }
        )
    role_id = SelectField(
        label="所属角色",
        coerce=int,
        # choices=[(v.id, v.name) for v in role_list],
        render_kw={
            "class": "form-control",
            }
        )
    submit = SubmitField(
        '添加',
        render_kw={
            "class": "btn btn-primary",
            }
        )
