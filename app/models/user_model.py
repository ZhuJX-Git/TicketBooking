from app.models.base_model import Base, db
from sqlalchemy import Column, Integer, String
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from app import login_manager


# 定义用户类
# 关于UserMixin：用于配合flask-login协同实现用户登录管理的功能，要求需要进行管理的自定义用户类必须继承UserMixin
# 详见：https://flask-login.readthedocs.io/en/latest/
class User(UserMixin, Base):
    __tablename__ = 'user'
    id = Column(Integer, autoincrement=True, primary_key=True)
    username = Column(String(50), nullable=False, unique=True)
    _password = Column('password', String(128), nullable=False)  # 下划线命名的属性是私有变量（只是作为一个警告，实际上python中并无真正的私有变量）

    # 由于python中没有真正的私有变量，因此需要通过手动定义getter和setter的方法来实现password的"私有化"
    # 关于property装饰器的详解见：https://www.tutorialsteacher.com/python/property-decorator
    # 使用property装饰，此方法会作为password属性的getter
    @property
    def password(self):
        return self._password

    # 使用此装饰器后，此方法会作为password属性的setter
    # 此处的参数raw_pwd相当于用户输入的密码，但是注意并不是直接在数据库中存储明文密码，
    # 而是通过python中自带的一个计算hash的函数计算密码的校验值，从而保证数据存储的安全性
    @password.setter
    def password(self, raw_pwd):
        self._password = generate_password_hash(raw_pwd)

    # 定义一些内部方法，用于后续简便的执行用户的相关操作

    # 检查密码是否正确
    def check_password(self, raw_pwd):
        return check_password_hash(self._password, raw_pwd)


# 提供一个callback函数，具体的目的是便于flask_login进行session管理
# 详见：https://flask-login.readthedocs.io/en/latest/
@login_manager.user_loader
def get_user(uid):
    return User.query.get(int(uid))