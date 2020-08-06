from wtforms import Form, StringField, PasswordField
from wtforms.validators import DataRequired, EqualTo


class AddAdminForm(Form):
    username = StringField('管理员用户名', validators=[DataRequired()])
    password = PasswordField('管理员密码', validators=[DataRequired(), EqualTo('repeat_password')])
    repeat_password = PasswordField('重复密码', validators=[DataRequired()])
