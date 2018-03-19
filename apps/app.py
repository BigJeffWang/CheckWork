# coding: utf8
# @Author  : WangYe
# @contact : bigjeffwang@163.com
# @Time    : 2018/3/8 上午11:13
# @File    : app

import os
from flask import Flask
from apps.extensions import mako
app = Flask(__name__)


instance_path = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__, instance_path=instance_path, template_folder='templates', static_folder='static')
# app.config.from_object()
# app.config['DEBUG'] = False
mako.init_app(app)
