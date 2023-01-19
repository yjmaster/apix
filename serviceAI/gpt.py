# -*- coding: utf-8 -*-
import json
import requests

from flask import request, make_response, jsonify, render_template
from flask_restx import Resource, Namespace, fields

from yj_kogpt2_sentiment_analyzer.sentiment_inference2 import kogpt2_inference_sentiment
senti_inferer_API = kogpt2_inference_sentiment()

from utils.textFormat import TextFormat
from utils.customWord import CustomWord
from utils.aiLog import aiLog

textFormat = TextFormat()
customWord = CustomWord()

log = aiLog()

Gpt = Namespace(
    name="gpt",
    description="gpt 테스트 API.",
)

# request model
gpt_req = Gpt.model('gpt_req', {
    'id_client': fields.String(required=True, description='클라이언트ID',
        example="CE746CE9-7456-11ED-94D7-7B233ECE4E1A"),
    'title': fields.String(required=True, description='기사 제목',
        example="'신발투척' 정창옥 광복절 집회서 경찰 폭행으로 또 구속 기로"),
    'content': fields.String(required=True, description='기사 본문',
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
gpt_res = Gpt.model('gpt_res', {
    'code': fields.Integer(description='API Success/Failure', required=True),
    'success': fields.Boolean(description='API Success/Failure', required=True),
    'extractor': fields.String(description='Success/Failure message', required=True)
})

@Gpt.route('/sentiment')
class GptSentiment(Resource):
	@Gpt.doc(parser=gpt_req)
	@Gpt.response(200, 'API Success/Failure', gpt_res)
	@Gpt.response(400, 'Failure')
	@Gpt.response(500, 'Error')
	def post(self):
		"""
		감성 분석 (GPT2) API 입니다.

		# Input Arguments 를 JSON 형식으로 전달합니다.

		**contents**: str : required **(필수)** : 기사의 본문 입니다. ( 태그가 존재 하면 안됩니다. )

		(5: 강한긍정, 4: 긍정, 3: 중립, 2: 부정, 1: 강한부정)

		## Output Arguments
		``` json
		{
			"code": 200,
			"extractor": "1",
			"success": true
		}
		```
		"""
		try:
			res =  {}
			args = textFormat.parse_data(request)
			router = (request.url_rule.rule).split("/")[-1]

			id_client = args['id_client']
			content = args['content']

			if 'title' not in args:
				args['title'] = ""

			logInfo = {
				'code': 200,
				'router': router,
				'id_client': id_client
			}

			# 호출 로그를 남겨준다.
			res = log.request_log(logInfo)
			logInfo.update(res)
			if not logInfo['success']: return

			# 키 인증을 받는다.
			res = log.authentication(id_client)
			logInfo.update(res)
			if not res['success']: return

			# 데이터 유효성 체크
			sents = textFormat.contentAnalysis(content)
			if len(sents) < 5:
				logInfo.update({
					"success": False,
					"message": "5문장 이상 입력해주세요.",
					'code': 400
				})
				res = logInfo
				return

			gpt = senti_inferer_API.inference(args['title'], args['content'])
			res['success'] = True
			res['extractor'] = gpt
			logInfo.update(res)
			res = logInfo

		except Exception as exp:
			res = {"success": False, "code": 400, "message": str(exp)}
			logInfo.update(res)
		finally:
			# 완료 로그를 남겨준다.
			complete_res = log.response_log(logInfo, args)
			if not complete_res['success']:
				res = complete_res
				logInfo.update(complete_res)
				log.response_log(logInfo, args)
			
			del logInfo['router']
			del logInfo['id_client']
			del logInfo['uid']
			del logInfo['media']

			print("------------------------------------")
			print("finally: ", res)
			print("------------------------------------")
			return make_response(res, logInfo['code'])