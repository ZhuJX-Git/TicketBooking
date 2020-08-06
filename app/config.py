# 配置数据库
SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://jiaxuzhu:Zjx19970418@127.0.0.1:5432/ticketbooking'
# 对于flask来说，其中自带的session管理需要依靠secret_key来实现，因此必须手动定义一个secret_key
SECRET_KEY = '1234567890'
SQLALCHEMY_TRACK_MODIFICATIONS = True
TEMPLATES_AUTO_RELOAD = True
