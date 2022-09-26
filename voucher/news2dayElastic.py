from flask import request
from flask_restx import Resource, Namespace, fields
from voucher.database.news2day.news2dayElastic import News2dayElastic
from voucher.util import Util
from extractor.db.aiLog import aiLog

NEWS2DAY_ELASTIC = Namespace(
    name="NEWS2DAY",
    description="뉴스투데이 API 입니다. (Elasticsearch 적용)"
)

news2dayElastic = News2dayElastic()
util = Util()
log = aiLog()

# response model
res_model = NEWS2DAY_ELASTIC.model('News2day Res', {
    'success': fields.Boolean(description='API Success/Failure', required=True),
    'message': fields.String(description='Success/Failure message',required=True),
})

@NEWS2DAY_ELASTIC.route('/selectNews')
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
            **display** : 한 페이지 내에 보여줄 기사 갯수 (default 10 / required)
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
                "success": True
            }
            ```
            """
        
            # result = news2dayDB.SELECT(params)
            params = request.get_json()
            
            # 220926 한스ESG 에서도 이 API 를 사용함. 한스ESG에서 검색 시 포털 선택을 하지 않기 때문에 type 값으로 N을 설정해준다. 
            if not params.get("type") : 
                params['type'] = "N"

            required = {'type': True, 'esg': True, 'display': 10, 'page': 1, 'emotion': "", 'query': True, 'sdate': True, 'edate': True, 'condition': ""}
            refineParams = util.validationCheck(params, required)
            
            result = None
            try:
                if refineParams["success"] :
                    newParams = refineParams["params"]
                    print(newParams)
                    
                    index = "voucher_news"
                    result = news2dayElastic.search(index, newParams)
                    write_log(request) # 검색 사용 로그를 남긴다
                    
                    return result
                
            except Exception as exp:
                result = {"success" : False, "message": str(exp)}
                
            finally:
                return result        

def write_log(request):
    router = (request.url_rule.rule).split("/")[-1]
    log.DB_CONNECT()
    log.DB_UPDATE("news2day", router)