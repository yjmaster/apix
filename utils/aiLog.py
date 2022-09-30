import pymysql
from datetime import datetime
from utils.reqFormat import reqFormat

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

	def DB_UPDATE(self, media, router, userInfo):
		try:
			# userInfo 는 필수값이 될 예정
			if bool(userInfo) == False :
				userInfo['user_login'] = media
				userInfo['user_name'] = media
    
			_SQL = """INSERT INTO news_ai_log SET
					router = '{router}',
					media = '{media}',
					user_login = '{user_login}',
					`user_name` = '{user_name}',
					last_date = NOW(),
					cnt = 1
				ON DUPLICATE KEY UPDATE
					cnt = cnt + 1,
					last_date = NOW(),
					user_login = '{user_login}',
					`user_name` = '{user_name}'""".format(
						router = router,
						media = media,
						user_login = userInfo['user_login'],
						user_name = userInfo['user_name']
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
		userInfo = {}
		router = (request.url_rule.rule).split("/")[-1]
		args = reqFormat.parse_data(request)
		if ('userLogin' in args) and ('userName' in args):
			userInfo['user_login'] = args['userLogin']
			userInfo['user_name'] = args['userName']

		self.DB_CONNECT()
		self.DB_UPDATE(media, router, userInfo)