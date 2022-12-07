import pymysql

class BflysoftDb:
	# def __init__(self, host='118.67.152.68', user='yjuser', password='Yjuser(1104#$)', db='spell_check'):
	def __init__(self, host='118.67.152.74', user='yjuser', password='Yjuser(1124#$)', db='spell_check'):
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

	def authentication(self, id_client):
		try:
			self.connect_db()
			res = {'success': False}
			
			_SQL = """SELECT
					NM_CLIENT,
					FG_NEWSAI_USE
				FROM tbs_api_client
				WHERE 1=1
				AND ID_CLIENT = '{ID_CLIENT}'""".format(
					ID_CLIENT = id_client
				)

			# print(_SQL)

			curs = self.conn.cursor()
			curs.execute(_SQL)

			isUser = curs.fetchone()
			if not isUser :
				res['message'] = '존재하지 않는 사용자 입니다.'
				res['code'] = 401
				return

			NM_CLIENT = isUser[0]
			FG_NEWSAI_USE = isUser[1]

			if FG_NEWSAI_USE == 'N':
				res['message'] = 'NEWS AI 사용 등록이 되지 않았습니다.'
				res['code'] = 403
				return

			res['success'] = True
			res['media'] = NM_CLIENT
			# raise Exception('authentication test error')
		except Exception as exp :
			res = {"success": False, "code": 500, "message": str(exp)}
		finally:
			self.conn.cursor().close()
			self.conn.close()
			return res