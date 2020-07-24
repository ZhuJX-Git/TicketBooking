# 定义用户进行登录或注册等身份验证时需要的表单，可以方便的定义一些验证机制，这些表单可以直接被传入到html中
from wtforms import Form, StringField, PasswordField
from wtforms.validators import DataRequired, EqualTo, ValidationError
from app.models import User


# 用户注册的表单
class RegisterForm(Form):
    username = StringField('用户名', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired(), EqualTo('repeatPassword')])
    repeatPassword = PasswordField('重复密码', validators=[DataRequired()])


# 用户登录的表单
class LoginForm(Form):
    username = StringField('用户名', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired(message='密码不能为空，请输入密码')])

    def verifyUsername(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已存在，请更换用户名')
