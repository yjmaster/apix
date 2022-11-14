from datetime import datetime
from voucher.database.LoadDB import LoadDB

loadDb = LoadDB()

class HansDB:
    def __init__(self) :
        self.query, self.sdate, self.edate = "", "", ""
        self.ecnt, self.scnt, self.gcnt  = 0, 0, 0

    def SELECT_SENTI(self, _CONDITION):
        result = {"success": True, "senti":[]}
        try:
            _CNT_SQL = "SELECT AI_Emotion, count(*) as cnt FROM _VOUCHER_HANS WHERE 1=1\n"
            _CNT_SQL += _CONDITION
            _CNT_SQL += "GROUP BY AI_Emotion"
   
            #print("== CALL SQL SELECT_SENTI==")
            #print(_CNT_SQL)

            with loadDb.conn.cursor() as cursor :
                cursor.execute(_CNT_SQL)

            for idx, row in enumerate(cursor) :
                result["senti"].append({
                    'level':row[0],'cnt': row[1]
                })

        except Exception as exp:
            result = {"success": False, "message": str(exp)}
        finally:
            return result

    def SELECT_COUNT(self, _CONDITION) :
        result = {"success": True, "total":[]}
        try:
            _CNT_SQL = "SELECT Section_ESG, count(*) FROM _VOUCHER_HANS WHERE 1=1\n"
            _CNT_SQL += _CONDITION
            _CNT_SQL += "GROUP BY Section_ESG"
   
            #print("== CALL SQL SELECT_COUNT ==")
            #print(_CNT_SQL)

            with loadDb.conn.cursor() as cursor :
                cursor.execute(_CNT_SQL)
            
            e_cnt, s_cnt, g_cnt = 0, 0, 0
            for idx, row in enumerate(cursor) :
                if 'E' in row[0] : e_cnt += row[1]
                if 'S' in row[0] : s_cnt += row[1]
                if 'G' in row[0] : g_cnt += row[1]

            self.ecnt = e_cnt
            self.scnt = s_cnt
            self.gcnt = g_cnt

            result["total"].append({"e_cnt":e_cnt})
            result["total"].append({"s_cnt":s_cnt})
            result["total"].append({"g_cnt":g_cnt})
    
        except Exception as exp:
            result = {"success": False, "message": str(exp)}
        finally:
            return result

    def SELECT_BY_ESG(self, _SQL, ESG):
        result = {"success": True, "result":[]}
        try:
            return_list, totalCnt, lastStatus = [], 0, None
            for esg in list(ESG) :
                _E_SQL, _TOTAL_SQL, ESG_LIST = "", "", []

                _E_SQL += "AND Section_ESG LIKE '%{}%'\n".format(esg)
                _E_SQL += "ORDER BY Article_Time DESC\n"

                # caculate limit
                page = int(self.page) - 1
                display = int(self.display)
                
                start = page*display
                end = display

                _E_SQL += "LIMIT {}, {}".format(start, end)
                _TOTAL_SQL = _SQL+_E_SQL

                #print("== CALL SQL SELECT_BY_ESG==")
                #print(_TOTAL_SQL)

                lastNum = start+end

                if esg == "E": totalCnt = self.ecnt
                if esg == "S": totalCnt = self.scnt
                if esg == "G": totalCnt = self.gcnt

                if lastNum >= totalCnt : lastStatus = True
                else :lastStatus = False
                
                with loadDb.conn.cursor() as cursor :
                    cursor.execute(_TOTAL_SQL)

                for idx, row in enumerate(cursor) :
                    ESG_LIST.append({
                        "press": str(row[1]),
                        "title": str(row[2]),
                        "article": str(row[3]),
                        "url": str(row[4]),
                        "emotion": str(row[8]),
                        "img": str(row[11])
                    })

                ESG_RESUT = {"type": esg, "list": ESG_LIST}
                return_list.append(ESG_RESUT)

        except Exception as exp:
            result = {"success": False, "message": str(exp)}
        finally:
            result["result"] = return_list
            if ESG != "ESG" : result["lastStatus"] = lastStatus
            return result

    def SELECT(self, obj) :
        result = None
        try:
            loadDb.DB_CONNECT()

            newQuery = ""
            condition =  obj["condition"]
            if condition == "OR":
                for idx, query in enumerate(obj['query']) :
                    newQuery += query + (" " if idx != len(obj['query'])-1 else "") 
            else :
                newQuery += "+"
                for idx, query in enumerate(obj['query']) :
                    newQuery += '"'+query+'"' + ("+" if idx != len(obj['query'])-1 else "")

            self.query = newQuery
            self.sdate = obj["sdate"]
            self.edate = obj["edate"]
            self.page = obj["page"]
            self.display = obj["display"]
            self.emotion = obj["emotion"]
 
            _SQL = "SELECT * FROM _VOUCHER_HANS WHERE 1=1\n"

            _CONDITION = "AND (MATCH(Title, Article) AGAINST('{}' IN BOOLEAN MODE))\n".format(self.query)
            _CONDITION += "AND Article_Time >= '{} 00:00:00'\n".format(self.sdate)
            _CONDITION += "AND Article_Time <= '{} 23:59:59'\n".format(self.edate)


            if self.emotion != "" :
                _CONDITION += "AND AI_Emotion = '{}'\n".format(self.emotion)
                
            _SQL = _SQL+_CONDITION

            #print("==== SELECT1 ====")
            #print(_SQL)
            #print("==== SELECT1 ====")
            
            result = self.SELECT_BY_ESG(_SQL, obj["esg"])
            display_type = list(obj["esg"])
            #print("display_type")
            #print(display_type)

            if len(display_type) != 1:
                cnt_list = self.SELECT_COUNT(_CONDITION)
                if cnt_list["success"] :
                    result["total"] = cnt_list["total"]
                
                senti_list = self.SELECT_SENTI(_CONDITION)
                if senti_list["success"] :
                    result["senti"] = senti_list["senti"]
 
        except Exception as exp:
            result = {"success": False, "message": str(exp)}
        finally: 
            loadDb.conn.commit()
            loadDb.conn.close()
            return result
