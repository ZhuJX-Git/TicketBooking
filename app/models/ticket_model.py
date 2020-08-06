from app.models.base_model import Base
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref


# 定义航空公司类
class Company(Base):
    __tablename__ = 'company'
    company_name = Column(String(50), primary_key=True, nullable=False)
    id = Column(Integer, autoincrement=True)
    english_name = Column(String(50), unique=True, nullable=False)  # 英文简称


# 定义机票类
class Ticket(Base):
    __tablename__ = 'ticket'
    id = Column(Integer, primary_key=True, autoincrement=True)
    one_or_round = Column(String(10), nullable=False)  # 单程或往返
    name = Column(String(50), unique=True)
    company_name = Column(String(50), ForeignKey('company.company_name'), nullable=False)  # 与company表建立外键联系
    # 出发城市&机场
    depart_city = Column(String(50), nullable=False)
    depart_airport = Column(String(50), nullable=False)
    # 到达城市&机场
    arrive_city = Column(String(50), nullable=False)
    arrive_airport = Column(String(50), nullable=False)
    # 出发日期&时间
    depart_date = Column(String(50), nullable=False)
    depart_time = Column(String(50), nullable=False)
    # 到达日期&时间
    arrive_date = Column(String(50), nullable=False)
    arrive_time = Column(String(50), nullable=False)
    # 如果是往返的话还有返程的日期&时间，单程票的话为null
    return_date = Column(String(50))
    return_time = Column(String(50))
    # 不同等级机票的价格和余量
    # eco和main都有，但是头等舱不必须
    economy_class_price = Column(Integer, nullable=False)
    economy_class_num = Column(Integer, nullable=False)
    business_class_price = Column(Integer, nullable=False)
    business_class_num = Column(Integer, nullable=False)
    first_class_price = Column(Integer)
    first_class_num = Column(Integer)
    # 和company建立联系，即可以通过ticket.company得到提供这个票的公司，也可以通过company.ticket得到这个公司提供的所有机票
    company = relationship('Company', backref=backref('ticket_of_company'))
