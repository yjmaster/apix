from flask import request, make_response
from flask_restx import Resource, Namespace, fields

import json
from extractor.db.aiLog import aiLog

from yj_kogpt2_API.inference2 import kogpt2_inference_API
from yj_kogpt2_sentiment_analyzer.sentiment_inference2 import kogpt2_inference_sentiment
from textrank_master.summary import TextRank 

KoGPT2_inferer_API = kogpt2_inference_API()
Senti_inferer_API = kogpt2_inference_sentiment()

log = aiLog()

CBS = Namespace(
    name="CBS",
    description="CBS API (GPT 를 활용한 AI 입니다.)",
)

# request model
cbs_req = CBS.model('cbs_req', {
    'title': fields.String(required=True, description='기사 제목',
        example="'신발투척' 정창옥 광복절 집회서 경찰 폭행으로 또 구속 기로"),
    'contents': fields.String(required=True, description='기사 본문',
        example="집단감염 우려 속에 서울 도심에서 강행된 광복절 집회에서 경찰에 폭력을 행사하는 등 공무집행을 방해한 참가자 2명이 18일 오후 구속심사를 받기 위해 법원에 출석했다.\n"+
                "2명 중 1명은 지난달 국회를 방문한 문재인 대통령을 향해 신발을 던졌던 정창옥(57)씨다. 정씨는 당시 구속 위기를 면했지만 이번엔 집회에서 경찰을 폭행한 혐의로 다시 구속 갈림길에 섰다.\n"+
                "서울중앙지법 최창훈 영장전담 부장판사는 이날 오후 3시부터 공무집행방해 등 혐의를 받는 정씨의 구속 전 피의자 심문(영장실질심사)을 진행한다.\n"+
                "정씨는 지난 15일 광화문 광장에서 열린 광복절 집회에 참여해 청와대 방면으로 이동하던 중 이를 저지하는 경찰관을 폭행한 혐의를 받는다. 그는 현행범으로 체포돼 경찰에서 조사를 받았다.\n"+
                "오후 2시 35분께 법원 앞에 모습을 드러낸 정씨는 '두 번째 영장심사인데 심경은 어떤가'라는 취재진 질문에 \"담담하다, 괜찮다\"며 \"왜 구속이 됐는지 모르겠고, 그냥 평화적으로 청와대로 가는 사람을 붙잡았다. 그것에 대해서 항거할 것\"이라고 답했다.\n"+
                "경찰에게 폭력을 행사했다는 혐의에 대해서는 \"전혀 한 적 없다\"며 \"(정부가) 저를 표적으로 삼았다\"고 말했다.\n"+
                "정씨는 국민에게 한마디를 해 달라는 한 유튜버의 요청을 받고 \"자유대한민국은 살아 있다. 끝까지 함께하겠다\"고 말하며 발걸음을 옮겼다.\n"+
                "이날 정씨의 출석 직후 정씨 아들이 대표를 맡은 비영리단체 '긍정의 힘' 관계자들은 법원 앞에서 기자회견을 열고 정씨의 구속이 부당하다는 취지로 주장했다.\n")
})

# response model
cbs_res = CBS.model('cbs_res', {
    'success': fields.Boolean(description='API Success/Failure', required=True),
    'extractor': fields.String(description='Success/Failure message', required=True)
})

################################################################################
@CBS.route('/GPT-keyword')
class GPT_keyword(Resource):
    @CBS.doc(parser=cbs_req)
    @CBS.response(200, 'API Success/Failure', cbs_res)
    @CBS.response(400, 'Failure')
    @CBS.response(500, 'Error')
    def post(self):
        """
        키워드 추출(GPT2) API 입니다.

        ## Input Arguments 를 JSON 형식으로 전달합니다.
        
        **title**: str : required **(필수)** : 기사의 제목 입니다.

        **contents**: str : required **(필수)** : 기사의 본문 입니다. ( 태그가 존재 하면 안됩니다. )

        ## Output Arguments
        ``` json
        {
            "success": true,
            "extractor": [
                "구속영장실질심사",
                "구속영장",
                "광화문집회",
                "집회",
                "정창옥",
                "광복절",
                "경찰폭행",
                "신발투척"
            ]
        }        
        ```
        """
        r = None
        try:
            wirte_log(request)
            args = parse_req_data(request)
            if len(args['title']) == 0 and len(args['contents']) == 0:
                r = {"success": False, "message": "NO INPUT"}
                return make_response(r)

            t = args['title']
            c = args['contents']

            gpt = KoGPT2_inferer_API.inference_KEYWORD(t, c)
            r = {"success": True, "extractor": gpt}

        except Exception as exp:
            r = {"success": False, "message": str(exp)}
        finally:
            return make_response(r)
################################################################################

################################################################################
@CBS.route('/GPT-section')
class GPT_section(Resource):
    @CBS.doc(parser=cbs_req)
    @CBS.response(200, 'API Success/Failure', cbs_res)
    @CBS.response(400, 'Failure')
    @CBS.response(500, 'Error')
    def post(self):
        """
        기사 분류(GPT2) API 입니다.

        ## Input Arguments 를 JSON 형식으로 전달합니다.
        
        **title**: str : required **(필수)** : 기사의 제목 입니다.

        **contents**: str : required **(필수)** : 기사의 본문 입니다. ( 태그가 존재 하면 안됩니다. )

        ## Output Arguments
        ``` json
        {
            "success": true,
            "extractor": "사회"
        }        
        ```
        """
        r = None
        try:
            wirte_log(request)
            args = parse_req_data(request)
            if len(args['title']) == 0 and len(args['contents']) == 0:
                r = {"success": False, "message": "NO INPUT"}
                return make_response(r)

            t = args['title']
            c = args['contents']

            gpt = KoGPT2_inferer_API.inference_SECTION(t, c)
            r = {"success": True, "extractor": gpt}

        except Exception as exp:
            r = {"success": False, "message": str(exp)}
        finally:
            return make_response(r)

################################################################################

################################################################################
@CBS.route('/GPT-sentiment')
class GPT_sentiment(Resource):
    @CBS.doc(parser=cbs_req)
    @CBS.response(200, 'API Success/Failure', cbs_res)
    @CBS.response(400, 'Failure')
    @CBS.response(500, 'Error')
    def post(self):
        """
        감성 분석(GPT2) API 입니다.

        ## Input Arguments 를 JSON 형식으로 전달합니다.
        
        **title**: str : 기사의 제목 입니다.

        **contents**: str : required **(필수)** : 기사의 본문 입니다. ( 태그가 존재 하면 안됩니다. )

        ## Output Arguments
        ``` json
        {
            "success": true,
            "extractor": "1"
        }        
        ```
        """
        r = None
        try:
            wirte_log(request)
            args = parse_req_data(request)
            title = ""
            if "title" in args:
                title = args['title']
                
            if len(title) == 0 and len(args['contents']) == 0:
                r = {"success": False, "message": "NO INPUT"}
                return make_response(r)

            t = title
            c = args['contents']

            gpt = Senti_inferer_API.inference(t, c)
            r = {"success": True, "extractor": gpt}

        except Exception as exp:
            r = {"success": False, "message": str(exp)}
        finally:
            return make_response(r)
################################################################################

################################################################################
@CBS.route('/textrank')
class textrank(Resource):
    @CBS.doc(parser=cbs_req)
    @CBS.response(200, 'API Success/Failure', cbs_res)
    @CBS.response(400, 'Failure')
    @CBS.response(500, 'Error')
    def post(self):
        """
        본문 요약(TFIDF) API 입니다.

        ## Input Arguments 를 JSON 형식으로 전달합니다.

        **contents**: str : required **(필수)** : 기사의 본문 입니다. ( 태그가 존재 하면 안됩니다. )

        ## Output Arguments
        ``` json
        {
            "success": true,
            "extractor": "집단감염 우려 속에 서울 도심에서 강행된 광복절 집회에서 경찰에 폭력을 행사하는 등 공무집행을 방해한 참가자 2명이 18일 오후 구속심사를 받기 위해 법원에 출석했다.\\n\\n정씨는 당시 구속 위기를 면했지만 이번엔 집회에서 경찰을 폭행한 혐의로 다시 구속 갈림길에 섰다.\\n\\n경찰에게 폭력을 행사했다는 혐의에 대해서는 \\"전혀 한 적 없다\\"며 \\"저를 표적으로 삼았다\\"고 말했다.\\n\\n"
        }         
        ```
        """

        r = None
        try:
            wirte_log(request)
            args = parse_req_data(request)

            if len(args['contents']) == 0:
                r = {"success": False, "message": "NO INPUT"}
                return make_response(r)

            c = args['contents']
            textrank = TextRank()
            gpt = textrank.summerizer(c, 3)
            r = {"success": True, "extractor": gpt}

        except Exception as exp:
            r = {"success": False, "message": str(exp)}
        finally:
            return make_response(r)
################################################################################

################################################################################
def wirte_log(request):
    router = (request.url_rule.rule).split("/")[-1]
    log.DB_CONNECT()
    log.DB_UPDATE("cbs", router)

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