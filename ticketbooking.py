# 项目的启动入口
from app import create_app

# create_app位于app/__init__.py文件中
app = create_app()
# 开启热修改
app.jinja_env.auto_reload = True
if __name__ == '__main__':
    app.run(host='localhost', debug=app.config['DEBUG'], port=5000)
