from wtforms import Form, StringField, IntegerField, RadioField, SelectField, DateField, TimeField
from wtforms.validators import DataRequired
from app.models.ticket_model import Company


# 添加新的航空公司的表单
class AddCompanyForm(Form):
    english_name = StringField('英文名称', validators=[DataRequired()])
    chinese_name = StringField('中文名称', validators=[DataRequired()])


# 添加机票信息的表单
class AddTicketForm(Form):
    one_or_round = RadioField('航班类型', choices=[('单程', '单程'), ('往返', '往返')])
    name = StringField('航班名称', validators=[DataRequired()])
    company_name = SelectField(label='航空公司', validators=[DataRequired("请选择航空公司")])  # SelectField中的内容就是在下面的构造方法被调用的时候创建的
    depart_city = StringField('出发城市', validators=[DataRequired()])
    arrive_city = StringField('到达城市', validators=[DataRequired()])
    depart_airport = StringField('出发机场', validators=[DataRequired()])
    arrive_airport = StringField('到达机场', validators=[DataRequired()])
    depart_date = DateField(label='出发日期', format='%m/%d/%y', validators=[DataRequired()])
    depart_time = TimeField(label='出发时间', validators=[DataRequired()])
    arrive_date = DateField(label='到达日期', format='%m/%d/%y', validators=[DataRequired()])
    arrive_time = TimeField(label='到达时间', validators=[DataRequired()])
    return_date = DateField(label='返程日期', format='%m/%d/%y')
    return_time = TimeField(label='返程时间')
    economy_class_price = IntegerField('经济舱价格', validators=[DataRequired()])
    economy_class_num = IntegerField('经济舱数量', validators=[DataRequired()])
    business_class_price = IntegerField('商务舱价格', validators=[DataRequired()])
    business_class_num = IntegerField('商务舱数量', validators=[DataRequired()])
    first_class_price = IntegerField('头等舱价格')
    first_class_num = IntegerField('头等舱数量')

    # 重写构造方法
    def __init__(self, *args, **kwargs):
        # 由于这个自定义的表单类继承了Form类，因此首先调用父类的构造方法
        super().__init__(*args, **kwargs)
        # 然后从数据库中读取所有的company信息
        self.company_name.choices = [(company.company_name, company.company_name) for company in Company.query.all()]
