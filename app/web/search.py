from . import web_blueprint
from flask import render_template, request, redirect, url_for
from app.forms.web_search_form import SearchForm, OrderForm
from app.models.ticket_model import Ticket
from app.data.web_data import TicketInfo, OrderInfo
from datetime import datetime
from app.models.base_model import db
from app.models.user_model import User
from app.models.order_model import Order
from flask_login import current_user, login_required


# 查询机票
@web_blueprint.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm(request.form)
    if request.method == 'GET':
        form.one_or_round.default = '往返'
        form.process()
        return render_template('web/search.html', form=form, tickets=[])
    else:
        # 根据"单程"或"往返"执行不同的查询
        tickets = Ticket.query.filter_by(
            one_or_round='单程', depart_date=form.depart_date.raw_data[0],
            depart_city=form.depart_city.data, arrive_city=form.arrive_city.data).all() \
            if form.one_or_round.data == '单程' \
            else \
            Ticket.query.filter_by(
            one_or_round='往返', depart_date=form.depart_date.raw_data[0],
            return_date=form.return_date.raw_data[0], depart_city=form.depart_city.data,
            arrive_city=form.arrive_city.data).all()
        tickets = TicketInfo(tickets).tickets
        return render_template('web/search.html', form=form, tickets=tickets)


# 预定机票（新增订单）
@web_blueprint.route('/order/<ticket_name>')
@login_required
def order(ticket_name):
    order_id = 'P' + datetime.now().strftime('%Y%m%d%H%M%S')
    ticket = Ticket.query.filter_by(name=ticket_name).first()
    form = OrderForm(request.form)
    form.order_id.default = order_id
    form.route.default = ticket.depart_city + '-' + ticket.arrive_city
    form.depart_time.default = ticket.depart_date + '-' + ticket.depart_time
    form.name.default = User.query.filter_by(id=current_user.id).first().username
    # 不是所有的舱位都可以选择
    if ticket.economy_class_num == 0:
        form.ticket_type.choices.remove(('经济舱', '经济舱'))
    if ticket.business_class_num == 0:
        form.ticket_type.choices.remove(('商务舱', '商务舱'))
    if not ticket.first_class_num or ticket.first_class_num == 0:
        form.ticket_type.choices.remove(('头等舱', '头等舱'))
    form.process()
    return render_template('web/order.html', form=form, ticket_name=ticket_name)


# 保存订单
@web_blueprint.route('/order/save/<ticket_name>', methods=['POST'])
@login_required
def save_order(ticket_name):
    # 得到提交的表单
    form = OrderForm(request.form)
    with db.auto_commit():
        # 第一步新增一个订单
        new_order = Order()
        new_order.order_id = form.order_id.data
        new_order.ticket_type = form.ticket_type.data
        new_order.route = form.route.data
        new_order.depart_time = form.depart_time.data
        new_order.user_id = current_user.id
        new_order.status = '正在处理'
        db.session.add(new_order)
        # 第二步修改机票的信息（舱位数量更新）
        cur_ticket = Ticket.query.filter_by(name=ticket_name).first()
        type_map = {'经济舱': 'economy_class_num', '商务舱': 'business_class_num', '头等舱': 'first_class_num'}
        ticket_type = type_map.get(new_order.ticket_type)
        old_num = getattr(cur_ticket, ticket_type)  # 首先获取旧的数量信息
        setattr(cur_ticket, ticket_type, old_num - 1)  # 然后进行更新
        db.session.add(cur_ticket)
    return redirect(url_for('web.my_order'))


# 显示当前用户的所有订单
@web_blueprint.route('/order/my')
@login_required
def my_order():
    # 首先获取当前用户的id
    user_id = current_user.id
    # 然后从数据库中查询订单
    orders = OrderInfo(Order.query.filter_by(user_id=user_id).all()).orders
    return render_template('web/my_order.html', orders=orders)
