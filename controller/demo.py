import string
from flask import request, render_template, redirect, url_for
from auth.kpf.db import KpfDb
from auth.kpf.user import KpfUser
from auth.bflysoft.db import BflysoftDb

from . import kpf
# from utils.encryption import AESCipher

kpfDb = KpfDb()
kpfUser = KpfUser()
bflysoftDb = BflysoftDb()

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
        if key:
            isKpfUser = kpfUser.find_key(key)
            isBflyUser = bflysoftDb.authentication(key)
            if isKpfUser["success"] or isBflyUser["success"]:
                return render_template(
                    'log.html', accessType="key", key=key)
            else:
                return render_template('login.html')
        else:
            if token:
                return render_template('log.html', accessType = "token")
            else:
                return render_template('login.html')
    elif request.method == 'POST':
        data = request.get_json()
        return kpfDb.get_log(data)

# @kpf.route('/test', methods=['GET','POST'])
# def test():
#     if request.method == 'GET':
#         return render_template('test.html')

#     elif request.method == 'POST':
#         res = {"success": True}
#         client_id = request.headers['Authorization']
#         isValidkey = kpfUser.find_key(client_id)
#         if isValidkey["success"]:
#             # secret_key = string.ascii_letters
#             secret_key = "test"
#             encryptKey = AESCipher.encrypt(client_id, secret_key).decode('utf-8')
#             res["encrypt_key"] = encryptKey
#             res["secret_key"] = secret_key
#             print(AESCipher.encrypt("6CF283C1-4708-5BDD-F4D0-B02C8DF03D7E", "test"))
#             return res