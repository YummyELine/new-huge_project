# coding:utf8

from . import admin
from flask import render_template, redirect, url_for, flash, session, request, abort
from app.admin.forms import (LoginForm, TagForm, ProductForm, PreviewForm, PwdForm, AuthForm, RoleForm, AdminForm,
                             ContactForm, AboutForm)
from app.models import Admin, Tag, Product, Preview, Oplog, Adminlog, Auth, Role, About, Contact
from functools import wraps  # 定义装饰器
from app import db, app
from werkzeug.utils import secure_filename  # 上传安全
import os
import uuid
import datetime


# 上下应用处理器  在admin.html 直接使用 online_time
@admin.context_processor
def tpl_extra():
    data = dict(
        online_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
    return data


# 定义登录装饰器
def admin_login_req(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "admin" not in session:
            return redirect(url_for("admin.login", next=request.url))
        return f(*args, **kwargs)
    
    return decorated_function


# 权限控制装饰器
def admin_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        admin = Admin.query.join(
            Role).filter(
            Role.id == Admin.role_id
            , Admin.id == session["admin_id"]).first()
        if admin.is_super == 1:
            auths = admin.role.auths
            auths = list(map(lambda v: int(v), auths.split(",")))
            auth_list = Auth.query.all()
            urls = [v.url for v in auth_list for val in auths if val == v.id]
            rule = request.url_rule
            print(urls)
            print(rule)
            print(str(rule))
            if str(rule) not in urls:
                abort(404)
        return f(*args, **kwargs)
    
    return decorated_function


# 修改文件名称
def change_filename(filename):
    fileinfo = os.path.splitext(filename)
    filename = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + str(uuid.uuid4().hex) + fileinfo[-1]
    return filename


@admin.route("/")
# @admin_login_req
# @admin_auth
def index():
    # role = Role(
    #     name="超级管理员",
    #     auths=''
    #     )
    # db.session.add(role)
    # db.session.commit()
    # ################_________________
    # from werkzeug.security import generate_password_hash
    #
    # admin = Admin(
    #     name='admin',
    #     pwd=generate_password_hash('1'),
    #     is_super=0,
    #     role_id=1
    #     )
    # db.session.add(admin)
    # db.session.commit()
    
    return redirect(url_for('admin.tag_list', page=1))


# 登录
@admin.route("/login/", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        admin = Admin.query.filter_by(name=data["account"]).first()
        if not admin.check_pwd(data["pwd"]):
            flash("密码错误!", "err")  # 弹出错误信息
            return redirect(url_for("admin.login"))
        session["admin"] = data["account"]
        session["admin_id"] = admin.id
        adminlog = Adminlog(
            admin_id=session["admin_id"],
            ip=request.remote_addr,
            )
        db.session.add(adminlog)
        db.session.commit()
        return redirect(request.args.get("next") or url_for("admin.index"))
    return render_template("admin/login.html", form=form)


# 登出
@admin.route("/logout/")
@admin_login_req
def logout():
    session.pop("admin", None)
    session.pop("admin_id", None)
    return redirect(url_for("admin.login"))


# 修改密码
@admin.route("/pwd/", methods=["GET", "POST"])
@admin_login_req
def pwd():
    form = PwdForm()
    if form.validate_on_submit():
        data = form.data
        admin = Admin.query.filter_by(name=session["admin"]).first()
        from werkzeug.security import generate_password_hash
        admin.pwd = generate_password_hash(data["new_pwd"])
        db.session.add(admin)
        db.session.commit()
        flash("修改密码成功", "ok")
        session.pop("admin", None)
        session.pop("admin_id", None)
        return redirect(url_for('admin.login'))
    return render_template("admin/pwd.html", form=form)


# 标签添加
@admin.route("/tag/add/", methods=["GET", "POST"])
@admin_login_req
@admin_auth
def tag_add():
    form = TagForm()
    if form.validate_on_submit():
        data = form.data
        tag = Tag.query.filter_by(name=data["name"]).count()
        tag_en = Tag.query.filter_by(name=data["name_en"]).count()
        if tag == 1 or tag_en == 1:
            flash("名称已经存在!", "err")
            return redirect(url_for('admin.tag_add'))
        tag = Tag(
            name=data["name"],
            name_en=data["name_en"]
            )
        db.session.add(tag)
        db.session.commit()
        flash("添加标签成功！", "ok")
        oplog = Oplog(
            admin_id=session["admin_id"],
            ip=request.remote_addr,
            reason="添加标签:{}".format(data["name"], )
            )
        db.session.add(oplog)
        db.session.commit()
        
        return redirect(url_for("admin.tag_add"))
    return render_template("admin/tag_add.html", form=form)


# 标签列表
@admin.route("/tag/list/<int:page>/", methods=['GET'])
@admin_login_req
@admin_auth
def tag_list(page=None):
    if page is None:
        page = 1
    page_data = Tag.query.order_by(
        Tag.addtime.desc()
        ).paginate(page=page, per_page=10)
    return render_template("admin/tag_list.html", page_data=page_data)


# 标签编辑
@admin.route("/tag/edit/<int:id>/", methods=["GET", "POST"])
@admin_login_req
@admin_auth
def tag_edit(id=None):
    form = TagForm()
    tag = Tag.query.get_or_404(id)
    if form.validate_on_submit():
        data = form.data
        tag_count = Tag.query.filter_by(name=data["name"]).count()
        tag_count_en = Tag.query.filter_by(name=data["name_en"]).count()
        before_name = tag.name
        before_name_en = tag.name_en
        if tag.name != data['name'] and (tag_count == 1 or tag_count_en == 1):
            flash("名称已经存在!", "err")
            return redirect(url_for('admin.tag_add', id=id))
        tag.name = data['name']
        tag.name_en = data['name_en']
        db.session.add(tag)
        db.session.commit()
        flash("修改标签成功！", 'ok')
        oplog = Oplog(
            admin_id=session["admin_id"],
            ip=request.remote_addr,
            reason="修改标签:中文：修改前{}、修改后{},英文：修改前{}、修改后{}".format(before_name, data["name"], before_name_en,
                                                               data["name_en"])
            )
        db.session.add(oplog)
        db.session.commit()
        redirect(url_for('admin.tag_edit', id=id))
    return render_template("admin/tag_edit.html", form=form, tag=tag)


# 标签删除
@admin.route("/tag/del/<int:id>", methods=['GET'])
@admin_login_req
@admin_auth
def tag_del(id=None):
    tag = Tag.query.filter_by(id=id).first_or_404()
    product = Product.query.filter(Product.tag_id==tag.id).count()
    if product >=1 :
        flash("已有产品使用这个标签，请先修改产品再删除！", "err")
        return redirect(url_for('admin.tag_list', page=1))
    db.session.delete(tag)
    db.session.commit()
    flash("删除标签成功！", "ok")
    oplog = Oplog(
        admin_id=session["admin_id"],
        ip=request.remote_addr,
        reason="删除标签{}".format(tag.name)
        )
    db.session.add(oplog)
    db.session.commit()
    return redirect(url_for('admin.tag_list', page=1))


# 添加电影
@admin.route("/product/add/", methods=["GET", "POST"])
@admin_login_req
@admin_auth
def product_add():
    form = ProductForm()
    if form.validate_on_submit():
        data = form.data
        # secure_filename 变成安全的名称
        file_logo = secure_filename(form.logo.data.filename)
        if not os.path.exists(app.config["UP_DIR"]):
            os.makedirs(app.config["UP_DIR"])
            # win系统不需要增加权限
            # os.chmod(app.config["UP_DIR"], "rw")
        logo = change_filename(file_logo)
        form.logo.data.save(app.config["UP_DIR"] + logo)
        product = Product(
            title=data['title'],
            title_en=data['title_en'],
            info=data['info'],
            info_en=data['info_en'],
            logo=logo,
            playnum=0,
            tag_id=int(data['tag_id']),
            release_time=data['release_time'],
            )
        db.session.add(product)
        db.session.commit()
        flash('添加产品成功！', 'ok')
        oplog = Oplog(
            admin_id=session["admin_id"],
            ip=request.remote_addr,
            reason="添加产品:{}".format(data["title"], )
            )
        db.session.add(oplog)
        db.session.commit()
        return redirect(url_for('admin.product_add'))
    
    return render_template("admin/product_add.html", form=form)


# 产品列表
@admin.route("/product/list/<int:page>", methods=["GET"])
@admin_login_req
@admin_auth
def product_list(page=None):
    if page is None:
        page = 1
    page_data = Product.query.join(Tag).filter(Tag.id == Product.tag_id).order_by(
        Product.addtime.desc()
        ).paginate(page=page, per_page=10)
    return render_template("admin/product_list.html", page_data=page_data)


# 电影删除
@admin.route("/product/del/<int:id>", methods=['GET'])
@admin_login_req
@admin_auth
def product_del(id=None):
    product = Product.query.filter_by(id=id).first_or_404()
    db.session.delete(product)
    db.session.commit()
    flash("删除产品成功！", "ok")
    oplog = Oplog(
        admin_id=session["admin_id"],
        ip=request.remote_addr,
        reason="删除产品:{}".format(product.title, )
        )
    db.session.add(oplog)
    db.session.commit()
    oplog = Oplog(
        admin_id=session["admin_id"],
        ip=request.remote_addr,
        reason="删除产品{}".format(product.title)
        )
    db.session.add(oplog)
    db.session.commit()
    return redirect(url_for('admin.product_list', page=1))


# 编辑电影
@admin.route("/product/edit/<int:id>", methods=["GET", "POST"])
@admin_login_req
@admin_auth
def product_edit(id=None):
    form = ProductForm()
    form.logo.validators = []
    product = Product.query.get_or_404(int(id))
    if request.method == "GET":
        form.info.data = product.info
        form.info_en.data = product.info_en
        form.tag_id.data = product.tag_id
    if form.validate_on_submit():
        data = form.data
        product_count = Product.query.filter_by(title=data["title"]).count()
        product_count_en = Product.query.filter_by(title=data["title_en"]).count()
        if (product_count == 1 or product_count_en == 1) and product.title != data["title"]:
            flash('名称已经存在！', 'err')
            return redirect(url_for('admin.product_edit', id=product.id))
        
        if not os.path.exists(app.config["UP_DIR"]):
            os.makedirs(app.config["UP_DIR"])
            # win系统不需要增加权限
            # os.chmod(app.config["UP_DIR"], "rw")
        
        if data["logo"] != "":
            file_logo = secure_filename(form.logo.data.filename)
            product.logo = change_filename(file_logo)
            form.logo.data.save(app.config["UP_DIR"] + product.logo)
        
        product.tag_id = data["tag_id"]
        product.info = data["info"]
        product.info_en = data["info_en"]
        product.title = data["title"]
        product.title_en = data["title_en"]
        product.release_time = data["release_time"]
        db.session.add(product)
        db.session.commit()
        flash('修改产品成功！', 'ok')
        oplog = Oplog(
            admin_id=session["admin_id"],
            ip=request.remote_addr,
            reason="修改产品{}".format(product.title)
            )
        db.session.add(oplog)
        db.session.commit()
        return redirect(url_for('admin.product_edit', id=product.id))
    return render_template("admin/product_edit.html", form=form, product=product)


# 添加预告
@admin.route("/preview/add/", methods=["GET", "POST"])
@admin_login_req
@admin_auth
def preview_add():
    form = PreviewForm()
    if form.validate_on_submit():
        data = form.data
        # secure_filename 变成安全的名称
        file_logo = secure_filename(form.logo.data.filename)
        if not os.path.exists(app.config["UP_DIR"]):
            os.makedirs(app.config["UP_DIR"])
            # win系统不需要增加权限
            # os.chmod(app.config["UP_DIR"], "rw")
        logo = change_filename(file_logo)
        form.logo.data.save(app.config["UP_DIR"] + logo)
        preview = Preview(
            title=data['title'],
            logo=logo
            )
        db.session.add(preview)
        db.session.commit()
        oplog = Oplog(
            admin_id=session["admin_id"],
            ip=request.remote_addr,
            reason="添加图片轮播{}".format(data['title'])
            )
        db.session.add(oplog)
        db.session.commit()
        flash('添加上映预告成功！', 'ok')
        return redirect(url_for('admin.preview_add'))
    return render_template("admin/preview_add.html", form=form)


# 预告列表
@admin.route("/preview/list/<int:page>", methods=["GET"])
@admin_login_req
@admin_auth
def preview_list(page=None):
    if page is None:
        page = 1
    page_data = Preview.query.order_by(
        Preview.addtime.desc()
        ).paginate(page=page, per_page=10)
    return render_template("admin/preview_list.html", page_data=page_data)


# 上映预告删除
@admin.route("/preview/del/<int:id>", methods=['GET'])
@admin_login_req
@admin_auth
def preview_del(id=None):
    preview = Preview.query.filter_by(id=id).first_or_404()
    db.session.delete(preview)
    db.session.commit()
    flash("删除图片轮播成功！", "ok")
    oplog = Oplog(
        admin_id=session["admin_id"],
        ip=request.remote_addr,
        reason="删除图片轮播{}".format(preview.title)
        )
    db.session.add(oplog)
    db.session.commit()
    return redirect(url_for('admin.preview_list', page=1))


# 编辑预告
@admin.route("/preview/edit/<int:id>", methods=["GET", "POST"])
@admin_login_req
@admin_auth
def preview_edit(id=None):
    form = PreviewForm()
    form.logo.validators = []
    preview = Preview.query.get_or_404(int(id))
    if request.method == "GET":
        form.title.data = preview.title
    if form.validate_on_submit():
        data = form.data
        if data["logo"] != "":
            file_logo = secure_filename(form.logo.data.filename)
            preview.logo = change_filename(file_logo)
            form.logo.data.save(app.config["UP_DIR"] + preview.logo)
        preview.title = data["title"]
        db.session.add(preview)
        db.session.commit()
        flash('修改图片轮播成功！', 'ok')
        oplog = Oplog(
            admin_id=session["admin_id"],
            ip=request.remote_addr,
            reason="修改图片轮播{}".format(preview.title)
            )
        db.session.add(oplog)
        db.session.commit()
        return redirect(url_for('admin.preview_edit', id=id))
    return render_template("admin/preview_edit.html", form=form, preview=preview)


# 联系我们添加
@admin.route("/contact/add/", methods=["GET", "POST"])
@admin_login_req
@admin_auth
def contact_add():
    form = ContactForm()
    if form.validate_on_submit():
        data = form.data
        contact = Contact.query.filter_by(name=data["name"]).count()
        if contact == 1:
            flash("名称已经存在!", "err")
            return redirect(url_for('admin.contact_add'))
        contact = Contact(
            name=data["name"],
            info=data["info"],
            info_en=data["info_en"],
            is_enable=0
            )
        db.session.add(contact)
        db.session.commit()
        flash("添加成功！", "ok")
        oplog = Oplog(
            admin_id=session["admin_id"],
            ip=request.remote_addr,
            reason="联系添加:{}".format(data["name"], )
            )
        db.session.add(oplog)
        db.session.commit()
        
        redirect(url_for("admin.contact_add"))
    return render_template("admin/contact_add.html", form=form)


# 联系我们列表
@admin.route("/contact/list/<int:page>", methods=["GET"])
@admin_login_req
@admin_auth
def contact_list(page=None):
    if page is None:
        page = 1
    page_data = Contact.query.order_by(
        Contact.addtime.desc()
        ).paginate(page=page, per_page=10)
    return render_template("admin/contact_list.html", page_data=page_data)


# 联系我们删除
@admin.route("/contact/del/<int:id>", methods=['GET'])
@admin_login_req
@admin_auth
def contact_del(id=None):
    contact = Contact.query.filter_by(id=id).first_or_404()
    db.session.delete(contact)
    db.session.commit()
    flash("删除产品成功！", "ok")
    oplog = Oplog(
        admin_id=session["admin_id"],
        ip=request.remote_addr,
        reason="删除联系我们:{}".format(contact.name, )
        )
    db.session.add(oplog)
    db.session.commit()
    return redirect(url_for('admin.contact_list', page=1))


# 编辑联系我们
@admin.route("/contact/edit/<int:id>", methods=["GET", "POST"])
@admin_login_req
@admin_auth
def contact_edit(id=None):
    form = ContactForm()
    contact = Contact.query.get_or_404(int(id))
    if request.method == "GET":
        form.info.data = contact.info
        form.info_en.data = contact.info_en
    if form.validate_on_submit():
        data = form.data
        contact_count = Contact.query.filter_by(name=data["name"]).count()
        if contact_count == 1 and contact.name != data["name"]:
            flash('名称已经存在！', 'err')
            return redirect(url_for('admin.contact_edit', id=contact.id))
        contact.info = data["info"]
        contact.info_en = data["info_en"]
        contact.name = data["name"]
        db.session.add(contact)
        db.session.commit()
        flash('修改产联系我们成功！', 'ok')
        oplog = Oplog(
            admin_id=session["admin_id"],
            ip=request.remote_addr,
            reason="修改联系我们:{}".format(contact.name, )
            )
        db.session.add(oplog)
        db.session.commit()
        return redirect(url_for('admin.contact_edit', id=contact.id))
    return render_template("admin/contact_edit.html", form=form, contact=contact)


# 联系我们启用
@admin.route("/contact/enable/<int:id>", methods=['GET'])
@admin_login_req
@admin_auth
def contact_enable(id=None):
    contact_alls = Contact.query.all()
    for contact_all in contact_alls:
        contact_all.is_enable = 0
        db.session.add(contact_all)
        db.session.commit()
    contact = Contact.query.filter_by(id=id).first_or_404()
    contact.is_enable = 1
    db.session.add(contact)
    db.session.commit()
    flash("启用产品成功！", "ok")
    oplog = Oplog(
        admin_id=session["admin_id"],
        ip=request.remote_addr,
        reason="启用联系我们:{}".format(contact.name, )
        )
    db.session.add(oplog)
    db.session.commit()
    oplog = Oplog(
        admin_id=session["admin_id"],
        ip=request.remote_addr,
        reason="启用联系我们:{}".format(contact.name, )
        )
    db.session.add(oplog)
    db.session.commit()
    return redirect(url_for('admin.contact_list', page=1))


# 关于我们添加
@admin.route("/about/add/", methods=["GET", "POST"])
@admin_login_req
@admin_auth
def about_add():
    form = AboutForm()
    if form.validate_on_submit():
        data = form.data
        about = About.query.filter_by(name=data["name"]).count()
        if about == 1:
            flash("名称已经存在!", "err")
            return redirect(url_for('admin.about_add'))
        about = About(
            name=data["name"],
            info=data["info"],
            info_en=data["info_en"],
            is_enable=0
            )
        db.session.add(about)
        db.session.commit()
        flash("添加成功！", "ok")
        oplog = Oplog(
            admin_id=session["admin_id"],
            ip=request.remote_addr,
            reason="关于添加:{}".format(data["name"], )
            )
        db.session.add(oplog)
        db.session.commit()
        
        return redirect(url_for("admin.about_add"))
    return render_template("admin/about_add.html", form=form)


# 关于我们列表
@admin.route("/about/list/<int:page>", methods=["GET"])
@admin_login_req
@admin_auth
def about_list(page=None):
    if page is None:
        page = 1
    page_data = About.query.order_by(
        About.addtime.desc()
        ).paginate(page=page, per_page=10)
    return render_template("admin/about_list.html", page_data=page_data)


# 关于我们删除
@admin.route("/about/del/<int:id>", methods=['GET'])
@admin_login_req
@admin_auth
def about_del(id=None):
    about = About.query.filter_by(id=id).first_or_404()
    db.session.delete(about)
    db.session.commit()
    flash("删除成功！", "ok")
    oplog = Oplog(
        admin_id=session["admin_id"],
        ip=request.remote_addr,
        reason="删除关于我们:{}".format(about.name, )
        )
    db.session.add(oplog)
    db.session.commit()
    return redirect(url_for('admin.about_list', page=1))


# 编辑关于我们
@admin.route("/about/edit/<int:id>", methods=["GET", "POST"])
@admin_login_req
@admin_auth
def about_edit(id=None):
    form = AboutForm()
    about = About.query.get_or_404(int(id))
    if request.method == "GET":
        form.info.data = about.info
        form.info_en.data = about.info_en
    if form.validate_on_submit():
        data = form.data
        about_count = About.query.filter_by(name=data["name"]).count()
        if about_count == 1 and about.name != data["name"]:
            flash('名称已经存在！', 'err')
            return redirect(url_for('admin.contact_edit', id=about.id))
        about.info = data["info"]
        about.info_en = data["info_en"]
        about.name = data["name"]
        db.session.add(about)
        db.session.commit()
        flash('修改产联系我们成功！', 'ok')
        oplog = Oplog(
            admin_id=session["admin_id"],
            ip=request.remote_addr,
            reason="编辑关于我们:{}".format(about.name, )
            )
        db.session.add(oplog)
        db.session.commit()
        return redirect(url_for('admin.about_edit', id=about.id))
    return render_template("admin/about_edit.html", form=form, about=about)


# 关于我们启用
@admin.route("/about/enable/<int:id>", methods=['GET'])
@admin_login_req
@admin_auth
def about_enable(id=None):
    about_alls = About.query.all()
    for about_all in about_alls:
        about_all.is_enable = 0
        db.session.add(about_all)
        db.session.commit()
    about = About.query.filter_by(id=id).first_or_404()
    about.is_enable = 1
    db.session.add(about)
    db.session.commit()
    flash("启用产品成功！", "ok")
    oplog = Oplog(
        admin_id=session["admin_id"],
        ip=request.remote_addr,
        reason="启用关于我们:{}".format(about.name, )
        )
    db.session.add(oplog)
    db.session.commit()
    return redirect(url_for('admin.about_list', page=1))


# 操作日志列表
@admin.route("/oplog/list/<int:page>", methods=["GET"])
@admin_login_req
@admin_auth
def oplog_list(page=None):
    if page is None:
        page = 1
    page_data = Oplog.query.join(
        Admin).filter(
        Admin.id == Oplog.admin_id).order_by(
        Oplog.addtime.desc()
        ).paginate(page=page, per_page=10)
    return render_template("admin/oplog_list.html", page_data=page_data)


# 管理员登录日志列表
@admin.route("/adminloginlog/list/<int:page>", methods=["GET"])
@admin_login_req
@admin_auth
def adminloginlog_list(page=None):
    if page is None:
        page = 1
    page_data = Adminlog.query.join(
        Admin).filter(
        Admin.id == Adminlog.admin_id).order_by(
        Adminlog.addtime.desc()
        ).paginate(page=page, per_page=10)
    return render_template("admin/adminloginlog_list.html", page_data=page_data)


# 添加权限
@admin.route("/auth/add/", methods=["GET", "POST"])
@admin_login_req
@admin_auth
def auth_add():
    form = AuthForm()
    if form.validate_on_submit():
        data = form.data
        auth = Auth(
            name=data["name"],
            url=data["url"]
            )
        db.session.add(auth)
        db.session.commit()
        flash("添加权限成功！", "ok")
    return render_template("admin/auth_add.html", form=form)


# 权限列表
@admin.route("/auth/list/<int:page>", methods=['GET'])
@admin_login_req
@admin_auth
def auth_list(page=None):
    if page is None:
        page = 1
    page_data = Auth.query.order_by(
        Auth.addtime.desc()
        ).paginate(page=page, per_page=10)
    return render_template("admin/auth_list.html", page_data=page_data)


# 权限编辑
@admin.route("/auth/edit/<int:id>/", methods=["GET", "POST"])
@admin_login_req
@admin_auth
def auth_edit(id=None):
    form = AuthForm()
    auth = Auth.query.get_or_404(id)
    if form.validate_on_submit():
        data = form.data
        auth_count = Auth.query.filter_by(name=data["name"]).count()
        if auth.name != data['name'] and auth_count == 1:
            flash("名称已经存在!", "err")
            return redirect(url_for('admin.auth_edit', id=id))
        auth.name = data['name']
        auth.url = data['url']
        db.session.add(auth)
        db.session.commit()
        flash("修改权限成功！", 'ok')
        oplog = Oplog(
            admin_id=session["admin_id"],
            ip=request.remote_addr,
            reason="修改权限:{}".format(data["name"], )
            )
        db.session.add(oplog)
        db.session.commit()
        redirect(url_for('admin.auth_edit', id=id))
    return render_template("admin/auth_edit.html", form=form, auth=auth)


# 权限删除
@admin.route("/auth/del/<int:id>", methods=['GET'])
@admin_login_req
@admin_auth
def auth_del(id=None):
    auth = Auth.query.filter_by(id=id).first_or_404()
    db.session.delete(auth)
    db.session.commit()
    flash("删除标签成功！", "ok")
    return redirect(url_for('admin.auth_list', page=1))


# 添加角色
@admin.route("/role/add/", methods=["GET", "POST"])
@admin_login_req
@admin_auth
def role_add():
    form = RoleForm()
    if form.validate_on_submit():
        data = form.data
        role = Role(
            name=data["name"],
            auths=",".join(map(lambda v: str(v), data["auths"]))  # 列表转换为字符串
            )
        db.session.add(role)
        db.session.commit()
        flash("添加角色成功！", "ok")
    return render_template("admin/role_add.html", form=form)


# 角色列表
@admin.route("/role/list/<int:page>", methods=["GET"])
@admin_login_req
@admin_auth
def role_list(page=None):
    if page is None:
        page = 1
    page_data = Role.query.order_by(
        Role.addtime.desc()
        ).paginate(page=page, per_page=10)
    return render_template("admin/role_list.html", page_data=page_data)


# 角色删除
@admin.route("/role/del/<int:id>/", methods=['GET'])
@admin_login_req
@admin_auth
def role_del(id=None):
    role = Role.query.filter_by(id=id).first_or_404()
    db.session.delete(role)
    db.session.commit()
    flash("删除角色成功！", "ok")
    return redirect(url_for('admin.role_list', page=1))


# 编辑角色
@admin.route("/role/edit/<int:id>/", methods=["GET", "POST"])
@admin_login_req
@admin_auth
def role_edit(id=None):
    form = RoleForm()
    role = Role.query.get_or_404(id)
    if request.method == "GET":
        auths = role.auths
        # form.name.data = role.name
        form.auths.data = list(map(lambda v: int(v), auths.split(",")))
    if form.validate_on_submit():
        data = form.data
        role.name = data["name"]
        role.auths = ",".join(map(lambda v: str(v), data["auths"]))  # 列表转换为字符串
        db.session.add(role)
        db.session.commit()
        flash("修改角色成功！", "ok")
    return render_template("admin/role_edit.html", form=form, role=role)


# 添加管理员
@admin.route("/admin/add/", methods=["GET", "POST"])
@admin_login_req
@admin_auth
def admin_add():
    form = AdminForm()
    from werkzeug.security import generate_password_hash
    if form.validate_on_submit():
        data = form.data
        admin = Admin(
            name=data["name"],
            pwd=generate_password_hash(data["pwd"]),
            role_id=data["role_id"],
            is_super=1
            )
        db.session.add(admin)
        db.session.commit()
        flash("添加管理员成功！", "ok")
    return render_template("admin/admin_add.html", form=form)


# 管理员列表
@admin.route("/admin/list/<int:page>", methods=["GET"])
@admin_login_req
@admin_auth
def admin_list(page=None):
    if page is None:
        page = 1
    page_data = Admin.query.join(Role).filter(Admin.role_id == Role.id).order_by(
        Admin.addtime.desc()
        ).paginate(page=page, per_page=10)
    return render_template("admin/admin_list.html", page_data=page_data)
