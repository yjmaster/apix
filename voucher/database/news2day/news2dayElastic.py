######ONLY FOR LOCAL TEST##########
import enum
import sys
import pandas as pd
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

                # ESG 검색 조건 추가 
                esg_query = {"match": {"Section_ESG": "ESG "+esg}}
                body_must_list = body['query']['bool']['must']
                body_must_list.append(esg_query)
                
                # 감성 검색 조건 추가
                if self.emotion != "":
                    senti_query = {"match": {"AI_Emotion": self.emotion}}
                    body_must_list.append(senti_query)

                es = loadElastic.es_conn() # 엘라스틱서치 연결
                # print("[{}] Elasticsearch Connected for searchByEsg [{}] \n".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), esg))
                # print("body : ", body)
                res = es.search(index=index, body=body)
                
                for idx, row in enumerate(res['hits']['hits']):
                    row = row['_source']
                    
                    ESG_List.append({
                        "press": str(row['PRESS']),
                        "title": str(row['Title']),
                        "url": str(row['URL']),
                        "emotion": str(row['AI_Emotion']),
                        "esg": str(row['Section_ESG']),
                        "img": str(row['IMGURL'])
                    })
                
                ESG_Result = {"type": esg, "list": ESG_List}
                returnList.append(ESG_Result) 
                
                if self.emotion != "": # ESG 감성지수 파이차트 조각 클릭
                    del body_must_list[2:]

                display_type = list(obj["esg"])
                if len(display_type) != 1:
                    del body_must_list[2:3]

        except Exception as err:
            print("[{}] SearchByEsg Error: \n".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), err)
        
        finally:
            result["result"] = returnList
            return result
            
    def searchCount(self, index, body):
        result = {"success": True, "total": []}
        try: 
            condition = {
                "aggs": {
                    "Section_ESG": {
                        "terms": {"field": "Section_ESG.keyword"}
                    }
                }
            }
            if 'aggs' in body: del body['aggs']
            body.update(condition)
            
            if self.emotion != "":
                body_must_list = body['query']['bool']['must']
                senti_query = {"match": {"AI_Emotion": self.emotion}}
                body_must_list.append(senti_query)

            es = loadElastic.es_conn() # 엘라스틱서치 연결
            # print("[{}] Elasticsearch Connected for searchCount \n".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            # print("searchCount : ", body)

            res = es.search(index=index, body=body)
            e_cnt, s_cnt, g_cnt, esg_cnt  = 0, 0, 0, 0
            for idx, row in enumerate(res['aggregations']['Section_ESG']['buckets']):
                if row['key'] == "E": e_cnt = row['doc_count']
                if row['key'] == "S": s_cnt = row['doc_count']
                if row['key'] == "G": g_cnt = row['doc_count']
                if row['key'] == "ESG": esg_cnt = row['doc_count']

            result["total"].append({"e_cnt" : e_cnt + esg_cnt})
            result["total"].append({"s_cnt" : s_cnt + esg_cnt})
            result["total"].append({"g_cnt" : g_cnt + esg_cnt})

        except Exception as err:
            print("[{}] SearchCount Error: \n".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), err)
            result = {"success": False, "message": str(err)}
            
        finally:
            return result 
            
    def searchSenti(self, index, body):
        result = {"success": True, "senti": []}
        try:
            condition = {
                "aggs": {
                    "genres_and_products": {
                        "multi_terms": {
                            "terms": [
                                {"field": "AI_Emotion.keyword"},
                                {"field": "Section_ESG.keyword"}
                            ]
                        }
                    }
                }
            }
            if 'aggs' in body: del body['aggs']
            body.update(condition)

            es = loadElastic.es_conn() # 엘라스틱서치 연결
            # print("[{}] Elasticsearch Connected for searchSenti \n".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            # print("body : ", body)
            res = es.search(index=index, body=body)

            sentiObj = {"level":[], "cnt":[]}
            for idx, row in enumerate(res['aggregations']['genres_and_products']['buckets']):
                sentiKey = row['key'][0]
                esgKey = row['key'][1]
                if esgKey != "ESG":
                    sentiObj["level"].append(sentiKey)
                    sentiObj["cnt"].append(row['doc_count'])
                else:
                    sentiObj["level"].append(sentiKey)
                    sentiObj["cnt"].append(row['doc_count']*3)
                    
            df = pd.DataFrame((sentiObj), columns=['level','cnt'])
            report = df.groupby(["level"]).sum().to_dict()
            for key, value in report["cnt"].items():
                result["senti"].append({"level": key, "cnt": value})

        except Exception as err:
            print("[{}] SearchSenti Error: \n".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), err)
            result = {"success": False, "message": str(err)}
        finally:
            return result 

    def search(self, index, obj):
        result = None
        try:
            es = loadElastic.es_conn() # 엘라스틱서치 연결
            # print("[{}] Elasticsearch Connected for search \n".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            
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

            body = {
                "from": self.page,
                "size": self.display,
                "sort": [{"Article_Time": {"order": "desc"}}],
                "query": {
                    "bool": {
                        "must": [
                            {"range": {"Article_Time": {"gte": self.sdate, "lte": self.edate}}},
                            {"match_phrase": {"TYPE.keyword": self.type}}
                        ],
                        "should": [
                            {"term": {"Title": self.query}},
                            {"term": {"Keywords": self.query}},
                            {"match_phrase": {"Title.nori": self.query}},
                            {"match_phrase": {"Keywords.nori": self.query}}
                        ],
                        "minimum_should_match": 1
                    }
                }
            } 

            # 기사 검색
            result = self.searchByEsg(index, body, obj)

            # ESG 카운드 조회
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