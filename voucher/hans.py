from flask import Flask, request, make_response
from flask.globals import request
from flask_restplus import Api, Resource, fields, marshal
from flask_restx import Resource, Api, Namespace, fields
from voucher.util import Util
from voucher.database.hans.HansDB import HansDB
import json

ESG = Namespace(
    name="ESG",
    description="ESG API 입니다.",
)

hansDB = HansDB()
utill = Util()

res_model = ESG.model('ESG Res', {
    'success': fields.Boolean(description='API Success/Failure', required=True),
    'message': fields.String(description='Success/Failure message',required=True),
})

@ESG.route('/selectNews')
class selectNews(Resource):

    esg_model = ESG.model('ESG_Model', {
        'query': fields.String(example="삼성전자"),
        'esg': fields.String(example="ESG"),
        'condition': fields.String(example=""),
        'sdate': fields.String(example="2021-07-01"),
        'edate': fields.String(example="2021-08-01"),
        'page': fields.String(example="1"),
        'display': fields.String(example="10"),
        'emotion': fields.String(example="")
    }) 

    @ESG.expect(esg_model)
    
    @ESG.response(200, 'API Success/Failure', res_model)
    @ESG.response(400, 'Failure')
    @ESG.response(500, 'Error')

    def post(self):
        """
        한스 ESG 기사 검색 API 입니다.

        ### page/display값은 ESG 통합검색에서는 사용되지 않습니다. (값 무시)
        ### ESG전체검색에서 ESG별로 TOTAL COUNT가 리턴됩니다.
        ###

        **query** : 검색어 (required)
        **esg** : 분류값 (ESG / "E,S,G" / required)
        **condition** : 조건 (""/"AND"/"OR")
        **sdate** : 시작날짜 (yyyy-mm-dd / required)
        **edate** : 종료날짜 (yyyy-mm-dd / required)

        **page** : 페이지 (default 1 / required)
        **display** : 한페이지내에 보여줄 기사 갯수 (default 10 / required)
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
            "success": true
        }
        ```
        """

        result = None
        try:
            params = request.get_json()
            required = {'query':True, 'esg':True, 'sdate':True, 'edate':True, 'page':1, 'display':5, 'emotion':"" ,'condition':""}
            refineParams = utill.validationCheck(params, required)
            #print("== validation result ==")
            #print(refineParams, end="\n\n")

            if refineParams["success"] : 
                newParams = refineParams["params"]
                result = hansDB.SELECT(newParams)

            else : result = refineParams

        except Exception as exp:
            result = {"success": False, "message": str(exp)}
        finally:
            #print("== result== ")
            #print(result, end="\n\n")
            return result
