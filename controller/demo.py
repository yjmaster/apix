from flask import request, render_template, redirect, url_for

from . import kpf

# userDb = UserDb()

@kpf.route('/demo', methods=['GET','POST'])
def demo():
    if request.method == 'GET':
        return render_template('demo.html')

# @kpf.route('/title', methods=['POST'])
# def title():
#     data = request.get_json()
#     print(data)
    
    #     print(data)
        # userResult = userDb.find_user(data, 'check')
        # return userResult
    
# @yjmedia.route('/login', methods=['GET','POST'])
# def login():
#     if request.method == 'GET':
#         token = request.cookies.get('access_token')
#         if token is None :
#             return render_template('login.html', site="yjmedia")
#         else:
#             userResult = userDb.decode_token(token, True)
#             if userResult['success']:
#                 return redirect('/')
#             else: 
#                 msg = userResult['message']
#                 return render_template('login.html', site="yjmedia", msg=msg)
        
#     elif request.method == 'POST':
#         data = request.get_json()
#         userResult = userDb.find_user(data, 'check')
#         return userResult

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

