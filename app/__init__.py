from flask import Flask
from app.models import db
from app.web import web
from app.admin import admin


# 配置程序
def createApp():
    app = Flask(__name__)
    # 热修改
    app.jinja_env.auto_reload = True
    app.config.from_object('app.config') # 导入config.py中的配置
    # 注册蓝图
    app.register_blueprint(web)
    app.register_blueprint(admin)
    db.init_app(app) # 注册数据库
    # 只需要在第一次运行程序时执行ORM，后续可注释下面两行
    with app.app_context():
        db.create_all(app=app)
    return app
