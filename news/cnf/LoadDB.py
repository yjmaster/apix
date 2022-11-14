import pymysql
from pprint import pprint
from ast import literal_eval

class LoadDB:
	def __init__(self, host='localhost', user='root', password='yjmedia', db='konke'):
		self.host = host
		self.user = user
		self.password = password
		self.db = db

	def DB_CONNECT(self):
		self.conn = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.db, charset='utf8')

	def DB_CLOSE(self):
		self.conn.close()

	def DB_ASIATIME_SELECT_JSON(self, q, l=10):
		curs = self.conn.cursor()
		_SQL="""SELECT 

                    JSON_OBJECT("items", JSON_ARRAYAGG(j)	)
                FROM (
                    SELECT 
                        MATCH(TITLE, CONTENT) AGAINST('*""" + q + """*' IN BOOLEAN MODE) AS SCORE,
                        JSON_OBJECT(
                            "title" , TITLE,
                            "content",CONTENT) AS j
                    FROM ASIATIMES_NEWS WHERE MATCH(TITLE, CONTENT) AGAINST('*""" + q + """*' IN BOOLEAN MODE)
                    LIMIT """ + l + """
                )A
		"""
		try:
			print(_SQL)
			curs.execute(_SQL)
			#curs.execute(_SQL.format( SECTIONCODE=str(sectioncode) ))
			res = curs.fetchone()
			return res[0]

		except Exception as e:
			pprint(_SQL)
			raise e

	def DB_NAVER_SELECT_JSON(self,keywords):
		curs = self.conn.cursor()
		sendJson = {"result":[]}
        
		for keyword in keywords :
			_SQL="""SELECT 
						JSON_OBJECT("items", JSON_ARRAYAGG(j)	)
					FROM (
						SELECT 
						MATCH(TITLE) AGAINST('*""" + keyword + """*' IN BOOLEAN MODE) AS SCORE,
								JSON_OBJECT(
									"title" , TITLE,
									"summary", SUMMARY,
									"img", IMG,
									"url", `URL`
									) AS j
						FROM naver_dict WHERE MATCH(TITLE) AGAINST('*""" + keyword + """*' IN BOOLEAN MODE)
						ORDER BY SCORE
					)A
			"""
			try:
				# print(_SQL)
				curs.execute(_SQL)
				res = curs.fetchone()
				obj = literal_eval(res[0])
				sendJson["result"].append(obj)
			except Exception as e:
				pprint(_SQL)
				raise e
		return sendJson

if __name__ == '__main__':
	loaddb = LoadDB()
	loaddb.DB_CONNECT()

	res = loaddb.DB_ASIATIME_SELECT_JSON('문재인','5')
	print(res)

	loaddb.DB_CLOSE()
