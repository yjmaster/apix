from datetime import datetime
from voucher.database.LoadDB import LoadDB
loadDb = LoadDB()
class CodeDB:
    def SELECT(self, obj) :
        try:
            loadDb.DB_CONNECT()
            return_list = []
            _SQL = "SELECT languageCode, countryCode FROM country_code WHERE 1=1"

            if obj["code"] != "":
                _SQL += " AND globalCode = '{}'".format(obj["code"])

            #print("== CALL SQL ==")
            #print(_SQL, end="\n\n")
            
            with loadDb.conn.cursor() as cursor :
                cursor.execute(_SQL)

            for idx, val in enumerate(cursor) :
                return_list.append({
                    'languageCode':val[0],'country_code': val[1]
                })
            return return_list

        finally:
            loadDb.conn.commit()
            loadDb.conn.close()
            cursor.close()



