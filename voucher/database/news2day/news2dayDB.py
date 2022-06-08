from voucher.database.LoadDB import LoadDB
from datetime import datetime

loadDb = LoadDB()

class News2dayDB:
    def __init__(self): 
        self.type, self.query, self.sdate, self.edate = "", "", "", ""
        self.ecnt, self.scnt, self.gcnt = 0, 0, 0
        
    def SELECT_BY_ESG(self, _SQL, ESG):
        result = {"success": True, "result": []}
        try:
            returnList, totalCnt, lastStatus = [], 0, None
            for esg in list(ESG) :
                _E_SQL, ESG_LIST = "", []
                
                _E_SQL += "AND Section_ESG LIKE '%{}%'\n".format(esg)
                _E_SQL += "ORDER BY Article_Time DESC\n"
                
                page = int(self.page) - 1
                display = int(self.display)
                
                start = page*display
                end = display
                
                _E_SQL += "LIMIT {}, {}".format(start, end)
                _TOTAL_SQL = _SQL + _E_SQL
                
                lastNum = start+end
                
                if esg == "E": totalCnt = self.ecnt
                if esg == "S": totalCnt = self.scnt
                if esg == "G": totalCnt = self.gcnt
                
                if lastNum >= totalCnt : lastStatus = True
                else: lastStatus = False
                
                with loadDb.conn.cursor() as cursor:
                    cursor.execute(_TOTAL_SQL)
                    
                for idx, row in enumerate(cursor):
                    ESG_LIST.append({
                        "press": str(row[2]),
                        "title": str(row[3]),
                        "url": str(row[5]),
                        "emotion": str(row[9]),
                        "img": str(row[12])
                    })
                    
                ESG_RESULT = {"type": esg, "list": ESG_LIST}
                returnList.append(ESG_RESULT)
                    
        except Exception as err:
            print("[{}] ERROR: \n".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), err)
        
        finally:
            result["result"] = returnList
            if ESG != "ESG" : result["lastStatus"] = lastStatus
            return result
    
    def SELECT_COUNT(self, _CONDITION):
        result = {"success": True, "total":[]}
        
        try: 
            _CNT_SQL = "SELECT Section_ESG, count(*) FROM VOUCHER_NEWS2DAY_ WHERE 1=1\n"
            _CNT_SQL += _CONDITION
            _CNT_SQL += "GROUP BY Section_ESG"
            
            with loadDb.conn.cursor() as cursor:
                cursor.execute(_CNT_SQL)
                
            e_cnt, s_cnt, g_cnt = 0, 0, 0
            for idx, row in enumerate(cursor):
                if "E" in row[0]: e_cnt += row[1]
                if "S" in row[0]: s_cnt += row[1]
                if "G" in row[0]: g_cnt += row[1]
                
            self.ecnt = e_cnt 
            self.scnt = s_cnt
            self.gcnt = g_cnt
            
            result["total"].append({"e_cnt" : e_cnt})
            result["total"].append({"s_cnt" : s_cnt})
            result["total"].append({"g_cnt" : g_cnt})
            
        except Exception as err:
            print("[{}] ERROR: \n".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), err)
            result = {"success": False, "message": str(err)}
            
        finally:
            return result
        
    def SELECT_SENTI(self, _CONDITION):
        result = {"success": True, "senti": []}
        try:
            _CNT_SQL = "SELECT AI_Emotion, count(*) as cnt FROM VOUCHER_NEWS2DAY_ WHERE 1=1\n"
            _CNT_SQL += _CONDITION
            _CNT_SQL += "GROUP BY AI_Emotion"
            
            with loadDb.conn.cursor() as cursor:
                cursor.execute(_CNT_SQL)
                
            for idx, row in enumerate(cursor):
                result["senti"].append({
                    "level": row[0], "cnt": row[1]
                })
            
        except Exception as err:
            print("[{}] ERROR: \n".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), err)
            result = {"success": False, "message": str(err)}
            
        finally:
            return result
        
    def SELECT(self, obj):
        result = None
        # news2day_list = [] # 맨 처음 전체 SELECT 호출 테스트용 
        
        try:
            loadDb.DB_CONNECT()
            
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
            self.sdate = obj["sdate"]
            self.edate = obj["edate"]
            self.page = obj["page"]
            self.display = obj["display"]
            self.emotion = obj["emotion"]
            
            _SQL = "SELECT * FROM VOUCHER_NEWS2DAY_ WHERE 1=1\n"
            
            _CONDITION = "AND (MATCH(Title, Article) AGAINST('{}' IN BOOLEAN MODE))\n".format(self.query)
            _CONDITION += "AND TYPE='{}'\n".format(self.type)
            _CONDITION += "AND Article_Time >= '{} 00:00:00'\n".format(self.sdate)
            _CONDITION += "AND Article_Time <= '{} 23:59:59'\n".format(self.edate)
            
            if self.emotion != "" :
                _CONDITION += "AND AI_Emotion='{}'\n".format(self.emotion)
            
            _SQL += _CONDITION
            
            result = self.SELECT_BY_ESG(_SQL, obj["esg"])
            display_type = list(obj["esg"])
            
            if len(display_type) != 1:
                cntList = self.SELECT_COUNT(_CONDITION)
                if cntList["success"]:
                    result["total"] = cntList["total"]
                
                sentiList = self.SELECT_SENTI(_CONDITION)
                if sentiList["success"]:
                    result["senti"] = sentiList["senti"]
                
            # 맨 처음 전체 SELECT 호출 테스트용 
            # with loadDb.conn.cursor() as cursor: 
            #     cursor.execute(_SQL)
            
            # for idx, row in enumerate(cursor): 
            #     # print("idx:{} / data:{}".format(idx, row))
            #     news2day_list.append({
            #         "press": row[2],
            #         "title": row[3],
            #         "url": row[5],
            #     })
                
        except Exception as err:
            print("[{}] ERROR: \n".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), err)
            result = {"success": False, "message": str(err)}
            
        finally:
            loadDb.conn.commit()
            loadDb.conn.close()
            return result

if __name__ == "__main__":    
    news2day = News2dayDB()
    obj = {"type" : "G"}
    result = news2day.SELECT(obj)
    print("===========result==========")
    print(result)