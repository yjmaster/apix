import pymysql

class LoadDB:
	def __init__(self, host='192.168.0.190',
		user='maria',password='maria123', db='maria_DB'):
		self.host = host
		self.user = user
		self.password = password
		self.db = db

	def DB_CONNECT(self):
		self.conn = pymysql.connect(
			host=self.host, user=self.user,
			password=self.password, db=self.db, charset='utf8')
			
	def DB_CLOSE(self):
		self.conn.close()