import re,json, requests
from flask import request, make_response
from flask_restx import Resource, Api, Namespace, fields
from pprint import pprint

from news.cnf.LoadDB import LoadDB
from news.cnf.LogDB import LogDB 

log = LogDB()

News = Namespace(
    name="News",
    description="News API (DB 를 이용한 기사 관련 API 입니다.)",
)



# REST Api에 이용할 데이터 모델을 정의한다
model_articles = News.model('row_articles', {
    'title': fields.String(required=True, description='기사 제목', help='필수'),
    'contents': fields.String(required=True, description='기사 본문', help='필수')
})

json_parser = News.parser()
json_parser.add_argument('json', type=str, required=True, location='json',
                        help='JSON BODY argument')
arg_parser = News.parser()
arg_parser.add_argument('json', type=str, required=True,
                        help='URL JSON argument')

res_model = News.model('News Res', {
    'success': fields.Boolean(description='API Success/Failure',
                                required=True),
    'message': fields.String(description='Success/Failure message',
                                required=True),
})

################################################################################
@News.route('/asiatimes')
class ASIATIMESSEARCH(Resource):
    @News.doc(params={'query': {'description': '검색어','type': 'str','in': 'query'},
                 'display': {'description': '검색 결과 출력 건수 10(기본값), 100(최대)', 'type': 'int', 'in': 'query', 'default': 10}
                 }
            )

    @News.response(200, 'API Success/Failure', res_model)
    @News.response(400, 'Failure')
    @News.response(500, 'Error')

    def get(self):

        """
        아시아 타임즈 기사 검색 API 입니다.

        # Input Arguments 파라미터를 QueryString 형식으로 전달합니다.

        **query** : str : required **(필수)** : 검색을 원하는 문자열입니다.
        **display** : int : Unrequired : 10(기본값), 100(최대)	검색 결과 출력 건수 지정

        # Example
        ``` json
            ?query=코로나&display=10
        ```

        # Output Arguments
        ``` json
        {
            "items": [-
                {
                    "title": "대남 위협 지속중인 北 &quot;미국, 남북 문제 입다물라“",                                           # 제목
                    "content": "도날드 트럼프 미 대통령이 신경을 쓰고 있는 미국 대선을 염두에 둔 발언도 있었다..."     # 본문 
                }
            ]
        }
        ```
        """

        r = None
        try:
            logSave((request.url_rule.rule).split("/")[-1])
            q = request.args.get('query')
            l = request.args.get('display')
            print('q = '+ str(q))
            print('l = '+ str(l))

            if q in (None, '') :
                r = {"success": False,"message":"검색어는 필수 입니다."}
            else :
                query_string = request.query_string.decode('utf-8')
                loaddb = LoadDB()
                loaddb.DB_CONNECT()
                res = loaddb.DB_ASIATIME_SELECT_JSON(q,l)
                loaddb.DB_CLOSE()
                r = {"success": False, "message": "결과값이 존재 하지 않습니다."} if res is None else res

        except Exception as exp:
            r = {"success": False, "message": str(exp)}
        finally:
            return make_response(r)



################################################################################

################################################################################
@News.route('/HansQuery')
class HANSSEARCH(Resource):
    @News.doc(params={'query': {'description': '검색어','type': 'str','in': 'query'},
                     'date-from': {'description':'From when to search', 'type':'datetime', 'in':'query'},
                     'date-to': {'description':'To when to search', 'type':'datetime', 'in':'query'}
                    }
            )

    @News.response(200, 'API Success/Failure', res_model)
    @News.response(400, 'Failure')
    @News.response(500, 'Error')

    def post(self):

        """
        아시아 타임즈 기사 검색 API 입니다.

        # Input Arguments 파라미터를 QueryString 형식으로 전달합니다.

        **query** : str : required **(필수)** : 검색을 원하는 문자열입니다.
        **date-from** : datetime : Unrequired : None(기본값) From when the search to be performed.
        **date-to** : datetime : Unrequired : None(기본값) To when the search to be performed.

        # Example
        ``` json
            ?query=코로나&date-from=2020:01:01&date-to=2021:01:01
        ```

        # Output Arguments
        ``` json
        {
            "items": [-
                {
                    "title": "대남 위협 지속중인 北 &quot;미국, 남북 문제 입다물라“",                                           # 제목
                    "content": "도날드 트럼프 미 대통령이 신경을 쓰고 있는 미국 대선을 염두에 둔 발언도 있었다..."     # 본문 
                }
            ]
        }
        ```
        """

        r = None
        try:
            logSave((request.url_rule.rule).split("/")[-1])
            #q = request.args.get('query')
            #l = request.args.get('display')
            #print('q = '+ str(q))
            #print('l = '+ str(l))

            q = request.args.get('query')
            dto = request.args.get('date-to')
            dfrom = request.args.get('date-from')

            if q in (None, '') :
                r = {"success": False,"message":"검색어는 필수 입니다."}
            else :
                query_string = request.query_string.decode('utf-8')
                loaddb = HANS_query()
                loaddb.DB_CONNECT()
                res = loaddb.DB_HANS_query(dfrom, dto, q)
                loaddb.DB_CLOSE()
                r = {"success": False, "message": "결과값이 존재 하지 않습니다."} if res is None or res['Success'] == False else res

        except Exception as exp:
            r = {"success": False, "message": str(exp)}
        finally:
            return make_response(r)
################################################################################


################################################################################
def parse_req_data(request):
    """
    flask의 request에서 데이터를 가져옴
        주의: flask-restplus 모듈을 이용하여 swagger ui를 이용하는 패러미터
            패싱이 제대로 안되어 본 함수 이용 (0.10.1)
    :param request: Flask의 request
    :return: parameter dict
    """
    if not hasattr(request, 'method'):
        return None
    if request.method.upper() != 'GET':
        if request.data:
            return json.loads(request.data.decode('utf-8'), strict=False)
    if 'json' in request.args:
        return json.loads(request.args['json'])
    if request.args:
        return request.args     # note: type is ImmutableMultiDict
    return {}

def logSave(router):
    log.DB_CONNECT()
    log.DB_INSERT(router)
    log.DB_CLOSE()
