from datetime import datetime
from datetime import timedelta
from voucher.database.LoadDB import LoadDB

loadDb = LoadDB()

class TopIssueDB:
    def SELECT_KEYWORD(self, code):

        keyword_list = []
        _SQL = """SELECT
            trans_keyword AS keyaord
            FROM top_keyword
            WHERE countryCode = '{}'""".format(code)
        
        #print("== CALL SQL ==")
        #print(_SQL)

        with loadDb.conn.cursor() as cursor :
            cursor.execute(_SQL)

        for idx, val in enumerate(cursor) :
            keyword_list.append(val[0])
        
        return keyword_list


    def SELECT(self, obj) :
        try:
            loadDb.DB_CONNECT()
            code_list = []

            _SQL = """SELECT countryCode,
                countryName
                FROM country_code
                WHERE globalCode = (
                    SELECT CODE
                    FROM global_code
                    WHERE NAME = "{}"
                )""".format(obj["area"])
                                    
            #print("== CALL SQL ==")
            #print(_SQL)

            with loadDb.conn.cursor() as cursor :
                cursor.execute(_SQL)

            for idx, val in enumerate(cursor) :
                keywords = self.SELECT_KEYWORD(val[0])
                code_list.append({
                    'code':val[0],
                    'name': val[1],
                    'keywords':keywords
                })
                
            return code_list
            
        finally:
            loadDb.conn.commit()
            loadDb.conn.close()
            cursor.close()

    def INSERT(self, keyword_list) :
        try:
            loadDb.DB_CONNECT()
            trans = keyword_list["trans"]
            for idx, word in enumerate(trans) :
            
                _SQL = """ INSERT INTO top_keyword SET
                    trans_keyword = '{trans_keyword}',
                    languageCode = '{languageCode}',
                    countryCode = '{countryCode}',
                    insert_date = NOW()

                    ON DUPLICATE KEY UPDATE
						trans_keyword = '{trans_keyword}',
                        languageCode = '{languageCode}',
                        countryCode = '{countryCode}'
                """.format(
                        trans_keyword = loadDb.conn.escape_string(word),
                        languageCode = keyword_list["languageCode"],
                        countryCode = keyword_list["countryCode"]
                    )

                #print("== CALL SQL ==")
                #print(_SQL)

                with loadDb.conn.cursor() as cursor :
                    cursor.execute(_SQL)

        finally:
            loadDb.conn.commit()
            loadDb.conn.close()
            cursor.close()

    def DELETE(self, obj=None) :
        try:
            loadDb.DB_CONNECT()
            return_list = {"success" : True}

            _SQL = """ TRUNCATE TABLE top_keyword""" 
            with loadDb.conn.cursor() as cursor :
                cursor.execute(_SQL)

            #print("== CALL SQL ==")
            #print(_SQL.format(
            #        idx = obj["idx"]
            #))

            return return_list

        finally:
            loadDb.conn.commit()
            loadDb.conn.close()
            cursor.close()
