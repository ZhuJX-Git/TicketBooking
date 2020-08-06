from . import web_blueprint
from flask import render_template, request
from app.forms.web_search_form import SearchForm


# 前台首页
@web_blueprint.route('/')
def home():
    form = SearchForm(request.form)
    # 设定预设值
    form.one_or_round.default = '往返'
    form.process()
    return render_template('web/home.html', form=form)
