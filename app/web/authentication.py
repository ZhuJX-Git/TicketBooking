from . import web_blueprint
from flask import request, render_template, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from app.forms.web_auth_form import RegisterForm, LoginForm, InfoForm
from app.models.user_model import User
from app.models.base_model import db


# 注册的视图方法
@web_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    # 首先创建一个空白的注册表单
    form = RegisterForm(request.form)
    # 当客户端浏览器请求此URL时的方法是GET，这时候将包含表单的html文件返回
    if request.method == 'GET':
        return render_template('web/register.html', form=form)
    else:
        # 当用户填写好表单，点击"注册"按钮后，此时的方法是POST，这时应该获取表单内容
        new_user = User()
        new_user.username = form.username.data
        new_user.password = form.password.data
        # 然后判断信息合法性并提交数据库
        if User.query.filter_by(username=new_user.username).first():
            flash('用户名已存在，请更换')  # 通过flask自带的flash给出一个警告，在html中编写相应的script实现
            return redirect(url_for('web.register'))
        else:
            with db.auto_commit():
                db.session.add(new_user)
            return redirect(url_for('web.login'))


# 登录的视图方法
@web_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    # 创建一个空白的登录表单
    form = LoginForm(request.form)
    # 原理同上面的注册视图
    if request.method == 'GET':
        return render_template('web/login.html', form=form)
    else:
        user = User.query.filter_by(username=form.username.data).first()
        # 如果用户名存在，并且调用User中的判断密码的方法验证无误才算登录成功
        if user and user.check_password(form.password.data):
            login_user(user, remember=True)  # 调用flask_login中的方法实现登录，当前的用户信息会存放在session中
            next_arg = request.args.get('next')
            if not next_arg:
                next_arg = url_for('web.info')
            return redirect(next_arg)
        else:
            flash('账号不存在或密码错误')
            return redirect(url_for('web.login'))


# 显示个人信息的视图
# 使用login_required装饰的方法要求首先登录才行，即44行的login_user方法必须要被执行
@web_blueprint.route('/info', methods=['GET', 'POST'])
@login_required
def info():
    form = InfoForm(request.form)
    if request.method == 'GET':
        return render_template('web/my_info.html', form=form)
    else:
        if not form.validate():
            flash('输入信息有误')
        else:
            # 修改数据库中的用户密码
            user = User.query.filter_by(id=current_user.id).first()
            with db.auto_commit():
                user.password = form.password.data
                db.session.add(user)  # 此处使用的虽然是add方法，但是会自动进行判断，如果当前对象已经存在，则执行更新操作，否则执行真正的add操作
        return redirect(url_for('web.info'))


# 登出
@web_blueprint.route('/logout')
@login_required
def logout():
    logout_user()  # 当前的用户信息会从session中删除，此时无法再执行login_required装饰的方法
    return redirect(url_for('web.home'))
