import pymysql

class BflysoftDb:
	def __init__(self, host='118.67.152.68', user='yjuser', password='Yjuser(1104#$)', db='spell_check'):
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
			returnStatus = {'success': False}

			self.connect_db()

			_SQL = """SELECT NM_CLIENT, FG_NEWSAI_USE
				FROM tbs_api_client
				WHERE 1=1
				AND ID_CLIENT = '{ID_CLIENT}'""".format(
					ID_CLIENT = id_client
				)

			print(_SQL)

			curs = self.conn.cursor()
			curs.execute(_SQL)

			message = ''
			isUser = curs.fetchone()
			if isUser :
				NM_CLIENT = isUser[0]
				FG_NEWSAI_USE = isUser[1]

				if FG_NEWSAI_USE == 'Y':
					returnStatus['success'] = True
					returnStatus['media'] = NM_CLIENT
				else:
					message = 'User is not authenticated'
			else:
				message = 'User does not exist'
				returnStatus['message'] = message

		except Exception as exp :
			returnStatus['success'] = False
			returnStatus['message'] = str(exp)

		finally:
			self.conn.cursor().close()
			self.conn.close()

			return returnStatus