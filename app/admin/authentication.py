from . import admin_blueprint
from app.forms.web_auth_form import LoginForm
from app.forms.admin_auth_form import AddAdminForm
from flask import request, render_template, redirect, url_for, flash
from app.models.admin_model import Admin
from app.data.admin_data import AdminInfo
from app.models.base_model import db


# 进入后台的管理页面之前首先要使用admin账户登录
@admin_blueprint.route('/admin', methods=['GET', 'POST'])
def login():
    # 创建一个登录表单，使用command + B定位到声明的文件
    form = LoginForm(request.form)
    # 用户浏览器第一次请求URL时使用的是GET方法，将html页面返回
    if request.method == 'GET':
        return render_template('admin/login.html', form=form)  # 将form传给html网页
    # 当用户填写完表单信息，点击"登录"按钮时，使用POST方法将表单传回后端，这时应该接收并验证表单信息
    else:
        # 查询用户进行验证
        admin_user = Admin.query.filter_by(username=form.username.data).first()
        # 验证成功，跳转到管理页面
        if admin_user and admin_user.check_password(form.password.data):
            return redirect(url_for('admin.admin_manage'))
        # 验证失败
        else:
            flash('管理员信息错误')  # 需要配合html中的相应script才能实现效果
            return redirect(url_for('admin.login'))


# 后台管理页面
@admin_blueprint.route('/admin/manage')
def admin_manage():
    # 创建一个添加管理员的表单
    form = AddAdminForm(request.form)
    # 获取所有的admin用户，这里用到了data中定义的相应class，并且在进行实例化时会自动调用该class中的__init__方法
    admin_users = AdminInfo(Admin.query.all()).admin_users
    return render_template('admin/manage.html', form=form, users=admin_users)


# 添加管理员账户
# 在管理页面中填写好表单后点击"提交"按钮跳转到当前URL（POST方法）
@admin_blueprint.route('/admin/add', methods=['POST'])
def admin_add():
    # 从request中获取用户提交的表单
    form = AddAdminForm(request.form)
    admin_users = AdminInfo(Admin.query.all()).admin_users
    # 验证表单并添加管理员用户到数据库中
    if request.method == 'POST' and form.validate():
        with db.auto_commit():
            new_admin_user = Admin()
            new_admin_user.username = form.username.data
            new_admin_user.role = 'super'
            new_admin_user.password = form.password.data
            db.session.add(new_admin_user)
            return redirect(url_for('admin.admin_manage'))
    else:
        if not form.validate():
            flash('请输入相同密码')
        return render_template('admin/manage.html', form=form, users=admin_users)


# 修改管理员信息
# URL中会携带管理员的用户名，根据这个用户名进行信息的修改
@admin_blueprint.route('/admin/change/<username>', methods=['GET'])
def admin_change(username):
    # 删除管理员用户
    with db.auto_commit():
        admin_user = Admin.query.filter_by(username=username).first()
        db.session.delete(admin_user)
    return redirect(url_for('admin.admin_manage'))
