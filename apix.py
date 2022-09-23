from flask import Flask
from flask_restx import Resource, Api
from flask_cors import CORS, cross_origin

### sample ###
from todo.todo import Todo 

### GPT API ###
from extractor.extractor import Extractor
from extractor.cbs import CBS

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

api.add_namespace(Todo, '/todo')
api.add_namespace(CBS, '/cbs')
api.add_namespace(Extractor, '/extractor')
api.add_namespace(News, '/news')
api.add_namespace(Global, '/global')
api.add_namespace(Google_Api, '/google')
api.add_namespace(ESG, '/esg')
api.add_namespace(NEWS2DAY, '/news2day')
api.add_namespace(NEWS2DAY_ELASTIC, '/news2day')

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=10001) #실제 운영 API 
    #app.run(debug=True, port=5000) # 테스트 API
