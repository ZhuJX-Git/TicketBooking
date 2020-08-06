from contextlib import contextmanager
from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy

__all__ = ['db', 'Base']  # 可以在其他的文件中直接引用db和Base的值


# 重写SQLAlchemy这个类，使用上下文管理器来实现数据库的自动提交和回滚
# 详见：https://blog.csdn.net/weixin_42359464/article/details/80742387
class SQLAlchemy(_SQLAlchemy):
    @contextmanager  # 上下文管理器（装饰器）
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as exception:
            self.session.rollback()
            raise exception


db = SQLAlchemy()  # 创建一个可交互的数据库实例，在此项目中的所有其他地方如果需要与数据库进行操作时都使用此实例


# 定义一个基类，作为所有需要通过ORM建立的实体类的父类
class Base(db.Model):
    __abstract__ = True  # 设置为abstract后，在执行ORM时当前类不会被映射为数据库中的表
