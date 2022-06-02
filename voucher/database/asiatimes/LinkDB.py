from datetime import datetime
from voucher.database.LoadDB import LoadDB
loadDb = LoadDB()
class LinkDB:
    def SELECT(self, obj) :
        try:
            loadDb.DB_CONNECT()
            return_list = []
            _SQL = """SELECT * FROM global_link WHERE 1=1\n"""

            if "area" in obj :
                if obj["area"] != "":
                    _SQL += "AND area = '{}'".format(obj["area"])
            
            if obj["idx"] != "":
                _SQL += "AND idx = '{}'".format(obj["idx"])

            if ("col" in obj) & ("order" in obj):
                _SQL += "ORDER BY `{}` {}".format(obj["col"], obj["order"])

            #print("== CALL SQL ==")
            #print(_SQL, end="\n\n")
            
            with loadDb.conn.cursor() as cursor :
                cursor.execute(_SQL)

            for idx, val in enumerate(cursor) :
                date = val[4].strftime('%Y.%m.%d')
                return_list.append({
                    'idx':val[0],'area': val[1],
                    'link': val[2], 'desc': val[3],
                    'date': date
                })
            return return_list

        finally:
            loadDb.conn.commit()
            loadDb.conn.close()
            cursor.close()

    def INSERT(self, obj) :
        try:
            loadDb.DB_CONNECT()    
            return_list = {"success" : True}
            _SQL = """ INSERT INTO global_link SET
                area = '{area}',
                link = '{link}',
                `desc` = '{desc}',
                date = '{date}'
            """ .format(
                    area = obj["area"],
                    link = loadDb.conn.escape_string(obj["link"]),
                    desc = loadDb.conn.escape_string(obj["desc"]),
                    date = datetime.now()
                )

            #print("== CALL SQL ==")
            #print(_SQL, end="\n\n")

            with loadDb.conn.cursor() as cursor :
                cursor.execute(_SQL)

            return return_list
            
        finally:
            loadDb.conn.commit()
            loadDb.conn.close()
            cursor.close()
    
    def UPDATE(self, obj) :
        try:
            loadDb.DB_CONNECT()
            return_list = {"success" : True}

            _SQL = """ UPDATE global_link SET `desc` = '{}'
                WHERE idx = '{}' """.format(obj["desc"], obj["idx"])

            #print("== CALL SQL ==")
            #print(_SQL)

            with loadDb.conn.cursor() as cursor :
                cursor.execute(_SQL)

            return return_list

        finally:
            loadDb.conn.commit()
            loadDb.conn.close()
            cursor.close()

    def DELETE(self, obj) :
        try:
            loadDb.DB_CONNECT()
            return_list = {"success" : True}
            _SQL = """ DELETE FROM global_link
                WHERE idx = '{idx}' """ .format(idx = obj["idx"])

            #print("== CALL SQL ==")
            #print(_SQL)

            with loadDb.conn.cursor() as cursor :
                cursor.execute(_SQL)

            return return_list

        finally:
            loadDb.conn.commit()
            loadDb.conn.close()
            cursor.close()



    
