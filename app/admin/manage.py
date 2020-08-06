from . import admin_blueprint
from flask import render_template, redirect, request, url_for, flash
from app.forms.admin_manage_form import AddCompanyForm, AddTicketForm
from app.models.ticket_model import Company, Ticket
from app.models.order_model import Order
from app.data.admin_data import CompanyInfo, OrderInfo
from app.models.base_model import db


# 航空公司管理页面
@admin_blueprint.route('/admin/company', methods=['GET', 'POST'])
def company():
    # 创建一个添加公司信息的表单
    form = AddCompanyForm(request.form)
    # 获取数据库中所有公司的信息
    companies = CompanyInfo(Company.query.all()).companies
    if request.method == 'GET':
        return render_template('admin/manage_company.html', form=form, companies=companies)
    else:
        # 验证表单
        if not form.validate():
            flash('请填写完整信息')
        else:
            # 更新数据库
            with db.auto_commit():
                new_company = Company()
                new_company.english_name = form.english_name.data
                new_company.company_name = form.chinese_name.data
                db.session.add(new_company)
        return redirect(url_for('admin.company'))


# 删除航空公司（URL中会携带公司的英文名称）
@admin_blueprint.route('/admin/company/<english_name>', methods=['GET', 'POST'])
def company_change(english_name):
    # 根据英文名称得到相应的公司
    _company = Company.query.filter_by(english_name=english_name).first()
    # 如果当前系统中有存储该航空公司的机票的话则无法删除该公司
    if Ticket.query.filter_by(company_name=_company.company_name).first():
        flash("存在此公司的机票，不能删除")
    # 成功删除
    else:
        with db.auto_commit():
            db.session.delete(_company)
    return redirect(url_for('admin.company'))


# 添加航班信息
@admin_blueprint.route('/admin/ticket', methods=['GET', 'POST'])
def ticket():
    form = AddTicketForm(request.form)
    if request.method == 'GET':
        return render_template('admin/manage_ticket.html', form=form)
    else:
        # 从表单中获取信息创建机票
        with db.auto_commit():
            new_ticket = Ticket()
            new_ticket.one_or_round = form.one_or_round.data
            new_ticket.name = form.name.data
            new_ticket.company_name = form.company_name.data
            new_ticket.depart_city = form.depart_city.data
            new_ticket.depart_airport = form.depart_airport.data
            new_ticket.arrive_city = form.arrive_city.data
            new_ticket.arrive_airport = form.arrive_airport.data
            new_ticket.depart_date = form.depart_date.raw_data[0]
            new_ticket.depart_time = form.depart_time.data
            new_ticket.arrive_date = form.arrive_date.raw_data[0]
            new_ticket.arrive_time = form.arrive_time.data
            new_ticket.return_date = form.return_date.raw_data[0]
            new_ticket.return_time = form.return_time.data
            new_ticket.economy_class_price = form.economy_class_price.data
            new_ticket.economy_class_num = form.economy_class_num.data
            new_ticket.business_class_price = form.business_class_price.data
            new_ticket.business_class_num = form.business_class_num.data
            new_ticket.first_class_price = form.first_class_price.data
            new_ticket.first_class_num = form.first_class_num.data
            db.session.add(new_ticket)
        return render_template('admin/manage_ticket.html', form=form)


# 查询订单
@admin_blueprint.route('/admin/order', methods=['GET', 'POST'])
def order():
    if request.method == 'GET':
        # 得到所有的订单信息
        orders = OrderInfo(Order.query.all()).orders
        return render_template('admin/manage_order.html', orders=orders)
    # 当点击"确认"按钮时，会以POST形式提交表单，并且会包含订单的id，修改相应订单的状态
    else:
        order_id = request.args.get('order_id')
        _order = Order.query.filter_by(order_id=order_id).first()
        with db.auto_commit():
            _order.status = '已处理'
            db.session.add(_order)
        return redirect(url_for('admin.order'))


# 删除已完成的订单
@admin_blueprint.route('/admin/delete_order', methods=['POST'])
def order_delete():
    order_id = request.args.get('order_id')
    with db.auto_commit():
        _order = Order.query.filter_by(order_id=order_id).first()
        db.session.delete(_order)
    return redirect(url_for('admin.order'))
