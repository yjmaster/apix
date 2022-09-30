import json
import requests
from pprint import pprint

from flask import request, make_response
from flask_restx import Resource, Namespace, fields

# custom modules
from utils.aiLog import aiLog
from utils.reqFormat import reqFormat

log = aiLog()

from konke.model.unsupervised.statistical.tfidf import TfIdf

# ai modules
from yj_kogpt2_API.inference import kogpt2_inference_API
from pytorch_bert_crf_ner.web_infer import ner_web_infer
from person_info.person_app import Person
from naver_search_dict.dict_api import NAVERAPI
from google_image.google_images_url import google_images_url 
from yj_kogpt2_sentiment_analyzer.sentiment_inference import kogpt2_inference_sentiment
from yj_kobart_summ.infer import kobart_inference_summ
from global_keyword.globalKey import keyCrawler
#from yj_kogpt2_ESG_section.inference_kogpt2_ESG import kogpt2_inference_ESG_section
from ASIA_TIMES_data_voucher.eng_senti.infer_senti import eng_senti

KoGPT2_inferer_API = kogpt2_inference_API()
KoBERT_inferer_API = ner_web_infer()
Person_inferer_API = Person()
Senti_inferer_API = kogpt2_inference_sentiment()
KoBART_inferer_API = kobart_inference_summ()
#KoGPT2_ESG_API = kogpt2_inference_ESG_section()
ASIA_TIMES_ENG_SENTI = eng_senti()

from textrank_master.summary import TextRank 

log = aiLog()

AsiaTimes = Namespace(
    name="AsiaTimes",
    description="아시아타임즈 API (GPT를 활용한 AI 입니다.)",
)

# request model
asia_req = AsiaTimes.model('asia_req', {
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
asia_res = AsiaTimes.model('asia_res', {
    'success': fields.Boolean(description='API Success/Failure', required=True),
    'extractor': fields.String(description='Success/Failure message', required=True)
})

################################################################################
@AsiaTimes.route('/GPT-title')
class GPT_title(Resource):
    @AsiaTimes.doc(parser=asia_req)
    @AsiaTimes.response(200, 'API Success/Failure', asia_res)
    @AsiaTimes.response(400, 'Failure')
    @AsiaTimes.response(500, 'Error')
    def post(self):
        """
        제목 생성(GPT2) API 입니다.

        # Input Arguments 를 JSON 형식으로 전달합니다.

        **contents**: str : required **(필수)** : 기사의 본문 입니다. ( 태그가 존재 하면 안됩니다. )
        
        ## Output Arguments
        ``` json
        {
            "success": true,
            "extractor": "[추천1] 광복절 집회서 경찰 폭행한 정씨 구속\\n[추천2] 광복절 집회서 경찰 폭행한 참가자 구속"
        }
        ```
        """
        r = None
        try:
            log.wirte_log('asiatimes', request)
            args = reqFormat.parse_data(request)
            
            if len(args['contents']) == 0:
                r = {"success": False, "message": "NO INPUT"}
                return make_response(r)
                
            t = "."
            c = args['contents']
            c = reqFormat.parse_content('asiatimes', c)
            
            gpt = KoGPT2_inferer_API.inference_TITLE(t, c)
            #gpt = gpt.split("제목 :")[-1]
            gpt = gpt.replace('</s>', '')
            #print(gpt)
            r = {"success": True, "extractor": gpt}

        except Exception as exp:
            r = {"success": False, "message": str(exp)}
        finally:
            return make_response(r)
################################################################################

################################################################################
@AsiaTimes.route('/GPT-section')
class GPT_section(Resource):
    @AsiaTimes.doc(parser=asia_req)
    @AsiaTimes.response(200, 'API Success/Failure', asia_res)
    @AsiaTimes.response(400, 'Failure')
    @AsiaTimes.response(500, 'Error')
    def post(self):
        """
        분류 추천(GPT2) API 입니다.

        ## Input Arguments 를 JSON 형식으로 전달합니다.
        
        **title**: str : required **(필수)** : 기사의 제목 입니다.

        **contents**: str : required **(필수)** : 기사의 본문 입니다. ( 태그가 존재 하면 안됩니다. )

        # Output Arguments
        ``` json
        {
            "extractor":  ["사회 섹션"]
        }        
        ```
        """

        r = None
        # atlog = AuditLog('[AAA] Login checking')
        try:
            log.wirte_log('asiatimes', request)
            args = reqFormat.parse_data(request)
            #pprint(args)

            if len(args['title']) == 0 and len(args['contents']) == 0:
                r = {"success": False, "message": "NO INPUT"}
                return make_response(r)

            t = args['title']
            c = args['contents']
            c = reqFormat.parse_content('asiatimes', c)

            gpt = KoGPT2_inferer_API.inference_SECTION(t, c)
            #print(gpt)
            r = {"success": True, "extractor": gpt}

        except Exception as exp:
            r = {"success": False, "message": str(exp)}
        finally:
            return make_response(r)
################################################################################

################################################################################
@AsiaTimes.route('/GPT-keyword')
class GPT_keyword(Resource):
    @AsiaTimes.doc(parser=asia_req)
    @AsiaTimes.response(200, 'API Success/Failure', asia_res)
    @AsiaTimes.response(400, 'Failure')
    @AsiaTimes.response(500, 'Error')
    def post(self):
        """
        키워드 추출(GPT2) API 입니다.

        ## Input Arguments 를 JSON 형식으로 전달합니다.
        
        **title**: str : required **(필수)** : 기사의 제목 입니다.

        **contents**: str : required **(필수)** : 기사의 본문 입니다. ( 태그가 존재 하면 안됩니다. )

        # Output Arguments
        ``` json
        {
            "extractor": "집단감염 우려 속에 서울 도심에서 강행된 광복절 집회에서 경찰에 폭력을 행사하는 등 공무집행을 방해한 참가자 2명이 18일 오후 구속심사를 받기 위해 법원에 출석했다. 2명 중 1명은 지난달 국회를 방문한 문재인 대통령을 향해 신발을 던졌던 정창옥(57)씨다. 그는 현행범으로 체포돼 경찰에서 조사를 받았다. 오후 2시 35분께 법원 앞에 모습을 드러낸 정씨는 '두 번째 영장심사인데 심경은 어떤가'라는 취재진 질문에 \"담담하다, 괜찮다\"며 \"왜 구속이 됐는지 모르겠고, 그냥 평화적으로 청와대로 가는 사람을 붙잡았다."
        }        
        ```
        """

        r = None
        # atlog = AuditLog('[AAA] Login checking')
        try:
            log.wirte_log('asiatimes', request)
            args = reqFormat.parse_data(request)
            #pprint(args)

            if len(args['title']) == 0 and len(args['contents']) == 0:
                r = {"success": False, "message": "NO INPUT"}
                return make_response(r)

            t = args['title']
            c = args['contents']
            c = reqFormat.parse_content('asiatimes', c)

            gpt = KoGPT2_inferer_API.inference_KEYWORD(t, c)
            #print(gpt)
            r = {"success": True, "extractor": gpt}

        except Exception as exp:
            r = {"success": False, "message": str(exp)}
        finally:
            return make_response(r)
################################################################################

################################################################################
@AsiaTimes.route('/GPT-sentiment')
class GPT_sentiment(Resource):
    @AsiaTimes.doc(parser=asia_req)
    @AsiaTimes.response(200, 'API Success/Failure', asia_res)
    @AsiaTimes.response(400, 'Failure')
    @AsiaTimes.response(500, 'Error')
    def post(self):
        """
        감성 분석(GPT2) API 입니다.

        ## Input Arguments 를 JSON 형식으로 전달합니다.
        
        **title**: str : required **(필수)** : 기사의 제목 입니다.

        **contents**: str : required **(필수)** : 기사의 본문 입니다. ( 태그가 존재 하면 안됩니다. )

        # Output Arguments
        ``` json
        {
            "extractor":  "한줄요약"
        }        
        ```
        """

        r = None
        # atlog = AuditLog('[AAA] Login checking')
        try:
            log.wirte_log('asiatimes', request)
            args = reqFormat.parse_data(request)
            #pprint(args)

            if len(args['title']) == 0 and len(args['contents']) == 0:
                r = {"success": False, "message": "NO INPUT"}
                return make_response(r)

            t = args['title']
            c = args['contents']
            c = reqFormat.parse_content('asiatimes', c)
            #c = 'Giberish'

            gpt = Senti_inferer_API.inference(t, c)
            #print(gpt)
            r = {"success": True, "extractor": gpt}

        except Exception as exp:
            r = {"success": False, "message": str(exp)}
        finally:
            return make_response(r)
################################################################################

################################################################################
@AsiaTimes.route('/GPT-summarizer')
class GPT_summarizer(Resource):
    @AsiaTimes.doc(parser=asia_req)
    @AsiaTimes.response(200, 'API Success/Failure', asia_res)
    @AsiaTimes.response(400, 'Failure')
    @AsiaTimes.response(500, 'Error')
    def post(self):
        """
        요약문 생성(GPT2) API 입니다.
        
        ## Input Arguments 를 JSON 형식으로 전달합니다.
        
        **title**: str : required **(필수)** : 기사의 제목 입니다.

        **contents**: str : required **(필수)** : 기사의 본문 입니다. ( 태그가 존재 하면 안됩니다. )
        
        # Output Arguments
        ``` json
        {
            "extractor": "집단감염 우려 속에 서울 도심에서 강행된 광복절 집회에서 경찰에 폭력을 행사하는 등 공무집행을 방해한 참가자 2명이 18일 오후 구속심사를 받기 위해 법원에 출석했다. 2명 중 1명은 지난달 국회를 방문한 문재인 대통령을 향해 신발을 던졌던 정창옥(57)씨다. 그는 현행범으로 체포돼 경찰에서 조사를 받았다. 오후 2시 35분께 법원 앞에 모습을 드러낸 정씨는 '두 번째 영장심사인데 심경은 어떤가'라는 취재진 질문에 \"담담하다, 괜찮다\"며 \"왜 구속이 됐는지 모르겠고, 그냥 평화적으로 청와대로 가는 사람을 붙잡았다."
        }        
        ```
        """

        r = None
        # atlog = AuditLog('[AAA] Login checking')
        try:
            log.wirte_log('asiatimes', request)
            args = reqFormat.parse_data(request)
            #pprint(args)

            if len(args['title']) == 0 and len(args['contents']) == 0:
                r = {"success": False, "message": "NO INPUT"}
                return make_response(r)

            t = args['title']
            c = args['contents']
            c = reqFormat.parse_content('asiatimes', c)

            gpt = KoGPT2_inferer_API.inference_SUMMARAZATION(t, c)
            gpt = gpt.split("요약하자면,")[-1]
            gpt = gpt.replace('</s>', '')
            #print(gpt)
            r = {"success": True, "extractor": gpt}

        except Exception as exp:
            r = {"success": False, "message": str(exp)}
        finally:
            return make_response(r)  
################################################################################
@AsiaTimes.route('/bert')
class bert(Resource):
    @AsiaTimes.doc(parser=asia_req)
    @AsiaTimes.response(200, 'API Success/Failure', asia_res)
    @AsiaTimes.response(400, 'Failure')
    @AsiaTimes.response(500, 'Error')
    def post(self):
        """
        객체명 추출 API 입니다.

        **http://192.168.0.118:8432/konkesite/**

        # Input Arguments 를 JSON 형식으로 전달합니다.
        **title**: str : required **(필수)** : 기사의 제목 입니다.

        **contents**: str : required **(필수)** : 기사의 본문 입니다. ( 태그가 존재 하면 안됩니다. )

        # Output Arguments
        ``` json
        {
            "extractor":  "한줄요약"
        }        
        ```
        """

        r = None
        # atlog = AuditLog('[AAA] Login checking')
        try:
            log.wirte_log('asiatimes', request)
            args = reqFormat.parse_data(request)
            pprint(args)

            if len(args['title']) == 0 and len(args['contents']) == 0:
                r = {"success": False, "message": "NO INPUT"}
                return make_response(r)

            t = args['title']
            c = args['contents']
            c = reqFormat.parse_content('asiatimes', c)

            # t = re.sub(r'\(.*?\)|\[.*?\]|\{.*?\}|\<.*?\>', '', args['title'])
            # c = re.sub(r'\(.*?\)|\[.*?\]|\{.*?\}|\<.*?\>', '', args['contents'])

            bert = KoBERT_inferer_API.ner_infer(t, c)
            #print(bert)
            r = {"success": True, "extractor":  bert}

        except Exception as exp:
            r = {"success": False, "message": str(exp)}
        finally:
            return make_response(r)
################################################################################

################################################################################
@AsiaTimes.route('/textrank')
class textrank(Resource):
    @AsiaTimes.doc(parser=asia_req)
    @AsiaTimes.response(200, 'API Success/Failure', asia_res)
    @AsiaTimes.response(400, 'Failure')
    @AsiaTimes.response(500, 'Error')
    def post(self):
        """
        본문 요약(TFIDF) API 입니다.

        **http://192.168.0.118:8432/konkesite/**

        # Input Arguments 를 JSON 형식으로 전달합니다.

        **contents**: str : required **(필수)** : 기사의 본문 입니다. ( 태그가 존재 하면 안됩니다. )

        # Example
        ``` json
        {
            "contents" : "집단감염 우려 속에 서울 도심에서 강행된 광복절 집회에서 경찰에 폭력을 행사하는 등 공무집행을 방해한 참가자 2명이 18일 오후 구속심사를 받기 위해 법원에 출석했다.\\n
        2명 중 1명은 지난달 국회를 방문한 문재인 대통령을 향해 신발을 던졌던 정창옥(57)씨다. 정씨는 당시 구속 위기를 면했지만 이번엔 집회에서 경찰을 폭행한 혐의로 다시 구속 갈림길에 섰다.\\n
        서울중앙지법 최창훈 영장전담 부장판사는 이날 오후 3시부터 공무집행방해 등 혐의를 받는 정씨의 구속 전 피의자 심문(영장실질심사)을 진행한다.\\n
        정씨는 지난 15일 광화문 광장에서 열린 광복절 집회에 참여해 청와대 방면으로 이동하던 중 이를 저지하는 경찰관을 폭행한 혐의를 받는다. 그는 현행범으로 체포돼 경찰에서 조사를 받았다.\\n
        오후 2시 35분께 법원 앞에 모습을 드러낸 정씨는 '두 번째 영장심사인데 심경은 어떤가'라는 취재진 질문에 \\"담담하다, 괜찮다\\"며 \\"왜 구속이 됐는지 모르겠고, 그냥 평화적으로 청와대로 가는 사람을 붙잡았다. 그것에 대해서 항거할 것\\"이라고 답했다.\\n
        경찰에게 폭력을 행사했다는 혐의에 대해서는 \\"전혀 한 적 없다\\"며 \\"(정부가) 저를 표적으로 삼았다\\"고 말했다.\\n
        정씨는 국민에게 한마디를 해 달라는 한 유튜버의 요청을 받고 \\"자유대한민국은 살아 있다. 끝까지 함께하겠다\\"고 말하며 발걸음을 옮겼다.\\n
        이날 정씨의 출석 직후 정씨 아들이 대표를 맡은 비영리단체 '긍정의 힘' 관계자들은 법원 앞에서 기자회견을 열고 정씨의 구속이 부당하다는 취지로 주장했다.\\n"
        }
        ```

        # Output Arguments
        ``` json
        {
            "extractor": "집단감염 우려 속에 서울 도심에서 강행된 광복절 집회에서 경찰에 폭력을 행사하는 등 공무집행을 방해한 참가자 2명이 18일 오후 구속심사를 받기 위해 법원에 출석했다.
	정씨는 당시 구속 위기를 면했지만 이번엔 집회에서 경찰을 폭행한 혐의로 다시 구속 갈림길에 섰다.
	경찰에게 폭력을 행사했다는 혐의에 대해서는 \"전혀 한 적 없다\"며 \" 저를 표적으로 삼았다\"고 말했다."
        }        
        ```
        """

        r = None
        # atlog = AuditLog('[AAA] Login checking')
        try:
            log.wirte_log('asiatimes', request)
            args = reqFormat.parse_data(request)
            #pprint(args)

            if len(args['contents']) == 0:
                r = {"success": False, "message": "NO INPUT"}
                return make_response(r)

            c = args['contents']
            c = reqFormat.parse_content('asiatimes', c)

            textrank = TextRank()
            gpt = textrank.summerizer(c, 5)
            #print(gpt)
            r = {"success": True, "extractor":  gpt}

        except Exception as exp:
            r = {"success": False, "message": str(exp)}
        finally:
            return make_response(r)
################################################################################

################################################################################
@AsiaTimes.route('/person-info')
class person_info(Resource):
    @AsiaTimes.doc(parser=asia_req)
    @AsiaTimes.response(200, 'API Success/Failure', asia_res)
    @AsiaTimes.response(400, 'Failure')
    @AsiaTimes.response(500, 'Error')
    def post(self):
        """
        인물 정보.

        **http://192.168.0.118:8432/konkesite/**

        # Input Arguments 를 JSON 형식으로 전달합니다.

        **name**: required **(필수)** 

        # Example
        ``` json
        {
        "name" : ["문재인"]
        }
        ```

        # Output Arguments
        ``` json
        {
        "extractor": "문재인 대통령`\\n출생 : 1953년 1월 24일\\n소속 : 대한민국 (대통령)\\n경력 : 제19대 대한민국 대통령"
        }       
        ```
        """

        #r = None
        r = {"extractor": "NO MATCH WAS FOUND"}
        #r = {"name": "NO MATCH WAS FOUND"}

        try:
            log.wirte_log('asiatimes', request)
            args = reqFormat.parse_data(request)
            print(args)
            c = args['name']
            c = reqFormat.parse_content('asiatimes', c)
            #c = args['extractor']
            ret = Person_inferer_API.inference(c)
            print(ret)

            r = {"success": True, "extractor":  ret}

        except Exception as exp:
            r = {"success": False, "message": str(exp)}
        finally:
            return make_response(r)
################################################################################

################################################################################
@AsiaTimes.route('/naver-dict')
class NAVER_DICT(Resource):
    @AsiaTimes.doc(parser=asia_req)
    @AsiaTimes.response(200, 'API Success/Failure', asia_res)
    @AsiaTimes.response(400, 'Failure')
    @AsiaTimes.response(500, 'Error')

    def post(self):
    
        """
        # Example
        ``` json
        {
            "name":  ["해운대","서울역"]
        }
        ```
        """

        r = None
        try:
            log.wirte_log('asiatimes', request)
            display = 3
            names = request.json['name']
            displayChk = "display" in request.json
            if displayChk :
                display = request.json['display']

            if names in (None, '') :
                r = {"success": False,"message":"검색어는 필수 입니다."}
            else :
                res = NAVERAPI.SEARCH_DICT(names, display)
                r = {"success": False, "message": "결과값이 존재 하지 않습니다."} if res is None else res

        except Exception as exp:
            r = {"success": False, "message": str(exp)}
        finally:
            return make_response(r)
################################################################################