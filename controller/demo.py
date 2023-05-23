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
        # http://localhost:10001/log?key=6CF283C1-4708-5BDD-F4D0-B02C8DF03D7E
        key = request.args.get('key', type=str)
        token = request.cookies.get('access_token')
        if token is None :
            if key is None:
                return render_template('login.html')
            else:
                isValidkey = kpfUser.find_key(key)
                if isValidkey["success"]:
                    return render_template('log.html', accessType = "key")
                else:
                    return render_template('login.html')
        else:
            return render_template('log.html', accessType = "token")
    elif request.method == 'POST':
        data = request.get_json()
        return kpfDb.get_log(data)