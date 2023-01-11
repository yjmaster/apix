from flask import request, render_template, redirect, url_for
from auth.db import YJDb
from auth.user import YJUser
from . import yjmedia

yjDb = YJDb()
yjUser = YJUser()

@yjmedia.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        token = request.cookies.get('access_token')
        if token is None :
            return render_template('login.html', site="yjmedia")
        else:
            return redirect('/')

    elif request.method == 'POST':
        data = request.get_json()
        return yjUser.find_user(data)

@yjmedia.route('/', methods=['GET'])
def demo():
    token = request.cookies.get('access_token')
    if token is None :
        return render_template('login.html')
    else:
        return redirect('/')
    
# @yjmedia.route('/', methods=['GET','POST'])
# def main():
#     if request.method == 'GET':
#         token = request.cookies.get('access_token')
#         if token is None :
#             return redirect(url_for('yjmedia.login'))
#         else:
#             userResult = userDb.decode_token(token, True)
#             if userResult['success']:
#                 return render_template('main.html', loginTitle="양재미디어")
#             else:
#                 msg = userResult['message']
#                 return render_template('login.html', site="yjmedia", msg=msg)
            
# @kpf.route('/login', methods=['GET','POST'])
# def login():
#     if request.method == 'GET':
#         token = request.cookies.get('access_token')
#         if token is None :
#             return render_template('login.html', site="kpf")
#         else:
#             userResult = userDb.decode_token(token, True)
#             if userResult['success']:
#                 return redirect(url_for('kpf.main'))
#             else: 
#                 msg = userResult['message']
#                 return render_template('login.html', site="kpf", msg=msg)

#     elif request.method == 'POST':
#         data = request.get_json()
#         userResult = userDb.find_user(data, 'check')
#         return userResult
    
# @kpf.route('/', methods=['GET','POST'])
# def main():
#     if request.method == 'GET':
#         token = request.cookies.get('access_token')
#         if token is None :
#             return redirect(url_for('kpf.login'))
#         else:
#             userResult = userDb.decode_token(token, True)
#             if userResult['success']:
#                 return render_template('main.html', loginTitle="한국언론진흥재단")
#             else:
#                 msg = userResult['message']
#                 return render_template('login.html', site="kpf", msg=msg)

