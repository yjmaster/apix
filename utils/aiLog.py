import uuid
import pymysql
class aiLog:
	# def __init__(self, host='localhost', user='kpf', password='kpf123', db='newsai'):
	def __init__(self, host='118.67.150.92', user='kpf', password='kpf123', db='newsai'):
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

	def count_log(self, cntInfo):
		try:
			res = {"success": True}

			_SQL = """INSERT INTO news_ai_cnt SET
					media = '{media}',
					router = '{router}',
					id_client = '{id_client}',
					cnt = 1,
					last_date = NOW()
				ON DUPLICATE KEY UPDATE
					cnt = cnt + 1,
					last_date = NOW()""".format(
						media = cntInfo['media'],
						router = cntInfo['router'],
						id_client = cntInfo['id_client']
					)

			# print("카운팅 로그 ----------> \n", _SQL)

			curs = self.conn.cursor()
			curs.execute(_SQL)

		except Exception as exp:
			print("count_log error : {}\n".format(str(exp)))
			print("query : {}\n".format(_SQL))
			res = {"success": False, "message": str(exp)}
		finally:
			self.conn.commit()
			return res

	def request_log(self, id_client, router):
		try:
			self.connect_db()
			uid = uuid.uuid1()
			res = {"success": True, "uid": uid}

			_SQL = """INSERT INTO news_ai_log SET
					`uid` = '{uid}',
					id_client = '{id_client}',
					router = '{router}',
					request_date = NOW()""".format(
						uid = uid,
						router = router,
						id_client = id_client
					)

			# print("호출 로그 ----------> \n", _SQL)

			curs = self.conn.cursor()
			curs.execute(_SQL)

		except Exception as exp:
			print("request_log error : {}\n".format(str(exp)))
			print("query : {}\n".format(_SQL))
			res = {"success": False, "message": str(exp)}
		finally:
			self.conn.commit()
			return res

	def response_log(self, resInfo, params):
		try:
			res = {"success": True}

			uid = resInfo['uid']
			code = resInfo['code']

			media_sql = ""
			if "media" in resInfo:
				media = resInfo['media']
				media_sql = "media = '{}' ,".format(media)

			message_sql = ""
			if "message" in resInfo:
				message = resInfo['message']
				message_sql = "error_msg = '{}' ,".format(message)

			_SQL = """UPDATE news_ai_log SET
					{media_sql}
					{message_sql}
					response_date = NOW(),
					response_code = '{code}'
				WHERE 1=1
				AND `uid` = '{uid}'""".format(
						media_sql = media_sql,
						message_sql = message_sql,
						code = code,
						uid = uid
					)

			# print("완료 로그 ----------> \n", _SQL)

			curs = self.conn.cursor()
			curs.execute(_SQL)

			# if not resInfo['success'] and code != 401:
			# 	print("추가파라미터저장")
			# 	params.update({'uid': uid})
			# 	res = self.error_data_log(params)
			# 	if not res['success']: return
    
			if resInfo['success'] and code == 200:
				self.count_log(resInfo)

		except Exception as exp:
			print("response_log error : {}\n".format(str(exp)))
			print("query : {}\n".format(_SQL))
			res = {"success": False, "message": str(exp)}
		finally:
			self.conn.commit()
			self.conn.cursor().close()
			self.conn.close()
			return res

	def error_data_log(self, params):
		try:
			res = {"success": True}

			_SQL = """INSERT INTO error_data
				SET `uid` = '{uid}',
					title = '{title}',
					content = '{content}',
					request_date = NOW()""".format(
						uid = params['uid'],
						title = self.conn.escape_string(params['title']),
						content = self.conn.escape_string(params['content'])
					)

			# print("데이터 로그 ----------> \n", _SQL)

			curs = self.conn.cursor()
			curs.execute(_SQL)

		except Exception as exp:
			print("error_data_log error : {}\n".format(str(exp)))
			print("query : {}\n".format(_SQL))
			res = {"success": False, "message": str(exp)}
		finally:
			self.conn.commit()
			return res
