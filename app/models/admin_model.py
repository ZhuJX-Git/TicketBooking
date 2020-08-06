from app.models.base_model import Base
from sqlalchemy import Column, Integer, String
from werkzeug.security import generate_password_hash, check_password_hash


# 后台管理用户类
# 结构同User类似，具体说明详见user_model.py
class Admin(Base):
    __tablename__ = 'admin'
    id = Column(Integer, primary_key=True)
    role = Column(String(50), nullable=False, default='super')
    username = Column(String(50), nullable=False)
    _password = Column(String(128), nullable=False)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw_pwd):
        self._password = generate_password_hash(raw_pwd)

    def check_password(self, raw_pwd):
        return check_password_hash(self._password, raw_pwd)
