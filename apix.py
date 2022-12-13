# -*- coding: utf-8 -*-
import configparser
from flask import Flask, request, redirect, url_for, render_template
from flask_restx import Resource, Api, apidoc
from flask_cors import CORS, cross_origin

from controller import kpf

# from auth.user import Auth
# from auth.db.userDb import UserDb

# userDb = UserDb()

### sample ###
from todo.todo import Todo

### kobart ###
from modelAI.kobart import Kobart

app = Flask(__name__)
CORS(app)
CORS(app, resources={r'*': {'origins': '*'}})

api = Api(
    app,
    version='0.1',
    title="KPF API Server",
    description="KPF API Server! (http://118.67.150.92:10001)",
    terms_url="/",
    contact="skc@yjmedia.com",
    license="MIT"
)
app.register_blueprint(kpf, url_prefix='/')

# @api.documentation
# def custom_ui():
#     #authCheck = request.headers.get('Authorization')
#     token = request.cookies.get('access_token')
#     print("token : ", token)
#     if token is None:
#         return redirect(url_for('kpf.login'))
#     else :
#         return apidoc.ui_for(api)
    

# api.add_namespace(Todo, '/todo')
# api.add_namespace(Auth, '/auth')

api.add_namespace(Kobart, '/v1')

config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8')
kpfdb = config['kpf']

if __name__ == "__main__":
    app.run(host=kpfdb['host'], port=kpfdb['port']) #실제 운영 API 
    # app.run(debug=True, port=kpfdb['port']) # 테스트 API
