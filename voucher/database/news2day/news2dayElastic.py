######ONLY FOR LOCAL TEST##########
import enum
import sys
from time import strptime

from soupsieve import escape
# sys.path.append("d:\\apix\\")
###################################

from voucher.database.LoadElastic import LoadElastic
from datetime import datetime
from elasticsearch import Elasticsearch

loadElastic = LoadElastic()

class News2dayElastic:
    def __init__(self):
        self.type, self.query, self.sdate, self.edate = "", "", "", ""
        self.ecnt, self.scnt, self.gcnt = 0, 0, 0
        
    def searchByEsg(self, index, body, obj):
        result = {"success": True, "result": []}
        try:
            returnList, totalCnt, lastStatus = [], 0, None
            for esg in list(obj["esg"]):
                esg = esg.upper()
                ESG_List = []
                
                page = int(self.page) - 1
                display = int(self.display)
                
                start = page*display
                end = display
                
                # 페이징 처리 
                body['from'] = start
                body['size'] = end
                
                lastNum = start+end
                
                if esg == "E": totalCnt = self.ecnt 
                if esg == "S": totalCnt = self.scnt
                if esg == "G": totalCnt = self.gcnt
                
                if lastNum >= totalCnt : lastStatus = True
                else: lastStatus = False
                
                # ESG 검색 조건 추가 
                condition = {"match": {"Section_ESG": esg}}
                body_must_list = body['query']['bool']['must']
                body_must_list.append(condition)
                
                es = loadElastic.es_conn() # 엘라스틱서치 연결
                print("[{}] Elasticsearch Connected for searchByEsg [{}] \n".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), esg))
                res = es.search(index=index, body=body)
                
                # print("========1. searchByEsg Body============")
                # print(body)
                
                for idx, row in enumerate(res['hits']['hits']):
                    row = row['_source']
                    
                    ESG_List.append({
                        "press": str(row['PRESS']),
                        "title": str(row['Title']),
                        "url": str(row['URL']),
                        "emotion": str(row['AI_Emotion']),
                        "img": str(row['IMGURL'])
                    })
                
                ESG_Result = {"type": esg, "list": ESG_List}
                returnList.append(ESG_Result) 
                
                # 앞서 추가된 조건 {"match": {"Section_ESG": esg}} 삭제 
                if obj["emotion"] : # ESG 감성지수 파이차트 조각 클릭 
                    # del body_must_list[2:]
                    del body_must_list[3:] # ES 검색 조건에 TYPE='G' or 'N' 추가하면서 코드 변경 
    
                else: 
                    # del body_must_list[1:2] 
                    del body_must_list[2:3] # ES 검색 조건에 TYPE='G' or 'N' 추가하면서 코드 변경 
                
        except Exception as err:
            print("[{}] SearchByEsg Error: \n".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), err)
        
        finally:
            result["result"] = returnList
            if obj["esg"] != "ESG" : result["lastStatus"] = lastStatus
            return result
            
    def searchCount(self, index, body):
        result = {"success": True, "total": []}
 
        try: 
            condition = {"aggs": 
                            {"Section_ESG": {
                                    "terms": {"field": "Section_ESG.keyword"}}}
                        }

            body_must_list = body['query']['bool']['must']
            # del body_must_list[2:4] # searchByEsg 에서 추가했던 {"match": {"Section_ESG": esg}} 조건 삭제 -> 다시 확인해보니 불필요하여 주석처리 
            body.update(condition) # searchCount 조건 추가 
            
            # print("=============2. searchCount Body==============")
            # print(body)
        
            es = loadElastic.es_conn() # 엘라스틱서치 연결
            print("[{}] Elasticsearch Connected for searchCount \n".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            res = es.search(index=index, body=body)
            
            e_cnt, s_cnt, g_cnt = 0, 0, 0
            for idx, row in enumerate(res['aggregations']['Section_ESG']['buckets']):
                if "E" in row['key']: e_cnt += row['doc_count']
                if "S" in row['key']: s_cnt += row['doc_count']
                if "G" in row['key']: g_cnt += row['doc_count']
                
            self.ecnt = e_cnt 
            self.scnt = s_cnt
            self.gcnt = g_cnt
            
            result["total"].append({"e_cnt" : e_cnt})
            result["total"].append({"s_cnt" : s_cnt})
            result["total"].append({"g_cnt" : g_cnt})
            
        except Exception as err:
            print("[{}] SearchCount Error: \n".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), err)
            result = {"success": False, "message": str(err)}
            
        finally:
            return result 
            
    def searchSenti(self, index, body):
        result = {"success": True, "senti": []}
        try:
            condition = {"aggs": 
                            {"AI_Emotion": {
                                    "terms": {"field": "AI_Emotion.keyword"}}}
                        }
            
            del body['aggs'] # searchByEsg 에서 추가했던 조건 삭제 
            body.update(condition) # searchSenti 조건 추가 
            
            es = loadElastic.es_conn() # 엘라스틱서치 연결
            print("[{}] Elasticsearch Connected for searchSenti \n".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            res = es.search(index=index, body=body)
            
            for idx, row in enumerate(res['aggregations']['AI_Emotion']['buckets']):
                result["senti"].append({
                    "level": row['key'], "cnt": row['doc_count']})
            
        except Exception as err:
            print("[{}] SearchSenti Error: \n".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), err)
            result = {"success": False, "message": str(err)}
            
        finally:
            return result 
    
    def search(self, index, obj):
        result = None
        try:
            es = loadElastic.es_conn() # 엘라스틱서치 연결
            print("[{}] Elasticsearch Connected for search \n".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            
            newQuery = ""
            condition = obj["condition"]
            if condition == "OR":
                for idx, query in enumerate(obj["query"]):
                    newQuery += query + (" " if idx != len(obj["query"])-1 else "")
            else :
                for idx, query in enumerate(obj["query"]):
                    newQuery += '"'+query+'"' + ("+" if idx != len(obj['query'])-1 else "")
                        
            self.query = newQuery
            self.type = obj["type"]
            self.sdate = obj["sdate"] + "T00:00:00"
            self.edate = obj["edate"] + "T23:59:59"
            self.page = obj["page"]
            self.display = obj["display"]
            self.emotion = obj["emotion"]
            
            body =  {   
                            "from": self.page,
                            "size": self.display,
                            "sort": [{"Article_Time": {"order": "desc"}}],
                            "query": {
                                    "bool": {
                                        "must": [{"range": {"Article_Time": {"gte": self.sdate, "lte": self.edate}}}, {"match_phrase": {"TYPE.keyword": self.type}}, {"match": {"AI_Emotion": self.emotion}}],
                                        "should": [{"term": {"Title": self.query}}, {"term": {"Article": self.query}},
                                                    {"match_phrase": {"Title.nori": self.query}}, {"match_phrase": {"Article.nori": self.query}}],
                                        "minimum_should_match": 1
                                            }
                                    }
                        } 
            
            # res = es.search(index=index, body=body)

            if self.emotion == "": 
                body_must_list = body['query']['bool']['must']
                # del body_must_list[1]
                del body_must_list[2] # ES 검색 조건에 TYPE='G' or 'N' 추가하면서 코드 변경 
            
            result = self.searchByEsg(index, body, obj)
            display_type = list(obj["esg"])
            
            if len(display_type) != 1:
                cntList = self.searchCount(index, body)
                if cntList["success"]:
                    result["total"] = cntList["total"]
                
                sentiList = self.searchSenti(index, body)
                if sentiList["success"]:
                    result["senti"] = sentiList["senti"]
                    
        except Exception as err:
            print("[{}] ELASTICSEARCH ERROR: \n".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), err)
            result = {"success": False, "message": str(err)}  
        
        finally:
            es.close()
            return result

if __name__ == "__main__":    
    news2dayElastic = News2dayElastic()
    obj = {"type":"N",
            "esg":"ESG",
            "display":"10",
            "page":"1",
            "emotion":"",
            "query":["제주"],
            "sdate":"2022-06-07",
            "edate":"2022-06-07",
            "condition":"OR"}
    index = "voucher_news" # 검색할 인덱스명 - 변경 가능 
    result = news2dayElastic.search(index, obj)
    # print("===========result==========")
    # print(result)