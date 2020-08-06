from flask import Flask
from flask_login import LoginManager
from app.models.base_model import db, Base
from app.models.admin_model import Admin
from app.web import web_blueprint
from app.admin import admin_blueprint


# 首先需要创建一个login manager，作用在于和flask-login共同实现flask项目中的用户会话管理
# 详见：http://www.pythondoc.com/flask-login/
login_manager = LoginManager()


# 将创建app的过程封装在此方法中
# 此方法中的所有import不能和上面的import放在一起，
# 准确来说是不能放在login_manager的创建之前，否则会造成循环引用，引发编译错误
def create_app():
    app = Flask(__name__)  # 新建一个Flask应用
    app.config.from_object('app.config')  # 使用自定义文件config.py中的项目配置
    # 注册blueprint
    # blueprint的作用在于实现模块间的解耦，详见：http://docs.jinkan.org/docs/flask/blueprints.html
    # 在web和admin两个package中的__init__文件中定义了两个blueprint实例
    from app.web import authentication, home, search
    from app.admin import authentication, manage
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(web_blueprint)
    # 把app注册到数据库实例上，这个数据库实例db在app/models/base.py中创建
    db.init_app(app)
    # 初始化LoginManager
    login_manager.init_app(app)
    # 对于某些页面来说，必须要先登录才能访问，因此在登录前访问的话会弹出一个警告框显示login_message
    # 然后会跳转到login_view规定的URL
    login_manager.login_view = 'web.login'  # web.login是指在app/web/authentication.py中定义的login()视图方法
    login_manager.login_message = '请先登录或注册'
    # 执行ORM
    from app.models import user_model, ticket_model, order_model, admin_model  # 只有这里import的文件中的类会被映射
    with app.app_context():
        db.create_all(app=app)
        # 在第一次启动项目时添加一个管理员用户
        # 只有管理员用户能够修改后台数据
        if not Admin.query.filter_by(username='admin').first():
            admin_user = Admin()
            admin_user.username = 'admin'
            admin_user.password = '123456'
            admin_user.role = 'super'
            with db.auto_commit():  # 这个auto_commit()是在app/models/base.py中自定义的
                db.session.add(admin_user)
    return app
