import pymysql
class aiLog:
	def __init__(self, host='localhost', user='kpf', password='kpf123', db='newsai'):
		self.host = host
		self.user = user
		self.password = password
		self.db = db

	def connect_db(self):
		self.conn = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.db, charset='utf8')
		self.conn.query("set character_set_connection=utf8;")
		self.conn.query("set character_set_server=utf8;")
		self.conn.query("set character_set_client=utf8;")
		self.conn.query("set character_set_results=utf8;")
		self.conn.query("set character_set_database=utf8;")

	def wirte_log(self, media, request):
		try:
			self.connect_db()
			router = (request.url_rule.rule).split("/")[-1]
			_SQL = """INSERT INTO news_ai_log SET
					router = '{router}',
					media = '{media}',
					last_date = NOW(),
					cnt = 1
				ON DUPLICATE KEY UPDATE
					cnt = cnt + 1,
					last_date = NOW()""".format(
						router = router,
						media = media
					)

			# print(_SQL)

			curs = self.conn.cursor()
			curs.execute(_SQL)
		
		except Exception as e :
			print("ERROR : {}".format(e))
		finally:
			self.conn.commit()
			self.conn.cursor().close()
			self.conn.close()
