import pymysql
from datetime import datetime

class aiLog:
	def __init__(self, host='192.168.0.190', user='maria', password='maria123', db='maria_DB'):
		self.host = host
		self.user = user
		self.password = password
		self.db = db

	def DB_CONNECT(self):
		self.conn = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.db, charset='utf8')
		self.conn.query("set character_set_connection=utf8;")
		self.conn.query("set character_set_server=utf8;")
		self.conn.query("set character_set_client=utf8;")
		self.conn.query("set character_set_results=utf8;")
		self.conn.query("set character_set_database=utf8;")

	def DB_UPDATE(self, media, router):
		try:
			now = datetime.now()
		
			_SQL = """UPDATE news_ai_log_ AS a,
				(SELECT cnt FROM news_ai_log_ WHERE router = '{router}') AS b
				SET last_date = '{last_date}', a.cnt = (b.cnt)+1
				WHERE 1=1
				AND router = '{router}'
				AND media = '{media}'""".format(
					router = router,
					last_date = now,
					media = media
				)

			#print(_SQL)

			curs = self.conn.cursor()
			curs.execute(_SQL)
		
		except Exception as e :
			print("ERROR : {}".format(e))
			pass
		else:
			self.conn.commit()
			self.conn.close()
			curs.close()

	def wirte_log(self, media, request):
		router = (request.url_rule.rule).split("/")[-1]
		self.DB_CONNECT()
		self.DB_UPDATE(media, router)