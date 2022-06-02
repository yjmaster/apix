import pymysql
from datetime import datetime

class LogDB:
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

	def DB_CLOSE(self):
		self.conn.close()

	def DB_INSERT(self, router):
		try:
			now = datetime.now()
			_SQL = """UPDATE news_ai_log AS a,
				(SELECT cnt FROM news_ai_log WHERE router = '{router}') AS b
				SET last_time = '{last_time}', a.cnt = (b.cnt)+1
				WHERE router = '{router}'"""

			curs = self.conn.cursor()
			curs.execute(_SQL.format(
				router = router,
				last_time = now
			))
		
		except Exception as e :
			pass
			# raise e
		else: self.conn.commit()

if __name__ == '__main__':
	LogDB = LogDB()
	LogDB.DB_CONNECT()
	LogDB.DB_INSERT()
	LogDB.DB_CLOSE()
