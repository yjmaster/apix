from flask import request
from flask_restx import Resource, Namespace, fields
from voucher.database.news2day.news2dayDB import News2dayDB
from voucher.util import Util

NEWS2DAY = Namespace(
    name="NEWS2DAY",
    description="뉴스투데이 API 입니다. (TEST를 위한 RDBMS 적용. 실제 사용 X)"
)

news2dayDB = News2dayDB()
util = Util()

res_model = NEWS2DAY.model('News2day Res', {
    'success': fields.Boolean(description='API Success/Failure', required=True),
    'message': fields.String(description='Success/Failure message',required=True),
})

@NEWS2DAY.route('/selectNews')
class selectNews(Resource):
    
        news2day_model = NEWS2DAY.model('NEWS2DAY_Model',{
            'type': fields.String(example="G")
        })
        
        @NEWS2DAY.expect(news2day_model)
        
        @NEWS2DAY.response(200, 'API Success/Failure', res_model)
        @NEWS2DAY.response(400, 'Failure')
        @NEWS2DAY.response(500, 'Error')
        
        def post(self):
            """
            뉴스투데이 API 입니다. (TEST를 위한 RDBMS 적용. 실제 사용 X)
            """
            result = None
        
            # result = news2dayDB.SELECT(params)
            params = request.get_json()
            required = {'type': True, 'esg': True, 'display': 10, 'page': 1, 'emotion': "", 'query': True, 'sdate': True, 'edate': True, 'condition': ""}
            refineParams = util.validationCheck(params, required)
            
            if refineParams["success"] :
                newParams = refineParams["params"]
                print(newParams)
                result = news2dayDB.SELECT(newParams) 
            
            return result