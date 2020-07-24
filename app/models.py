# 包含所有需要进行ORM操作的类，所有的类需要继承db.Model才能被进行映射
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref

db = SQLAlchemy()


# 后台的admin用户
class Admin(db.Model):
    __tablename__ = 'admin'
    id = Column(Integer, primary_key=True)
    role = Column(String(50), nullable=False, default='super')
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)


# 用户类
class User(db.Model):
    __tablename__ = 'user'
    username = Column(String(50), primary_key=True, nullable=False) # 用户名
    password = Column(String(50), nullable=False) # 密码


# 航空公司类
class Company(db.Model):
    __tablename__ = 'company'
    id = Column(Integer, autoincrement=True) # id
    companyName = Column(String(50), primary_key=True, nullable=False) # 航司名称
    engAbbr = Column(String(50), nullable=False) # 英文简写


# 机票类
class Ticket(db.Model):
    __tablename__ = 'ticket'
    id = Column(Integer, primary_key=True) # 机票编码
    oneOrRound = Column(String(50), nullable=False) # 单程或往返
    name = Column(String(50), unique=True) ###
    companyName = Column(String(50), ForeignKey('company.companyName'), nullable=False) # 提供机票的航司，建立外键关系
    departCity = Column(String(50), nullable=False) # 出发地
    arriveCity = Column(String(50), nullable=False) # 到达地
    departAirport = Column(String(50), nullable=False) # 出发机场
    arriveAirport = Column(String(50), nullable=False) # 到达机场
    # 出发日期&时间
    departDate = Column(String(50))
    departTime = Column(String(50))
    # 到达日期&时间
    arriveDate = Column(String(50))
    arriveTime = Column(String(50))
    # 返程日期&时间
    returnDate = Column(String(50))
    returnTime = Column(String(50))
    # 头等舱机票余量及价格
    firstClassNum = Column(Integer)
    firstClassPrice = Column(Integer)
    # 商务舱机票余量及价格
    businessClassNum = Column(Integer)
    businessClassPrice = Column(Integer)
    # 经济舱机票余量及价格
    economyClassNum = Column(Integer, nullable=False)
    economyClassPrice = Column(Integer, nullable=False)
    # 建立一对多关系，即一个航司可以提供多张机票
    company = relationship('Company', backref=backref('ticketOfCompany'))


# 订单类
class Order(db.Model):
    __tablename__ = 'order'
    id = Column(Integer, primary_key=True) # 订单编号
    username = Column(String, ForeignKey('user.username')) # 下订单的用户，建立外键关系
    ticketClass = Column(String(50), nullable=False) # 机票等级
    route = Column(String(50), nullable=False) # 飞行路线
    departTime = Column(String(50), nullable=False) # 起飞时间
    status = Column(String(50), nullable=False) # 订单状态：待执行 / 执行完成
    # 与用户建立一对多的关系
    user = relationship('User', backref=backref('userOfTicket'))
