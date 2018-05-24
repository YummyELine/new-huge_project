# coding:utf8
from . import home_cn
from flask import render_template, redirect, url_for, request
from app.models import Preview, Tag, Product, About, Contact


@home_cn.route("/")
def index():
    return redirect(url_for("home_cn.about"))


# 产品
@home_cn.route("/product/<int:page>/")
def product(page=None):
    tags = Tag.query.all()
    page_data = Product.query
    # 标签
    tid = request.args.get("tid", 0)
    if int(tid) != 0:
        page_data = page_data.filter_by(tag_id=int(tid))
        # 时间
    time = request.args.get("time", 0)
    if int(time) != 0:
        if int(time) == 1:
            page_data = page_data.order_by(Product.addtime.desc())
        else:
            page_data = page_data.order_by(Product.addtime.asc())
    # page = request.args.get("page", 1)
    if page is None:
        page = 1
    page_data = page_data.paginate(page=page, per_page=10)
    p = dict(
        tid=tid,
        time=time
        )
    return render_template("home_cn/product.html", tags=tags, p=p, page_data=page_data)


# 首页动态图  上映预告
@home_cn.route("/animation/")
def animation():
    data = Preview.query.all()
    return render_template("home_cn/animation.html", data=data)


# 搜索
@home_cn.route("/search/<int:page>/")
def search(page=None):
    if page is None:
        page = 1
    key = request.args.get("key", "")
    product_count = Product.query.filter(
        Product.title.ilike('%' + key + '%')
        ).count()
    page_data = Product.query.filter(
        Product.title.ilike('%' + key + '%')
        ).order_by(
        Product.addtime.desc()
        ).paginate(page=page, per_page=10)
    return render_template("home_cn/search.html", key=key, page_data=page_data, product_count=product_count)


# 产品详情
@home_cn.route("/product/details/<int:id>/", methods=["GET"])
def product_details(id=None):
    product = Product.query.join(Tag).filter(
        Tag.id == Product.tag_id
        , Product.id == int(id)
        ).first_or_404()
    return render_template("home_cn/product_details.html",product=product)

# 关于
@home_cn.route("/about/")
def about():
    about =About.query.filter(About.is_enable == 1).first_or_404()
 
    return render_template("home_cn/about.html",about=about)

# 联系我们
@home_cn.route("/contact/")
def contact():
    contact = Contact.query.filter(Contact.is_enable == 1).first_or_404()
    return render_template("home_cn/contact.html",contact=contact)