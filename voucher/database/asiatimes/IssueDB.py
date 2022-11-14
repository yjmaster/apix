from datetime import datetime
from voucher.database.LoadDB import LoadDB
from voucher.database.asiatimes.LinkDB import LinkDB
import ast

loadDb = LoadDB()
linkDB = LinkDB()

class IssueDB:
    def SELECT(self, obj=None) :
        try:
            loadDb.DB_CONNECT()
            return_list = []

            _SQL = """ SELECT 
                        issue.idx,
                        issue.keyword,
                        issue.date,
                        issue.link,
                        issue.area,
                        code.code
                    FROM global_issue AS issue
                    INNER JOIN global_code AS `code`
                    ON issue.area = code.name """

            if obj is not None : 
                if obj["idx"] != "" :
                    _SQL += "WHERE issue.idx = {}".format(obj["idx"])

                elif obj["area"] != "" :
                    _SQL += "WHERE issue.area = '{}'".format(obj["area"])

                _SQL += " ORDER BY issue.{} {}".format(obj["col"], obj["order"])

            #print("== CALL SQL ==")
            #print(_SQL, end="\n\n")

            with loadDb.conn.cursor() as cursor :
                cursor.execute(_SQL)

            for val in cursor :
                return_link = []
                date = val[2].strftime('%Y.%m.%d')

                link_list = ast.literal_eval(val[3])
                for link_idx in link_list :
                    linkList = linkDB.SELECT({"idx":link_idx})[0]

                    return_link.append({
                        "idx" : linkList["idx"],
                        "link" : linkList["link"]
                    })

                return_obj = {}
                return_obj["idx"] = val[0]
                return_obj["keyword"] = val[1]
                return_obj["date"] = date
                return_obj["area"] = val[4]
                return_obj["code"] = val[5]

                if len(return_link) != 0:
                    return_obj["links"] = return_link

                return_list.append(return_obj)

            return return_list

        finally:
            loadDb.conn.commit()
            loadDb.conn.close()
            cursor.close()

    def INSERT(self, obj) :
        try:
            loadDb.DB_CONNECT()    
            return_list = {"success" : True}
            _SQL = """ INSERT INTO global_issue SET
                keyword = '{keyword}',
                date = '{date}',
                link = '{link}',
                area = '{area}'
            """ .format(
                    keyword = obj["keyword"],
                    date = datetime.now(),
                    link = obj["link"],
                    area = obj["area"]
                )

            #print("== CALL SQL ==")
            #print(_SQL)

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

            _SQL = """ UPDATE global_issue SET
                link = '{link}'
                WHERE idx = '{idx}'
            """ .format(
                    link = obj["link"],
                    idx = obj["idx"]
                )
            
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

            _SQL = """ DELETE FROM global_issue
                WHERE idx = '{idx}' """ .format(
                        idx = obj["idx"])

            #print("== CALL SQL ==")
            #print(_SQL)

            with loadDb.conn.cursor() as cursor :
                cursor.execute(_SQL)

            return return_list

        finally:
            loadDb.conn.commit()
            loadDb.conn.close()
            cursor.close()

