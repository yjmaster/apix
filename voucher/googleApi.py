import json
from re import T
from flask import Flask, request, make_response
from flask_restplus import Api, Resource, fields, marshal
from flask_restx import Resource, Api, Namespace, fields
from voucher.util import Util
from voucher.googleModule.gse import GSE
from voucher.googleModule.trans import Trans
from voucher.googleModule.keyCrawler import KeyCrawler

from voucher.database.asiatimes.IssueDB import IssueDB
from voucher.database.asiatimes.NewsDB import NewsDB
from voucher.database.asiatimes.CodeDB import CodeDB
from voucher.database.asiatimes.TopIssueDB import TopIssueDB


Google_Api = Namespace(
    name="Google",
    description="Google API 입니다.",
)

issueDB = IssueDB()
newsDB = NewsDB()
codeDB = CodeDB()
topIssueDB = TopIssueDB()

keyCrawler = KeyCrawler()
utill = Util()

gse = GSE(issueDB, newsDB)
trans = Trans()

res_model = Google_Api.model('Google Res', {
    'success': fields.Boolean(description='API Success/Failure', required=True),
    'message': fields.String(description='Success/Failure message',required=True),
})


# 구글 검색 API #
@Google_Api.route('/search')
class search_news(Resource):    

    google_model = Google_Api.model('Google_Api_Search', {
        'idx': fields.String(example="2")
    }) 

    @Google_Api.expect(google_model)
    @Google_Api.response(200, 'API Success/Failure', res_model)
    @Google_Api.response(400, 'Failure')
    @Google_Api.response(500, 'Error')

    def post(self):
        """
        구글 기사 수집 API 입니다.

        등록된 이슈 키워드의 인덱스 번호로 파라미터를 전달합니다.
        현재부터 24시간 전까지의 기사를 수집합니다.
        idx값이 ""이면 현재 등록된 모든 이슈 키워드의 기사를 수집합니다.

        **idx** : DB에 저장된 이슈 키워드의 인덱스

        # Output Arguments
        ``` json

        ```
        """

        result = None
        try:
            params = request.get_json()
            required = {'idx': "", 'area':"", "col":"date", "order":"desc"}

            refineParams = utill.validationCheck(params, required)

            if refineParams["success"] : 
                newParams = refineParams["params"]

                #print("== validation result ==")
                #print(newParams, end="\n\n")

                result = gse.setParameter(newParams)

            else : result = refineParams

        except Exception as exp:
            result = {"success": False, "message": str(exp)}
        finally:
            #print("== result== ")
            #print(result, end="\n\n")
            return result

# 구글 번역 API #
@Google_Api.route('/translate')
class translate(Resource):
    google_model = Google_Api.model('Google_Api_Translate', {
        'text': fields.String(example="The quick brown fox jumped over a lazy dog.")
    }) 

    @Google_Api.expect(google_model)    
    @Google_Api.response(200, 'API Success/Failure', res_model)
    @Google_Api.response(400, 'Failure')
    @Google_Api.response(500, 'Error')

    def post(self):
        """
        구글 번역 API 입니다.


        # Output Arguments
        ``` json

        ```
        """

        result = None
        try:
            params = request.get_json()
            required = {'text': True}
            refineParams = utill.validationCheck(params, required)

            #print("== validation result ==")
            #print(refineParams, end="\n\n")

            if refineParams["success"] :
                newParams = refineParams["params"]
                result = trans.translate(newParams, "en")

            else : result = refineParams
  
        except Exception as exp:
            result = {"success": False, "message": str(exp)}
        finally:
            #print("== result== ")
            #print(result, end="\n\n")
            return result

# 나라별 이슈 키워드 수집하기 *
@Google_Api.route('/setIssueKey')
class setIssueKey(Resource):

    Google_Api_model = Google_Api.model('setIssueKey_Model', {
        'code': fields.String(example=""),
    }) 

    @Google_Api.expect(Google_Api_model)
    @Google_Api.response(200, 'API Success/Failure', res_model)
    @Google_Api.response(400, 'Failure')
    @Google_Api.response(500, 'Error')

    def post(self):
        """
        실시간 나라별 이슈 키워드를 수집합니다.

        '' : 전체 (default)
        AS : 아시아
        NA : 북아메리카/북미
        EU : 유럽
        OC : 오세아니아/호주
        

        **code** : DB에 저장된 권역 코드

        # Output Arguments
        ``` json

        ```
        """

        result = None
        try:
            params = request.get_json()
            required = {'code': ''}
            refineParams = utill.validationCheck(params, required)

            #print("== validation result ==")
            #print(refineParams, end="\n\n")

            if refineParams["success"] : 
                newParams = refineParams["params"]
                delete_result = topIssueDB.DELETE()

                if delete_result["success"] :
                    selected_code = codeDB.SELECT(newParams)

                    for code in selected_code:
                        trans_result = {}
                        trans_keywords = []
                        languageCode = code["languageCode"]
                        countryCode = code["country_code"]
                        url = "https://news.google.com/topstories?hl="+languageCode+"&gl="+countryCode+"&ceid="+countryCode+":"+languageCode
                        keywords = keyCrawler.OPEN_BROWSER(url)
                        trans_obj = {"text": str(keywords)}

                        result = trans.translate(trans_obj, languageCode)
                        if result["success"] :
                            strlist = result["text"]
                            strlist = strlist[1:-1].replace("'","").split(",")
                            for keyword in strlist: 
                                trans_keywords.append(keyword.strip())

                            trans_result["trans"] = trans_keywords
                            trans_result["languageCode"] = languageCode
                            trans_result["countryCode"] = countryCode

                            topIssueDB.INSERT(trans_result)
                            result = {"success": True}

            else : result = refineParams 

        except Exception as exp:
            result = {"success": False, "message": str(exp)}
        finally:
            #print("== result== ")
            #print(result, end="\n\n")
            return result

@Google_Api.route('/getIssueKey')
class getIssueKey(Resource):

    Google_Api_model = Google_Api.model('getIssueKey_Model', {
        'area': fields.String(example="아시아"),
    }) 

    @Google_Api.expect(Google_Api_model)
    @Google_Api.response(200, 'API Success/Failure', res_model)
    @Google_Api.response(400, 'Failure')
    @Google_Api.response(500, 'Error')

    def post(self):
        """
        현재 등록된 나라별 이슈 키워드를 가져 옵니다.

        # Output Arguments
        ``` json

        ```
        """

        result = None
        try:
            params = request.get_json()
            required = {'area': True}
            refineParams = utill.validationCheck(params, required)
 
            #print("== validation result ==")
            #print(refineParams, end="\n\n")

            if refineParams["success"] : 
                newParams = refineParams["params"]
                selected_keyword = topIssueDB.SELECT(newParams)
                result = {"success": True, "list": selected_keyword}

            else : result = refineParams 

        except Exception as exp:
            result = {"success": False, "message": str(exp)}
        finally:
            #print("== result== ")
            #print(result, end="\n\n")
            return result
