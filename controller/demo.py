from flask import request, render_template, redirect, url_for
from auth.kpf.db import KpfDb
from auth.kpf.user import KpfUser
from . import kpf

kpfDb = KpfDb()
kpfUser = KpfUser()

@kpf.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        token = request.cookies.get('access_token')
        if token is None :
            return render_template('login.html')
        else:
            return render_template('demo.html')

    elif request.method == 'POST':
        data = request.get_json()
        return kpfUser.find_user(data)

@kpf.route('/demo', methods=['GET'])
def demo():
    token = request.cookies.get('access_token')
    if token is None :
        return render_template('login.html')
    else:
        return render_template('demo.html')

@kpf.route('/options', methods=['POST'])
def options():
    data = request.get_json()
    return kpfDb.get_options(data)

@kpf.route('/log', methods=['GET','POST'])
def log():
    if request.method == 'GET':
        token = request.cookies.get('access_token')
        if token is None :
            return render_template('login.html')
        else:
            return render_template('log.html')
    elif request.method == 'POST':
        data = request.get_json()
        return kpfDb.get_log(data)