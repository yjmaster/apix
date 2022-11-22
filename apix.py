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

# ### GPT API ###
# from extractor.extractor import Extractor
# from extractor.cbs import CBS
# from extractor.asiatimes import AsiaTimes

# ### NEWS API ###
# from news.news import News

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
# api.add_namespace(CBS, '/cbs')
# api.add_namespace(AsiaTimes, '/asiatimes')

# api.add_namespace(Extractor, '/extractor')
# api.add_namespace(News, '/news')

if __name__ == "__main__":
    # app.run(debug=True, host='0.0.0.0', port=10001) #실제 운영 API 
    app.run(debug=True, port=5000) # 테스트 API
