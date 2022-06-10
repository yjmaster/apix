from flask import request
from flask_restx import Resource, Namespace, fields
from voucher.database.news2day.news2dayElastic import News2dayElastic
from voucher.util import Util

NEWS2DAY_ELASTIC = Namespace(
    name="NEWS2DAY",
    description="뉴스투데이 API 입니다. (Elasticsearch 적용)"
)

news2dayElastic = News2dayElastic()
util = Util()

res_model = NEWS2DAY_ELASTIC.model('News2day Res', {
    'success': fields.Boolean(description='API Success/Failure', required=True),
    'message': fields.String(description='Success/Failure message',required=True),
})

@NEWS2DAY_ELASTIC.route('/selectNewsElastic')
# @NEWS2DAY_ELASTIC.route('/_search')
class selectNews(Resource):
    
        news2day_model = NEWS2DAY_ELASTIC.model('NEWS2DAY_Model_Elastic',{
            'type': fields.String(example="G")
        })
        
        @NEWS2DAY_ELASTIC.expect(news2day_model)
        
        @NEWS2DAY_ELASTIC.response(200, 'API Success/Failure', res_model)
        @NEWS2DAY_ELASTIC.response(400, 'Failure')
        @NEWS2DAY_ELASTIC.response(500, 'Error')
        
        def post(self):
            """
            뉴스투데이 API 입니다. (TEST 중 / Elasticsearch 적용)
            """
            result = None
        
            # result = news2dayDB.SELECT(params)
            params = request.get_json()
            required = {'type': True, 'esg': True, 'display': 10, 'page': 1, 'emotion': "", 'query': True, 'sdate': True, 'edate': True, 'condition': ""}
            refineParams = util.validationCheck(params, required)
            
            if refineParams["success"] :
                newParams = refineParams["params"]
                print(newParams)
                
                index = "voucher_news"
                result = news2dayElastic.search(index, newParams)
            
            return result