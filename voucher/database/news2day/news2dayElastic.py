######ONLY FOR LOCAL TEST##########
import sys
from time import strptime

from soupsieve import escape
sys.path.append("d:\\apix\\")
###################################

from voucher.database.LoadElastic import LoadElastic
from datetime import datetime
from elasticsearch import Elasticsearch

loadElastic = LoadElastic()

class News2dayElastic:
    def __init__(self):
        self.type, self.query, self.sdate, self.edate = "", "", "", ""
        self.ecnt, self.scnt, self.gcnt = 0, 0, 0
        
    def searchByEsg(self, index, body, ESG):
        result = {"success": True, "result": []}
        try:
            returnList, totalCnt, lastStatus = [], 0, None
            for esg in list(ESG):
                ESG_List = []
                
                page = int(self.page) - 1
                display = int(self.display)
                
                start = page*display
                end = display
                lastNum = start+end
                
                if esg == "E": totalCnt = self.ecnt 
                if esg == "S": totalCnt = self.scnt
                if esg == "G": totalCnt = self.gcnt
                
                if lastNum >= totalCnt : lastStatus = True
                else: lastStatus = False
                
                ######### DB SQL REFERENCE #########
                # """    
                # SELECT * FROM VOUCHER_NEWS2DAY_ WHERE 1=1
                # AND (MATCH(Title, Article) AGAINST('삼성' IN BOOLEAN MODE))
                # AND TYPE='N'
                # AND Article_Time >= '2022-06-06 00:00:00'
                # AND Article_Time <= '2022-06-08 23:59:59'
                # AND Section_ESG LIKE '%'E'%'
                # ORDER BY Article_Time DESC
                # LIMIT {start}, {end} -- 페이징처리 
                # """
                ####################################
                
                # ESG 검색 조건 추가 
                # 엘라 쿼리문 다솜대리님이랑 재확인 해야함
                # 페이징 처리, 내림차순 DESC 처리 해야함  
                condition = {"match": {"Section_ESG": esg}}
                es_must_list = body['query']['bool']['must']
                es_must_list.append(condition)
                                
                es = loadElastic.es_conn() # 엘라스틱서치 연결
                print("[{}] Elasticsearch Connected for searchByEsg [{}] \n".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), esg))
                searchByEsg_body = body
                res = es.search(index=index, body=searchByEsg_body)

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
                
        except Exception as err:
            print("[{}] SearchByEsg Error: \n".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), err)
        
        finally:
            result["result"] = returnList
            if ESG != "ESG" : result["lastStatus"] = lastStatus
            return result

    def searchCount(self, index, body):
        result = {"success": True, "total": []}
        try:
            pass
            # condition = {
            #                 "aggs": {
            #                     "Section_ESG": {
            #                     "terms": {
            #                         "field": "E"
            #                     }
            #                     },
            #                     "Section_ESG": {
            #                     "terms": {
            #                         "field": "S"
            #                     }
            #                     },
            #                     "Section_ESG":{ 
            #                     "terms": {
            #                         "field": "G"
            #                     }
            #                     }
            #                 }
            #             }
            # body.update(condition)
            # # print(body)
            
            # es = loadElastic.es_conn() # 엘라스틱서치 연결
            # print("[{}] Elasticsearch Connected for searchCount \n".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            # searchCount_body = body
            # res = es.search(index=index, body=searchCount_body)
            # print(res)
            
            # # searchCount_body = {'from': '0', 'size': '10', 'query': {'bool': {'must': [{'range': {'Article_Time': {'gte': '2022-06-07 00:00:00', 'lte': '2022-06-07 23:59:59'}}}], 
            # #         'should': [{'term': {'Title': '제주'}}, {'term': {'Article': '제주'}}, {'match_phrase': {'Title.nori': '제주'}}, 
            # #         {'match_phrase': {'Article.nori': '제주'}}], 'minimum_should_match': 1}}} 
     
            
            ######### DB SQL REFERENCE #########
            # """    
            # SELECT Section_ESG, count(*) FROM VOUCHER_NEWS2DAY_ WHERE 1=1
            # AND (MATCH(Title, Article) AGAINST('삼성' IN BOOLEAN MODE))
            # AND TYPE='N'
            # AND Article_Time >= '2022-06-06 00:00:00'
            # AND Article_Time <= '2022-06-08 23:59:59'
            # GROUP BY Section_ESG
            # """
            ####################################
            
        except Exception as err:
            print("[{}] SearchByEsg Error: \n".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), err)
            result = {"success": False, "message": str(err)}
            
        finally:
            return result 
    
    def searchSenti(self, index, body):
        result = {"success": True, "senti": []}
        try:
            pass
            ######### DB SQL REFERENCE #########
            # """    
            # SELECT AI_Emotion, count(*) FROM VOUCHER_NEWS2DAY_ WHERE 1=1
            # AND (MATCH(Title, Article) AGAINST('삼성' IN BOOLEAN MODE))
            # AND TYPE='N'
            # AND Article_Time >= '2022-06-06 00:00:00'
            # AND Article_Time <= '2022-06-08 23:59:59'
            # GROUP BY AI_Emotion
            # """
            ####################################
            
        except Exception as err:
            print("[{}] SearchByEsg Error: \n".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), err)
            result = {"success": False, "message": str(err)}
            
        finally:
            return result 
    
    def search(self, index, obj):
        result = None
        
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
        self.sdate = obj["sdate"] + " 00:00:00"
        self.edate = obj["edate"] + " 23:59:59"
        self.page = obj["page"]
        self.display = obj["display"]
        self.emotion = obj["emotion"]
        
        es_body =  {   
                        "from": self.page,
                        "size": self.display,
                        "query": {
                                "bool": {
                                    "must": [{"range": {"Article_Time": {"gte": self.sdate, "lte": self.edate}}}],
                                    "should": [{"term": {"Title": self.query}}, {"term": {"Article": self.query}},
                                                {"match_phrase": {"Title.nori": self.query}}, {"match_phrase": {"Article.nori": self.query}}],
                                    "minimum_should_match": 1
                                        }
                                }
                    } 
        
        res = es.search(index=index, body=es_body)
        
        result = self.searchByEsg(index, es_body, obj["esg"])
        display_type = list(obj["esg"])
        
        if len(display_type) != 1:
            cntList = self.searchCount(index, es_body)
            if cntList["success"]:
                result["total"] = cntList["total"]
            
            sentiList = self.searchSenti(index, es_body)
            if sentiList["success"]:
                result["senti"] = sentiList["senti"]
            
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
    print("===========result==========")
    print(result)