from wtforms import Form, SelectField, RadioField, DateField, StringField, IntegerField
from wtforms.validators import DataRequired
from app.models.ticket_model import Ticket


# 定义辅助方法查询城市
def search_cities(param):
    raw_cities = Ticket.query.with_entities(Ticket.depart_city).distinct().all() if param == 0 \
        else Ticket.query.with_entities(Ticket.arrive_city).distinct().all()
    for index in range(0, len(raw_cities)):
        raw_cities[index] = raw_cities[index] + raw_cities[index]
    return raw_cities


# 机票查询表单
class SearchForm(Form):
    # 首先从数据库中查询所有的城市
    # 定义表单中的条目
    one_or_round = RadioField('航班类型', choices=[('单程', '单程'), ('往返', '往返')])
    depart_city = SelectField('出发城市', validators=[DataRequired()])
    arrive_city = SelectField('到达城市', validators=[DataRequired()])
    depart_date = DateField(label='出发日期', format='%m/%d/%y', validators=[DataRequired()])
    return_date = DateField(label='返程日期', format='%m/%d/%y')

    # 重写构造方法
    def __init__(self, *args, **kwargs):
        # 由于这个自定义的表单类继承了Form类，因此首先调用父类的构造方法
        super().__init__(*args, **kwargs)
        # 然后查询所有的出发城市和到达城市
        self.depart_city.choices = search_cities(0)
        self.arrive_city.choices = search_cities(1)


# 预定机票表单
class OrderForm(Form):
    order_id = StringField('订单号', validators=[DataRequired()])
    route = StringField('行程', validators=[DataRequired()])
    depart_time = StringField('起飞时间', validators=[DataRequired()])
    ticket_type = SelectField('机票类型', choices=[('经济舱', '经济舱'), ('商务舱', '商务舱'), ('头等舱', '头等舱')])
    name = StringField('乘客姓名', validators=[DataRequired()])

    # 重写构造方法
    def __init__(self, *args, **kwargs):
        # 由于这个自定义的表单类继承了Form类，因此首先调用父类的构造方法
        super().__init__(*args, **kwargs)
