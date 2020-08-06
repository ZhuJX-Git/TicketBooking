# 在这个文件中定义的类都是用来处理数据的，即把数据库查询出的原生数据进行提取加工
# 将这部分功能分离出来的目的在于提高可复用性


class TicketInfo:
    def __init__(self, raw_data):
        self.tickets = []
        for ticket in raw_data:
            if (ticket.first_class_num == 0 or not ticket.first_class_num)\
                    and ticket.business_class_num == 0 and ticket.economy_class_num == 0:
                continue
            info = {'name': ticket.name,
                    'company': ticket.company_name,
                    'depart_city': ticket.depart_city,
                    'arrive_city': ticket.arrive_city,
                    'depart_date_time': '起飞:' + ticket.depart_date + '-' + ticket.depart_time,
                    'arrive_date_time': '降落:' + ticket.arrive_date + '-' + ticket.arrive_time,
                    'return_date_time': ticket.return_date + ' ' + ticket.return_time,
                    'depart_airport': ticket.depart_airport,
                    'arrive_airport': ticket.arrive_airport,
                    'economy_class_price': '经济舱' + (str(ticket.economy_class_price) + '元')
                    if ticket.economy_class_num != 0 else '经济舱无票',
                    'business_class_price': '商务舱' + (str(ticket.business_class_price) + '元')
                    if ticket.business_class_num != 0 else '商务舱无票',
                    'first_class_price': '头等舱' + (str(ticket.business_class_price) + '元')
                    if ticket.first_class_num != 0 else '头等舱无票'
                    }
            self.tickets.append(info)


class OrderInfo:
    def __init__(self, raw_data):
        self.orders = []
        for order in raw_data:
            info = {'order_id': order.order_id,
                    'ticket_type': order.ticket_type,
                    'route': order.route,
                    'depart_time': order.depart_time,
                    'status': order.status
                    }
            self.orders.append(info)
