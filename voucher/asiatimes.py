from re import T
from flask import Flask, request, make_response
from flask.globals import request
from flask_restplus import Api, Resource, fields, marshal
from flask_restx import Resource, Api, Namespace, fields
from voucher.util import Util

from voucher.database.asiatimes.LinkDB import LinkDB
from voucher.database.asiatimes.IssueDB import IssueDB
from voucher.database.asiatimes.NewsDB import NewsDB
from voucher.database.asiatimes.CodeDB import CodeDB

Global = Namespace(
    name="Global",
    description="Global API 입니다.",
)

linkDB = LinkDB()
issueDB = IssueDB()
newsDB = NewsDB()
codeDB = CodeDB()


utill = Util()

res_model = Global.model('Global_RES', {
    'success': fields.Boolean(description='API Success/Failure', required=True),
    'message': fields.String(description='Success/Failure message',required=True),
})


# 링크 관리 #
@Global.route('/selectLink')
class selectLink(Resource):
    global_model = Global.model('selectLink_model', {
        'area': fields.String(example=""),
        'idx': fields.String(example="")
    }) 

    @Global.expect(global_model)
    @Global.response(200, 'API Success/Failure', res_model)
    @Global.response(400, 'Failure')
    @Global.response(500, 'Error')

    def post(self):
        """
        등록된 링크 검색 API 입니다.

        ### area / idx 값이 "" 이면 전체 링크를 가져옵니다
        **area** : 나라 권역 이름
        **idx** : 링크 ID

        ### 없으면 자동으로 넣어주는 키와 값
        **col** : 소팅할 컬럼 이름 default "date"
        **order** : 소팅 순서 default "desc"

        # Output Arguments
        ``` json
        {
        "success": true,
        "list": [
                {
                    "idx": ,
                    "area": "",
                    "link": "",
                    "date": ""
                }
            ]
        }
     
        ```
        """

        result = None
        try:
            params = request.get_json()
            required = {"area":"", "idx":"", "col":"date", "order":"desc"}
            refineParams = utill.validationCheck(params, required)

            #print("== validation result ==")
            #print(refineParams, end="\n\n")

            if refineParams["success"] : 
                newParams = refineParams["params"]
                selected = linkDB.SELECT(newParams)
                result = {"success": True, "list": selected}

            else : result = refineParams

        except Exception as exp:
            result = {"success": False, "message": str(exp)}
        finally:
            #print("== result== ")
            #print(result, end="\n\n")
            return result

@Global.route('/insertLink')
class insertLink(Resource):

    global_model = Global.model('insertLink_Model', {
        'area': fields.String(example="아시아"),
        'link': fields.String(example="www.naver.com"),
        'desc': fields.String(example="네이버 입니다.")
    }) 

    @Global.expect(global_model)
    
    @Global.response(200, 'API Success/Failure', res_model)
    @Global.response(400, 'Failure')
    @Global.response(500, 'Error')

    def post(self):
        """
        링크 등록 API 입니다.

        **area** : 나라 권역 이름(required)
        **link** : 링크 (required)
        **desc** : 링크 관련 설명

        # Output Arguments
        ``` json
        { "success": true }
     
        ```
        """

        result = None
        try:
            params = request.get_json()
            required = {'area':True, 'link':True, 'desc':""}
            refineParams = utill.validationCheck(params, required)
     
            #print("== validation result ==")
            #print(refineParams, end="\n\n")

            if refineParams["success"] : 
                newParams = refineParams["params"]
                duplicateParams = utill.duplicationCheck(newParams, "global_link", "link")
                
                if duplicateParams["success"] :
                    inesrt_result = linkDB.INSERT(newParams)
                    if inesrt_result : result = inesrt_result
                else : result = duplicateParams
                    
            else : result = refineParams

        except Exception as exp:
            result = {"success": False, "message": str(exp)}
        finally:
            #print("== result== ")
            #print(result, end="\n\n")
            return result

@Global.route('/updateLink')
class updateLink(Resource):

    global_model = Global.model('updateLink_Model', {
        'idx': fields.String(example="104"),
        'desc': fields.String(example="설명입니다.")
    }) 

    @Global.expect(global_model)
    
    @Global.response(200, 'API Success/Failure', res_model)
    @Global.response(400, 'Failure')
    @Global.response(500, 'Error')

    def post(self):
        """
        링크 설명 수정 API 입니다.

        # Output Arguments
        ``` json
        { "success": true }
     
        ```
        """

        result = None
        try:
            params = request.get_json()
            required = {'idx':True, 'desc':''}
            refineParams = utill.validationCheck(params, required)
     
            #print("== validation result ==")
            #print(refineParams, end="\n\n")

            if refineParams["success"] : 
                newParams = refineParams["params"]

                update_result = linkDB.UPDATE(newParams)
                if update_result : result = update_result

            else : result = refineParams

        except Exception as exp:
            result = {"success": False, "message": str(exp)}
        finally:
            #print("== result== ")
            #print(result, end="\n\n")
            return result

@Global.route('/deleteLink')
class deleteLink(Resource):

    global_model = Global.model('deleteLink_Model', {
        'idx': fields.String(example="97")
    }) 

    @Global.expect(global_model)
    
    @Global.response(200, 'API Success/Failure', res_model)
    @Global.response(400, 'Failure')
    @Global.response(500, 'Error')

    def post(self):
        """
        링크 삭제 API 입니다.

        ※기존 링크 삭제 금지

        **idx** : 링크 ID (required)

        # Output Arguments
        ``` json
        { "success": true }
     
        ```
        """

        result = None
        try:
            params = request.get_json()
            required = {'idx':True}
            refineParams = utill.validationCheck(params, required)
     
            #print("== validation result ==")
            #print(refineParams, end="\n\n")

            if refineParams["success"] : 
                newParams = refineParams["params"]

                delete_result = linkDB.DELETE(newParams)
                if delete_result : result = delete_result

            else : result = refineParams

        except Exception as exp:
            result = {"success": False, "message": str(exp)}
        finally:
            #print("== result== ")
            #print(result, end="\n\n")
            return result

# 이슈 관리 #
@Global.route('/selectIssue')
class selectIssue(Resource):

    global_model = Global.model('selectIssue_Model', {
        'area': fields.String(example=""),
        'idx': fields.String(example="")
    }) 

    @Global.expect(global_model)
    
    @Global.response(200, 'API Success/Failure', res_model)
    @Global.response(400, 'Failure')
    @Global.response(500, 'Error')

    def post(self):
        """
        등록된 이슈 검색 API 입니다.

        ### area / idx 값이 "" 이면 전체 이슈를 가져옵니다
        **area** : 나라 권역 이름
        **idx** : 이슈 ID

        ### 없으면 자동으로 넣어주는 키와 값
        **col** : 소팅할 컬럼 이름 default "date"
        **order** : 소팅 순서 default "desc"

        # Output Arguments
        ``` json
        {
        "success": true,
        "list": [
            {
                "idx": ,
                "keyword": "",
                "date": "",
                "area": "",
                "code": "",
                "links": []
            }
        ]
     
        ```
        """

        result = None
        try:
            params = request.get_json()
            required = {"area":"", "idx":"", "col":"date", "order":"desc"}
            refineParams = utill.validationCheck(params, required)

            #print("== validation result ==")
            #print(refineParams, end="\n\n")

            if refineParams["success"] : 
                newParams = refineParams["params"]
                selected = issueDB.SELECT(newParams)
                result = {"success": True, "list": selected}

            else : result = refineParams

        except Exception as exp:
            result = {"success": False, "message": str(exp)}
        finally:
            #print("== result== ")
            #print(result, end="\n\n")
            return result

@Global.route('/insertIssue')
class insertIssue(Resource):

    global_model = Global.model('insertIssue_Model', {
        'keyword': fields.String(example="SpaceX"),
        'area': fields.String(example="북미"),
        'link': fields.String(example="[46,47,48,49]")
    }) 

    @Global.expect(global_model)
    
    @Global.response(200, 'API Success/Failure', res_model)
    @Global.response(400, 'Failure')
    @Global.response(500, 'Error')

    def post(self):
        """
        이슈 등록 API 입니다.

        **keyword** : 이슈 키워드 (required)
        **area** : 나라 권역 이름 (required)
        **link** : 링크 (required)

        # Output Arguments
        ``` json
        { "success": true }
     
        ```
        """

        result = None
        try:
            params = request.get_json()
            required = {'keyword':True, 'area':True, 'link':True}
            refineParams = utill.validationCheck(params, required)

            #print("== validation result ==")
            #print(refineParams, end="\n\n")

            if refineParams["success"] : 
                newParams = refineParams["params"]
                inesrt_result = issueDB.INSERT(newParams)
                if inesrt_result : result = inesrt_result
         
            else : result = refineParams

        except Exception as exp:
            result = {"success": False, "message": str(exp)}
        finally:
            #print("== result== ")
            #print(result, end="\n\n")
            return result

@Global.route('/updatetIssue')
class updatetIssue(Resource):

    global_model = Global.model('updatetIssue_Model', {
        'idx': fields.String(example="45"),
        'link': fields.String(example="[46,47,48,50]")
    }) 

    @Global.expect(global_model)
    
    @Global.response(200, 'API Success/Failure', res_model)
    @Global.response(400, 'Failure')
    @Global.response(500, 'Error')

    def post(self):
        """
        이슈 링크 수정 API 입니다.

        **idx** : 이슈 ID (required)
        **link** : 링크 ID (required)

        # Output Arguments
        ``` json
        { "success": true }
     
        ```
        """

        result = None
        try:
            params = request.get_json()
            required = {'idx':True, 'link':True}
            refineParams = utill.validationCheck(params, required)
     
            #print("== validation result ==")
            #print(refineParams, end="\n\n")

            if refineParams["success"] : 
                newParams = refineParams["params"]
                update_result = issueDB.UPDATE(newParams)
                if update_result : result = update_result
         
            else : result = refineParams

        except Exception as exp:
            result = {"success": False, "message": str(exp)}
        finally:
            #print("== result== ")
            #print(result, end="\n\n")
            return result

@Global.route('/deletetIssue')
class deletetIssue(Resource):

    global_model = Global.model('deletetIssue_Model', {
        'idx': fields.String(example="45")
    }) 

    @Global.expect(global_model)
    
    @Global.response(200, 'API Success/Failure', res_model)
    @Global.response(400, 'Failure')
    @Global.response(500, 'Error')

    def post(self):
        """
        이슈 삭제 API 입니다.

        ※기존 이슈 삭제 금지 (기사도 같이 삭제됨)
        **idx** : 이슈 ID (required)

        # Output Arguments
        ``` json
        { "success": true }
     
        ```
        """

        result = None
        try:
            params = request.get_json()
            required = {'idx':True}
            refineParams = utill.validationCheck(params, required)
     
            #print("== validation result ==")
            #print(refineParams, end="\n\n")

            if refineParams["success"] : 
                newParams = refineParams["params"]

                delete_news_result = newsDB.DELETE(newParams)
                if delete_news_result["success"] :
                    #print("기사 삭제 완료")
                    delete_issue_result = issueDB.DELETE(newParams)
                    if delete_issue_result["success"] : 
                        #print("이슈 삭제 완료")
                        result = delete_issue_result
            
            else : result = refineParams

        except Exception as exp:
            result = {"success": False, "message": str(exp)}
        finally:
            #print("== result== ")
            #print(result, end="\n\n")
            return result

# 뉴스 관리 #
@Global.route('/selectNews')
class selectNews(Resource):

    global_model = Global.model('selectNews_Model', {
        'area': fields.String(example="아시아"),
        'keyword': fields.String(example="taliban"),
        'sdate': fields.String(example="2021-09-17"),
        'edate': fields.String(example="2021-09-23"),
        'senti' : fields.String(example=""),
        'page': fields.String(example="1"),
        'display': fields.String(example="5")
    }) 

    @Global.expect(global_model)
    
    @Global.response(200, 'API Success/Failure', res_model)
    @Global.response(400, 'Failure')
    @Global.response(500, 'Error')

    def post(self):
        """
        뉴스 검색 API 입니다.

        **area** : 나라 권역 이름 (required)
        **keyword** : 이슈 키워드 (required)
        **sdate** : 시작 날짜 (required)
        **edate** : 종료 날짜 (required)
        **senti** : 감성점수 ("" : 전체기사)
        **page** : 시작 페이지 (default 1)
        **display** : 한 페이지에 보여줄 갯수 (default 5)

        # Output Arguments
        ``` json
        {
            "success": ,
            "list": [
                {
                    "idx": ,
                    "title": "",
                    "summary": "",
                    "image": "",
                    "link": "",
                    "upload_date": "",
                    "keyword": "",
                    "area": "",
                    "insert_date": "",
                    "senti": "" 
                }
            ],
            "lastResult": ,
            "totalCount": 
        ```
        """

        result = None
        try:
            params = request.get_json()
            required = {'area':True, 'keyword':True, 'sdate':True, 'edate':True, 'senti':"", 'page':1, 'display':5}
            refineParams = utill.validationCheck(params, required)

            #print("== validation result ==")
            #print(refineParams, end="\n\n")

            if refineParams["success"] : 
                lastStatus = None
                page = int(params["page"]) - 1
                display = int(params["display"])

                start = page*display
                end = display

                newParams = refineParams["params"]
                senti_list = newsDB.SELECTCNT(newParams)
                totalCnt = 0
                for obj in senti_list:
                    totalCnt+=obj["cnt"]
                
                selected = newsDB.SELECT(newParams, start, end)

                lastNum = start+end
    
                if lastNum >= totalCnt : lastStatus = True
                else: lastStatus = False

                result = {"success": True, "list": selected,
                    "lastResult": lastStatus, "totalCount": totalCnt,
                    "senti":senti_list}

            else : result = refineParams

        except Exception as exp:
            result = {"success": False, "message": str(exp)}
        finally:
            #print("== result== ")
            #print(result, end="\n\n")
            return result

@Global.route('/deleteNews')
class deleteNews(Resource):

    @Global.response(200, 'API Success/Failure', res_model)
    @Global.response(400, 'Failure')
    @Global.response(500, 'Error')

    def post(self):
        """
        뉴스 삭제 API 입니다.
        
        1주일치 뉴스만 보관하므로 1주일이 지나면 자동 삭제됩니다. 

        # Output Arguments
        ``` json

        ```
        """

        result = None
        try:
            delete_news_result = newsDB.DELETE()
            if delete_news_result["success"] :
                result = delete_news_result

        except Exception as exp:
            result = {"success": False, "message": str(exp)}
        finally:
            #print("== result== ")
            #print(result, end="\n\n")
            return result











 

