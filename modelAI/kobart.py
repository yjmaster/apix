from flask import request, make_response, render_template
from flask_restx import Resource, Namespace

from kobart_modules.inference import kobart_inference_API
kobart_api = kobart_inference_API()

from pytorch_bert_crf_ner.inference import ner_inference_API
ner_api = ner_inference_API()

from analyzer_modules.inference import analyzer_inference_API
analyzer_api = analyzer_inference_API()

from three_modules.inference import three_inference_API
three_api = three_inference_API()

from summary_modules.inference import summary_inference_API
summary_api = summary_inference_API()

Kobart = Namespace(
    name="kobart",
    description="kobart 테스트 API.",
)

@Kobart.route('/title')
class KobartTitle(Resource):
    def post(self):
        """kobart 모델을 통해 제목을 가져옵니다."""
        
        try:
            contents = request.get_json()['contents']
            if len(contents) == 0:
                r = {"success": False, "message": "NO INPUT"}
                return make_response(r)
            contents.replace("/n", "")
            
            title_result = kobart_api.kobart_title(contents)
            
            if title_result == "기사가 너무 깁니다. 줄여주세요":
                r = {"success": False, "message": "기사가 너무 깁니다. 줄여주세요"}
                return make_response(r)
            
            r = {"success": True, "extractor": title_result}
        except Exception as exp:
            r = {"success": False, "message": str(exp)}
        finally:
            return make_response(r)
    
@Kobart.route('/keyword')
class KobartKeyword(Resource):
    def post(self):
        """keyword 알고리즘을 통해 제목을 가져옵니다."""

        try:
            contents = request.get_json()['contents']
            if len(contents) == 0:
                r = {"success": False, "message": "NO INPUT"}
                return make_response(r)
            contents.replace("/n", "")
            
            title_result = kobart_api.kobart_title(contents)
            
            if title_result == "기사가 너무 깁니다. 줄여주세요":
                r = {"success": False, "message": "기사가 너무 깁니다. 줄여주세요"}
                return make_response(r)
            
            ner = ner_api.ner(title_result)
            result = analyzer_api.analyzer(title_result, ner)
            keyword_result = ""
            for i in result:
                keyword_result += i[0] + "/"
            
            keyword_result = keyword_result[:-1]
            
            r = {"success": True, "extractor": keyword_result}
        except Exception as exp:
            r = {"success": False, "message": str(exp)}
        finally:
            return make_response(r)
        
@Kobart.route('/keywordai')
class KobartKeyword(Resource):
    def post(self):
        """kobart 모델을 통해 키워드를 가져옵니다."""

        try:
            contents = request.get_json()['contents']
            if len(contents) == 0:
                r = {"success": False, "message": "NO INPUT"}
                return make_response(r)
            contents.replace("/n", "")
            
            keyword_result = kobart_api.kobart_keyword(contents)
            
            if keyword_result == "기사가 너무 깁니다. 줄여주세요":
                r = {"success": False, "message": "기사가 너무 깁니다. 줄여주세요"}
                return make_response(r)
            
            r = {"success": True, "extractor": keyword_result}
        except Exception as exp:
            r = {"success": False, "message": str(exp)}
        finally:
            return make_response(r)

@Kobart.route('/ner')
class KobartKeyword(Resource):
    def post(self):
        """ner 모델을 통해 개체명을 가져옵니다."""
        try:
            contents = request.get_json()['contents']
            if len(contents) == 0:
                r = {"success": False, "message": "NO INPUT"}
                return make_response(r)
            contents.replace("/n", "")
            
            three_result = three_api.three(contents)
            ner_result = ner_api.ner(three_result)
        
            r = {"success": True, "extractor": ner_result}
        except Exception as exp:
            r = {"success": False, "message": str(exp)}
        finally:
            return make_response(r)
        
@Kobart.route('/summary')
class KobartTitle(Resource):
    def post(self):
        """kobart 모델을 통해 요약을 가져옵니다."""
        
        try:
            contents = request.get_json()['contents']
            if len(contents) == 0:
                r = {"success": False, "message": "NO INPUT"}
                return make_response(r)
            contents.replace("/n", "")
            
            summary_result = summary_api.summary(contents)
            
            if summary_result == "기사가 너무 깁니다. 줄여주세요":
                r = {"success": False, "message": "기사가 너무 깁니다. 줄여주세요"}
                return make_response(r)
            
            r = {"success": True, "extractor": summary_result}
        except Exception as exp:
            r = {"success": False, "message": str(exp)}
        finally:
            return make_response(r)

@Kobart.route('/test')
class KobartTitleTest(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('test.html'),200,headers)
    
@Kobart.route('/keyword/test')
class KobartKeywordTest(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('keyword_test.html'),200,headers)
    
@Kobart.route('/keyword/testai')
class KobartKeywordTest(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('keyword_testai.html'),200,headers)
    
@Kobart.route('/keyword/testner')
class KobartKeywordTest(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('keyword_testner.html'),200,headers)
    
@Kobart.route('/summary/test')
class KobartKeywordTest(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('summary_test.html'),200,headers)