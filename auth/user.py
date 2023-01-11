from auth.db import YJDb
yjDb = YJDb()

class YJUser:
	def find_user(self, params):
		try:
			yjDb.connect_db()
			result = {"success": True}

			_SQL = """SELECT *
				FROM news_ai_users
				WHERE 1=1
				AND user_login = '{user_login}'
				AND `password` = SHA2('{password}', 256)""".format(
					user_login = params['user_login'],
					password = params['password']
				)

			curs = yjDb.conn.cursor()
			curs.execute(_SQL)
			user = curs.fetchone()
			if user:
				result["id_client"] = user[0]
			else:
				result["success"] = False
				result["message"] = "존재하지 않는 사용자 입니다."

		except Exception as exp :
			result = {"success": False, "message": str(exp)}
		finally: 
			yjDb.conn.cursor().close()
			yjDb.conn.close()
			return result




