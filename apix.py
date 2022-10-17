from flask import Flask, request, redirect, url_for
from flask_restx import Resource, Api, apidoc
from flask_cors import CORS, cross_origin

from controller import yjmedia
from controller import kpf

from auth.user import Auth
from auth.db.userDb import UserDb

userDb = UserDb()

### sample ###
from todo.todo import Todo 

### GPT API ###
from extractor.extractor import Extractor
from extractor.cbs import CBS
from extractor.asiatimes import AsiaTimes

### NEWS API ###
from news.news import News

### VOUCHER API ###
from voucher.asiatimes import Global
from voucher.googleApi import Google_Api
from voucher.hans import ESG
from voucher.news2day import NEWS2DAY
from voucher.news2dayElastic import NEWS2DAY_ELASTIC

app = Flask(__name__)
CORS(app)
CORS(app, resources={r'*': {'origins': '*'}})

api = Api(
    app,
    version='0.1',
    title="AI TEAM's API Server",
    description="AI TEAM 118 API Server! (http://211.232.77.118:10001/)",
    terms_url="/",
    contact="skc@yjmedia.com",
    license="MIT"
)

app.register_blueprint(yjmedia, url_prefix='/')
app.register_blueprint(kpf, url_prefix='/kpf')

@api.documentation
def custom_ui():
    #authCheck = request.headers.get('Authorization')
    token = request.cookies.get('access_token')
    if token is None:
        return redirect(url_for('yjmedia.login'))
    else :
        return apidoc.ui_for(api)
    

api.add_namespace(Todo, '/todo')
api.add_namespace(Auth, '/auth')
api.add_namespace(CBS, '/cbs')
api.add_namespace(AsiaTimes, '/asiatimes')

api.add_namespace(Extractor, '/extractor')
api.add_namespace(News, '/news')
api.add_namespace(Global, '/global')
api.add_namespace(Google_Api, '/google')
api.add_namespace(NEWS2DAY_ELASTIC, '/esg')
# api.add_namespace(ESG, '/esg')
# api.add_namespace(NEWS2DAY, '/news2day')

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=10001) #실제 운영 API 
    #app.run(debug=True, port=5000) # 테스트 API
