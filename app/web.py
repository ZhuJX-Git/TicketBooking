# web作为一个blueprint，包含所有与前台网页相关的url映射
from flask import Blueprint, request, render_template, flash, redirect, url_for
from app.forms.authentication import RegisterForm, LoginForm
from app.models import db, User

web = Blueprint('web', __name__) # 生成一个蓝图（蓝图的使用意义在于模块之间的解耦）


@web.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form) # 创建一个空白的注册表单
    # 当用户进入这个url时，请求的方式是GET，这时候应该传给他这个空白的表单；
    # 但是当用户填写完毕，点击"注册"按钮后，请求的还是当前的url，但是请求方式已经变成了POST，因为要提交表单
    # 因此在POST情况下说明需要对用户填写的信息进行验证，成功的话需要更新数据库
    if request.method == 'GET':
        return render_template('Foreground/register.html', form=form)
    if request.method == 'POST':
        newUser = User()
        newUser.username = form.data['username']
        newUser.password = form.data['password']
        # 如果用户名已经存在的话则调用flask内部的flash方法给出一个警告，此外还需要在html中编写相应的javascript
        if User.query.filter_by(username=newUser.username).first():
            flash('用户名已存在，请更换')
            return redirect(url_for('web.register'))
        # 如果新建的用户合法则添加到数据库中，并重定向到登录界面
        else:
            db.session.add(newUser)
            db.session.commit()
            return redirect(url_for('web.login'))


@web.route('/login', methods=['GET', 'POST'])
def login():


    return 'hello world'
