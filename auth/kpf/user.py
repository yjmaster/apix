from auth.kpf.db import KpfDb
kpfDb = KpfDb()

class KpfUser:
	def find_user(self, params):
		try:
			kpfDb.connect_db()
			result = {"success": True}

			_SQL = """SELECT *
				FROM news_ai_users
				WHERE 1=1
				AND user_login = '{user_login}'
				AND `password` = SHA2('{password}', 256)""".format(
					user_login = params['user_login'],
					password = params['password']
				)

			curs = kpfDb.conn.cursor()
			curs.execute(_SQL)
			user = curs.fetchone()
			if user:
				result["id_client"] = user[0]
				result["media"] = user[1]
			else:
				result["success"] = False
				result["message"] = "존재하지 않는 사용자 입니다."

		except Exception as exp :
			result = {"success": False, "message": str(exp)}
		finally: 
			kpfDb.conn.cursor().close()
			kpfDb.conn.close()
			return result

	def find_key(self, key):
		try:
			kpfDb.connect_db()
			res = {"success": True}

			_SQL = """SELECT *
				FROM news_ai_users
				WHERE 1=1
				AND id_client = '{key}'""".format(
					key = key
				)

			# print(_SQL)

			curs = kpfDb.conn.cursor()
			curs.execute(_SQL)

			user = curs.fetchone()
			if user:
				res["id_client"] = user[0]
				res["media"] = user[1]
			else:
				res["success"] = False
				res["message"] = "존재하지 않는 사용자 입니다."
				res['code'] = 400

		except Exception as exp :
			res = {"success": False, "code": 500, "message": str(exp)}
		finally: 
			kpfDb.conn.cursor().close()
			kpfDb.conn.close()
			return res





