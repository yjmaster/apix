from flask import request
from flask_restx import Resource, Namespace, fields
from voucher.database.news2day.news2dayElastic import News2dayElastic
from voucher.util import Util
from utils.aiLog import aiLog

NEWS2DAY_ELASTIC = Namespace(
    name="ESG",
    description="한스/뉴스투데이 공통 AI ESG API. (Elasticsearch 사용)"
)

news2dayElastic = News2dayElastic()
util = Util()
log = aiLog()

# request model
req_model = NEWS2DAY_ELASTIC.model('NEWS2DAY_Model',{
            'type': fields.String(example="N"),
            'esg' : fields.String(example="ESG"),
            'display' : fields.String(example="10"),
            'page' : fields.String(example="1"),
            'emotion' : fields.String(example=""),
            'query' : fields.String(example="양재"),
            'sdate': fields.String(example="2022-09-26"),
            'edate': fields.String(example="2022-09-27"),
            'condition': fields.String(example="OR")
        })

# response model
res_model = NEWS2DAY_ELASTIC.model('News2day Res', {
    'success': fields.Boolean(description='API Success/Failure', required=True),
    'result': fields.String(description='Success/Failure message',required=True),
})

@NEWS2DAY_ELASTIC.route('/selectNews')
class selectNews(Resource):
        
        @NEWS2DAY_ELASTIC.doc(parser=req_model)
        
        @NEWS2DAY_ELASTIC.response(200, 'API Success/Failure', res_model)
        @NEWS2DAY_ELASTIC.response(400, 'Failure')
        @NEWS2DAY_ELASTIC.response(500, 'Error')
        
        def post(self):
            """
            한스/뉴스투데이 공통 AI ESG API 입니다.

            ### page/display 값은 ESG 통합검색에서는 사용되지 않습니다. (값 무시)
            ### ESG: ESG별로 TOTAL COUNT가 리턴됩니다.
            ### EMOTION: 감성 점수별로 TOTAL COUNT가 리턴됩니다.

            **type** : 포털 타입 (네이버:N, 구글:G / required) - 한스 ESG의 경우 포털을 선택하지 않기 때문에 API에서 자체적으로 포털 타입을 "N"으로 설정합니다.  
            **query** : 검색어 (required)
            **esg** : 분류값 (ESG / "E,S,G" / required)
            **condition** : 조건 (""/"AND"/"OR")
            **sdate** : 시작날짜 (yyyy-mm-dd / required)
            **edate** : 종료날짜 (yyyy-mm-dd / required)

            **page** : 페이지 (default 1 / required)
            **display** : 한 페이지 내에 보여줄 기사 갯수 (default 10 / required)
            **emotion** : 감성 점수 입니다 1~5 (default "" / required)

            # Output Arguments (Example)
            ``` json
            {
                "success": true,
                "result": [
                    {
                    "type": "E",
                    "list": [
                        {
                        "press": "언론사",
                        "title": "기사제목",
                        "url": "기사 url",
                        "emotion": "감성 점수",
                        "img": "기사 썸네일 이미지 url"
                        }
                    ]
                    },
                    {
                    "type": "S",
                    "list": [
                        {
                        "press": "언론사",
                        "title": "기사제목",
                        "url": "기사 url",
                        "emotion": "감성 점수",
                        "img": "기사 썸네일 이미지 url"
                        }
                    ]
                    },
                    {
                    "type": "G",
                    "list": [
                        {
                        "press": "언론사",
                        "title": "기사제목",
                        "url": "기사 url",
                        "emotion": "감성 점수",
                        "img": "기사 썸네일 이미지 url"
                        }
                    ]
                    }
                ],
                "total": [
                    {
                    "e_cnt": 32
                    },
                    {
                    "s_cnt": 301
                    },
                    {
                    "g_cnt": 53
                    }
                ],
                "senti": [
                    {
                    "level": "5",
                    "cnt": 103
                    },
                    {
                    "level": "3",
                    "cnt": 80
                    },
                    {
                    "level": "4",
                    "cnt": 75
                    },
                    {
                    "level": "1",
                    "cnt": 67
                    },
                    {
                    "level": "2",
                    "cnt": 54
                    }
                ]
                }
            ```
            """
        
            # result = news2dayDB.SELECT(params)
            params = request.get_json()
            
            media = None
            # 220926 한스ESG 에서도 이 API 를 사용함. 한스ESG에서 검색 시 포털 선택을 하지 않기 때문에 type 값으로 N을 설정해준다. 
            if not params.get("type") : 
                params['type'] = "N"
                media = "hans"
            else : media = "news2day"

            required = {'type': True, 'esg': True, 'display': 10, 'page': 1, 'emotion': "", 'query': True, 'sdate': True, 'edate': True, 'condition': ""}
            refineParams = util.validationCheck(params, required)
            
            result = None
            try:
                if refineParams["success"] :
                    newParams = refineParams["params"]
                    #print(newParams)
                    
                    index = "voucher_news"
                    result = news2dayElastic.search(index, newParams)
                    log.wirte_log(media, request) # 검색 사용 로그를 남긴다
                    
                    return result
                
            except Exception as exp:
                result = {"success" : False, "message": str(exp)}
                
            finally:
                return result        
