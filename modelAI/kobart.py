# -*- coding: utf-8 -*-
import json
import requests

from flask import request, make_response, render_template
from flask_restx import Resource, Namespace, fields

# custom modules
from utils.aiLog import aiLog
from utils.reqFormat import reqFormat

log = aiLog()

Kobart = Namespace(
    name="kobart",
    description="kobart 테스트 API.",
)

# request model
kobart_req = Kobart.model('asia_req', {
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
kobart_res = Kobart.model('asia_res', {
    'success': fields.Boolean(description='API Success/Failure', required=True),
    'extractor': fields.String(description='Success/Failure message', required=True)
})

@Kobart.route('/title')
class KoBart_title(Resource):
    @Kobart.doc(parser=kobart_req)
    @Kobart.response(200, 'API Success/Failure', kobart_res)
    @Kobart.response(400, 'Failure')
    @Kobart.response(500, 'Error')
    def post(self):
        """
        제목 생성(kobart) API 입니다.

        # Input Arguments 를 JSON 형식으로 전달합니다.

        **contents**: str : required **(필수)** : 기사의 본문 입니다. ( 태그가 존재 하면 안됩니다. )
        
        ## Output Arguments
        ``` json
        {
            "success": true,
            "extractor": "광복절 집회서 경찰 폭행한 정창옥, 구속 갈림길에 서다"
        }
        ```
        """
        r = None
        try:
            log.wirte_log('yjmedia', request)
            args = reqFormat.parse_data(request)
            url = 'http://192.168.0.190:5000/kobart/title'
            headers = {'Content-Type':'application/json; charset=utf-8'}
            res = requests.post(url, json=args, headers=headers)
            if res.status_code == 200 :
                r = json.loads(res.text)
                
        except Exception as exp:
            r = {"success": False, "message": str(exp)}
        finally:
            return make_response(r)
        
# @Kobart.route('/test')
# class KobartTest(Resource):
#     def get(self):
#         headers = {'Content-Type': 'text/html'}
#         return make_response(render_template('test.html'),200,headers)

