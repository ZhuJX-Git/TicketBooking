# 在这个文件中定义的类都是用来处理数据的，即把数据库查询出的原生数据进行提取加工
# 将这部分功能分离出来的目的在于提高可复用性
from app.models.user_model import User


# 定义一个类用来汇总所有的admin user信息，raw_data是在数据库查询后得到的所有的admin，只需要其中的用户名和类型
class AdminInfo:
    def __init__(self, raw_data):
        self.admin_users = []
        for user in raw_data:
            info = {'username': user.username, 'role': user.role}
            self.admin_users.append(info)


# 定义一个类来汇总所有的航空公司信息
class CompanyInfo:
    def __init__(self, raw_data):
        self.companies = []
        for company in raw_data:
            info = {'english_name': company.english_name, 'chinese_name': company.company_name}
            self.companies.append(info)


# 定义一个类来获取所有的订单信息
class OrderInfo:
    def __init__(self, raw_data):
        self.orders = []
        for order in raw_data:
            user_id = order.user_id
            user = User.query.filter_by(id=user_id).first()
            info = {'order_id': order.order_id, 'username': user.username, 'ticket_type': order.ticket_type,
                    'route': order.route, 'depart_time': order.depart_time, 'status': order.status,
                    }
            self.orders.append(info)
