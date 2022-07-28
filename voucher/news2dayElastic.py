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
            뉴스투데이 API 입니다. (Elasticsearch 적용)

            ### page/display값은 ESG 통합검색에서는 사용되지 않습니다. (값 무시)
            ### ESG전체검색에서 ESG별로 TOTAL COUNT가 리턴됩니다.
            ###

            **query** : 검색어 (required)
            **esg** : 분류값 (ESG / "E,S,G" / required)
            **condition** : 조건 (""/"AND"/"OR")
            **sdate** : 시작날짜 (yyyy-mm-dd / required)
            **edate** : 종료날짜 (yyyy-mm-dd / required)

            **page** : 페이지 (default 1 / required)
            **display** : 한페이지내에 보여줄 기사 갯수 (default 10 / required)
            **emotion** : 감성 점수 입니다 1~5 (default "" / required)

            # Output Arguments
            ``` json
            {
                "result": [
                    {
                        "type": "",
                        "list": [
                            {
                                "article": "",
                                "title": "",
                                "url": ""
                            }
                        ]
                    }
                ],
                "success": true
            }
            ```
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