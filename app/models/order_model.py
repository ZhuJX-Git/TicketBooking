from app.models.base_model import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref


# 订单类
class Order(Base):
    __tablename__ = 'order'
    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))  # 下订单的用户id
    order_id = Column(String(50), nullable=False)
    ticket_type = Column(String(50), nullable=False)  # 机票的等级
    route = Column(String(50), nullable=False)  # 路线
    depart_time = Column(String(50), nullable=False)  # 行程出发时间
    status = Column(String(50), nullable=False)  # 订单完成状态（"处理中"或"已完成"）
    # 和user建立联系，即可以通过order.user得到下订单的用户，也可以通过user.order得到这个用户的所有订单
    user = relationship('User', backref=backref('user_of_order'))

