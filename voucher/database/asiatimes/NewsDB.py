from datetime import datetime
from datetime import timedelta
from voucher.database.LoadDB import LoadDB
from voucher.database.asiatimes.LinkDB import LinkDB

loadDb = LoadDB()
linkDB = LinkDB()

class NewsDB:
    def SELECTCNT(self, obj) :
        try:
            loadDb.DB_CONNECT()
            return_list = []
            _SQL = """ SELECT senti, count(*) FROM global_news WHERE 1=1\n """
            _SQL += "AND area='{}'\n".format(obj["area"])
            _SQL += "AND keyword='{}'\n".format(obj["keyword"])
            _SQL += "AND upload_date >= '{} 00:00:00'\n".format(obj["sdate"])
            _SQL += "AND upload_date <= '{} 23:59:59'\n".format(obj["edate"])

            if obj["senti"] :
                _SQL += "AND senti = '{}'\n".format(obj["senti"])
            
            _SQL += "GROUP BY senti"

            #print("== CALL Total SQL ==")
            #print(_SQL)

            with loadDb.conn.cursor() as cursor :
                cursor.execute(_SQL)

                for idx, val in enumerate(cursor) :
                    return_list.append({
                        'senti':val[0],'cnt': val[1]
                    })

                return return_list
            
        finally:
            loadDb.conn.commit()
            loadDb.conn.close()
            cursor.close()

    def SELECT(self, obj, start, end) :
        try:
            loadDb.DB_CONNECT()
            return_list = []
            _SQL = """ SELECT * FROM global_news WHERE 1=1\n """
            _SQL += "AND area='{}'\n".format(obj["area"])
            _SQL += "AND keyword='{}'\n".format(obj["keyword"])
            _SQL += "AND upload_date >= '{} 00:00:00'\n".format(obj["sdate"])
            _SQL += "AND upload_date <= '{} 23:59:59'\n".format(obj["edate"])

            if obj["senti"] :
                _SQL += "AND senti = '{}'\n".format(obj["senti"])

            _SQL += "ORDER BY upload_date DESC\n"
            _SQL += "LIMIT {},{}".format(start, end)

            #print("== CALL SQL ==")
            #print(_SQL)

            with loadDb.conn.cursor() as cursor :
                cursor.execute(_SQL)

            for idx, val in enumerate(cursor) :
                upload_date = val[5].strftime('%Y.%m.%d')
                insert_date = val[8].strftime('%Y.%m.%d')

                return_list.append({
                    'idx':val[0],'title': val[1],
                    'summary': val[2], 'image': val[3],
                    'link':val[4], 'upload_date':upload_date,
                    'keyword':val[6], 'area':val[7],
                    'insert_date':insert_date,
                    'senti':val[9]
                })

            return return_list
            
        finally:
            loadDb.conn.commit()
            loadDb.conn.close()
            cursor.close()

    def INSERT(self, newsList) :
        try:
            loadDb.DB_CONNECT()
            return_list = {"success" : True}
            for item in newsList :    
            
                _SQL = """ INSERT INTO global_news SET
                    idx = (SELECT IFNULL((SELECT MAX(idx) FROM global_news AS subq),0)+1),
                    title = '{title}',
                    summary = '{summary}',
                    `image` = '{image}',
                    link = '{link}',
                    `upload_date` = '{upload_date}',
                    keyword = '{keyword}',
                    area = '{area}',
                    senti = '{senti}',
                    insert_date = NOW()

                    ON DUPLICATE KEY UPDATE
						title = '{title}',
						summary = '{summary}',
						`image` = '{image}',
						`upload_date` = '{upload_date}',
                        keyword = '{keyword}',
                        area = '{area}',
                        senti = '{senti}',
                        insert_date = NOW()""".format(
                            title = loadDb.conn.escape_string(item["title"]),
                            summary = loadDb.conn.escape_string(item["summary"]),
                            image = item["image"],
                            link = item["link"],
                            upload_date = item["date"],
                            keyword = item["keyword"],
                            area = item["area"],
                            senti = item["emotion"]
                        )

                with loadDb.conn.cursor() as cursor :
                    cursor.execute(_SQL)
        
            return return_list

        finally:
            loadDb.conn.commit()
            loadDb.conn.close()
            cursor.close()

    def DELETE(self, obj=None) :
        try:
            loadDb.DB_CONNECT()
            return_list = {"success" : True}
            if obj is not None :
                _SQL = """ DELETE FROM global_news 
                    WHERE keyword = (
                        SELECT keyword FROM global_issue
                        WHERE idx = '{idx}'
                    ) """.format(idx = obj["idx"])
                    
                #print("== CALL SQL ==")
                #print(_SQL)

                with loadDb.conn.cursor() as cursor :
                    cursor.execute(_SQL)
            else :
                today = datetime.now()
                limitDate = (today - timedelta(7)).strftime('%Y-%m-%d 00:00:00')
                _SQL = "DELETE FROM global_news WHERE insert_date < '{}'".format(limitDate)

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
