# -*- coding: utf-8 -*-
import json
import requests

from flask import request, make_response, jsonify, render_template
from flask_restx import Resource, Namespace, fields

# text modules
from textrank_master.summary import TextRank

# ai model
from kobart_modules.inference import kobart_inference_API
kobart_api = kobart_inference_API()

# custom db
from auth.bflysoft.db import BflysoftDb

# custom modules
from utils.textFormat import TextFormat
from utils.customWord import CustomWord
from utils.aiLog import aiLog

bflysoftDb = BflysoftDb()
textFormat = TextFormat()
customWord = CustomWord()

log = aiLog()

Kobart = Namespace(
    name="kobart",
    description="kobart 테스트 API.",
)

# request model
kobart_req = Kobart.model('asia_req', {
    'id_client':fields.String(required=True, description='클라이언트ID', example="8C131969-5015-D02E-CCF1-EB4624C93692"),
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
class koBart_title(Resource):
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
		
		try:
			res =  {}
			args = textFormat.parse_data(request)
			router = (request.url_rule.rule).split("/")[-1]

			id_client = args['id_client']
			content = args['content']

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
			res = bflysoftDb.authentication(id_client)
			logInfo.update(res)
			if not res['success']: return

			# 데이터 유효성 체크
			top3Summary = ""
			sents = textFormat.contentAnalysis(content)
			# sents = ['test1','test2','test3','test4','test5']
			if len(sents) < 5:
				logInfo.update({
					"success": False,
					"message": "5문장 이상 입력해주세요.",
					'code': 400
				})
				res = logInfo
				return

			for idx, sent in enumerate(sents):
				if idx < 3: top3Summary += sent
    
			args['summary'] = top3Summary
                
			# 제목추출
			titles = []
			title1 = kobart_api.kobart_title(content)
			# title1 = {"success": False, "code": 400, "message": "제목추출에러1"}
			# title1 = {"success": True, "extractor": "제목추출1"}
			if not title1['success']:
				logInfo.update(title1)
				res = logInfo
				return

			title2 = kobart_api.kobart_title(top3Summary)
			# title2 = {"success": False, "code": 400, "message": "제목추출에러2"}
			# title2 = {"success": True, "extractor": "제목추출2"}
			if not title2['success']:
				args['summary'] = top3Summary
				logInfo.update(title2)
				res = logInfo
				return

			t1 = title1["extractor"]
			t2 = title2["extractor"]

			if t1 == t2 :
				titles.append(t1)
			else:
				titles.append(t1)
				titles.append(t2)
			
			logInfo["extractor"] = titles
			res = logInfo

			# raise Exception('kobart test error')
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

			print("------------------------------------")
			print("logInfo : ", logInfo)
			print("finally: ", res)
			print("------------------------------------")
			return make_response(res, logInfo['code'])
        
@Kobart.route('/keyword')
class KobartKeyword(Resource):
	@Kobart.doc(parser=kobart_req)
	@Kobart.response(200, 'API Success/Failure', kobart_res)
	@Kobart.response(400, 'Failure')
	@Kobart.response(500, 'Error')
	def post(self):
		"""
		키워드 생성 (kobart) API 입니다.

		# Input Arguments 를 JSON 형식으로 전달합니다.

		**contents**: str : required **(필수)** : 기사의 본문 입니다. ( 태그가 존재 하면 안됩니다. )

		## Output Arguments
		``` json
		{
			"success": true,
			"extractor": "광복절/집회방해/구속"
		}
		```
		"""
		try:
			res =  {}
			args = textFormat.parse_data(request)
			router = (request.url_rule.rule).split("/")[-1]

			id_client = args['id_client']
			title = args['title']
			content = args['content']

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
			res = bflysoftDb.authentication(id_client)
			logInfo.update(res)
			if not res['success']: return

			# 데이터 유효성 체크
			top3Summary = ""
			sents = textFormat.contentAnalysis(content)
			# sents = ['test1','test2','test3','test4','test5']
			if len(sents) < 5:
				logInfo.update({
					"success": False,
					"message": "5문장 이상 입력해주세요.",
					'code': 400
				})
				res = logInfo
				return

			for idx, sent in enumerate(sents):
				if idx < 3: top3Summary += sent

			args['summary'] = top3Summary
                
			# 키워드 추출
			keywords = []
			total_contents = (title + '\n' + content)
			keyword1 = kobart_api.kobart_keyword(total_contents)
			# keyword1 = {"success": False, "code": 400, "message": "키워드추출에러1"}
			# keyword1 = {"success": True, "extractor": "키워드1/키워드2/키워드3"}
			if not keyword1['success']:
				logInfo.update(keyword1)
				res = logInfo
				return

			keyword2 = kobart_api.kobart_keyword(top3Summary)
			# keyword2 = {"success": False, "code": 400, "message": "키워드추출에러2"}
			# keyword2 = {"success": True, "extractor": "키워드4/키워드5/키워드6"}
			if not keyword2['success']:
				args['summary'] = top3Summary
				logInfo.update(keyword2)
				res = logInfo
				return

			k1 = keyword1["extractor"].split("/")
			k2 = keyword2["extractor"].split("/")

			keywords = (k1 + k2)
			keywords = customWord.countryNameParsing(total_contents, keywords)
			keywords = textFormat.keywordsIncludeContent(total_contents, keywords)

			logInfo["extractor"] = keywords
			res = logInfo

			# raise Exception('kobart keyword test error')
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

			print("------------------------------------")
			print("logInfo : ", logInfo)
			print("finally: ", res)
			print("------------------------------------")
			return make_response(res, logInfo['code'])

@Kobart.route('/subTitle')
class KobartKeyword(Resource):
	@Kobart.doc(parser=kobart_req)
	@Kobart.response(200, 'API Success/Failure', kobart_res)
	@Kobart.response(400, 'Failure')
	@Kobart.response(500, 'Error')
	def post(self):
		"""
		부제목 생성 (kobart) API 입니다.

		# Input Arguments 를 JSON 형식으로 전달합니다.

		**contents**: str : required **(필수)** : 기사의 본문 입니다. ( 태그가 존재 하면 안됩니다. )

		## Output Arguments
		``` json
		{
			"success": true,
			"extractor": ""
		}
		```
		"""
		try:
			res =  {}
			args = textFormat.parse_data(request)
			router = (request.url_rule.rule).split("/")[-1]

			id_client = args['id_client']
			title = args['title']
			content = args['content']

			logInfo = {
				'code': 200,
				'router': router,
				'id_client': id_client,
				'media': 'tester'
			}

			# 호출 로그를 남겨준다.
			res = log.request_log(logInfo)
			logInfo.update(res)
			if not logInfo['success']: return

			# 데이터 유효성 체크
			sents = textFormat.contentAnalysis(content)
			# sents = ['test1','test2','test3','test4','test5']
			if len(sents) < 5:
				logInfo.update({
					"success": False,
					"message": "5문장 이상 입력해주세요.",
					'code': 400
				})
				res = logInfo
				return

			# 부제목 추출
			subTitles = []
			textrank = TextRank()
			summary = textrank.summerizer(sents, 4)
			# summary = ["요약문장입니다1","요약문장입니다2","요약문장입니다3","요약문장입니다4"]
			for summ in summary:
				# title = {"success": False, "code": 400, "message": "부제목추출에러2"}
				# title = {"success": True, "extractor": "부제목추출"}
				title = kobart_api.kobart_title(summ)
				if not title['success']:
					args['summary'] = summ
					logInfo.update(title)
					res = logInfo
					return
				subTitles.append(title['extractor'])

			subTitles = list(set(subTitles))
			logInfo['extractor'] = subTitles
			res = logInfo

			# raise Exception('kobart subtitle test error')
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

			print("------------------------------------")
			print("logInfo : ", logInfo)
			print("finally: ", res)
			print("------------------------------------")
			return make_response(res, logInfo['code'])