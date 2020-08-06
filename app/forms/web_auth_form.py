from wtforms import Form, StringField, PasswordField
from wtforms.validators import DataRequired, EqualTo, ValidationError
from app.models.user_model import User


# 所有自定义表单需要继承wtforms中自带的Form类
# 定义时的validator中为用户在实际填写时需要满足的规则

# 用户注册表单
class RegisterForm(Form):
    username = StringField('用户名', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired(), EqualTo('repeat_password')])
    repeat_password = PasswordField('重复密码', validators=[DataRequired()])


# 用户登录表单（同时也是admin用户的登录表单）
class LoginForm(Form):
    username = StringField('用户名', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired(message='请输入密码')])


# 用户信息表单
class InfoForm(Form):
    password = PasswordField('新密码', validators=[DataRequired(), EqualTo('repeat_password')])
    repeat_password = PasswordField('重复新密码', validators=[DataRequired()])
