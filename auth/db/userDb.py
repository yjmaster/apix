from copyreg import constructor
import jwt
import hashlib
import pymysql

class UserDb:
	def __init__(self, host='192.168.0.190', user='maria', password='maria123', db='maria_DB'):
		self.host = host
		self.user = user
		self.password = password
		self.db = db
		self.type = ''

	def DB_CONNECT(self):
		self.conn = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.db, charset='utf8')
		self.conn.query("set character_set_connection=utf8;")
		self.conn.query("set character_set_server=utf8;")
		self.conn.query("set character_set_client=utf8;")
		self.conn.query("set character_set_results=utf8;")
		self.conn.query("set character_set_database=utf8;")

	def create_token(self, userInfo):
		access_token = jwt.encode(userInfo, "yjmedia", algorithm="HS256").decode('utf-8') #서버
		#access_token = jwt.encode(userInfo, "yjmedia", algorithm="HS256") #로컬
		return access_token

	def create_user(self, userInfo):
		try:
			returnStatus = { 'success': True }

			pwd = userInfo['password']
			pwdEncode = hashlib.sha256(pwd.encode())
			pwdEncode = pwdEncode.hexdigest()

			access_token = self.create_token(userInfo)
			returnStatus['access_token'] = access_token

			self.DB_CONNECT()

			_SQL = """INSERT INTO api_users SET
				media = '{media}',
				user_login = '{user_login}',
				`user_name` = '{user_name}',
				`password` = '{password}',
				`role` = '{role}',
				register_date = NOW()""".format(
					media = userInfo['media'],
					user_login = userInfo['user_login'],
					user_name = userInfo['user_name'],
					password = pwdEncode,
					role = userInfo['role']
				)

			# print(_SQL)

			curs = self.conn.cursor()
			curs.execute(_SQL)

		except Exception as exp :
			returnStatus['success'] = False
			returnStatus['message'] = str(exp)
		finally:
			self.conn.commit()
			return returnStatus
	
	def user_yn(self, userInfo):
		try:
			returnStatus = { 'success': True }

			_SQL = """UPDATE api_users SET
				useYn = '{useYn}',
				update_date = NOW()\n""".format(
					useYn = userInfo['useYn']
				)
    
			_SQL += "WHERE 1=1\n"
			_SQL += "AND user_login = '{user_login}'\n".format(
				user_login = userInfo['user_login'])
			_SQL += "AND media = '{media}'\n".format(
				media = userInfo['media'])

			#print(_SQL)

			curs = self.conn.cursor()
			curs.execute(_SQL)

			if userInfo['useYn'] == 'Y':
				returnStatus['message'] = "Active user"
			elif userInfo['useYn'] == 'N':
				returnStatus['message'] = "Inactive user"
    
		except Exception as exp :
			returnStatus['success'] = False
			returnStatus['message'] = str(exp)
		finally:
			return returnStatus

	def return_format(self, userCurs, userData):
		returnStatus = { 'success': True }

		if self.type == 'register':
			isUser = userCurs.fetchone()
			if isUser is None:
				returnStatus = self.create_user(userData)
				if returnStatus['success'] :
					returnStatus['message'] = "User registration is complete"
			else:
				returnStatus['success'] = False
				returnStatus['message'] = "user that exists"
		
		elif self.type == 'update':
			affectedCnt =  userCurs.rowcount
			if affectedCnt > 0:
				returnStatus['success'] = True
				returnStatus['message'] = "User has been modified"
			else:
				returnStatus['success'] = False
				returnStatus['message'] = "User information does not exist."

		elif self.type == 'yn':
			isUser = userCurs.fetchone()
			if not isUser:
				returnStatus['success'] = False
				returnStatus['message'] = "not found"
			else:
				returnStatus = self.user_yn(userData)

		elif self.type == 'check':
			isUser = userCurs.fetchone()
			if not isUser:
				returnStatus['success'] = False
				returnStatus['message'] = "User does not exist or not registered"
			else:
				userRole = isUser[6]
				userYn = isUser[7]
				if userRole != 'A':
					returnStatus['success'] = False
					returnStatus['message'] = "This is an unauthorized account"
				elif userYn == 'N':
					returnStatus['success'] = False
					returnStatus['message'] = "Inactive user"
				else:
					returnStatus['access_token'] = self.create_token(userData)

		elif self.type == 'auth':
			isUser = userCurs.fetchone()
			if isUser is None:
				returnStatus['success'] = False
				returnStatus['message'] = "unauthorized"
			else:
				returnStatus['success'] = True
				returnStatus['message'] = "authorized"

		elif self.type == 'get':
			isUser = userCurs.fetchall()
			if not isUser:
				returnStatus['success'] = False
				returnStatus['message'] = "User does not exist or not registered"
			else:
				userList = []
				for user in isUser:
					userData = {}
					media = user[0]
					user_login = user[1]
					user_name = user[2]
					password = user[3]
					role = user[6]
					useYn = user[7]

					userData['media'] = media
					userData['user_login'] = user_login
					userData['user_name'] = user_name
					userData['password'] = password
					userData['role'] = role
			
					access_token = self.create_token(userData)
					register_date = user[4].strftime("%Y-%m-%d %H:%M:%S")
					update_date = ''
					if user[5] is not None:
						update_date = user[5].strftime("%Y-%m-%d %H:%M:%S")

					obj = {}
					obj['media'] = media
					obj['user_login'] = user_login
					obj['user_name'] = user_name
					obj['register_date'] = register_date
					obj['update_date'] = update_date
					obj['role'] = role
					obj['useYn'] = useYn
					obj['access_token'] = access_token
					userList.append(obj)

				returnStatus["result"] = userList

		return returnStatus

	def find_user(self, userData, type):
		try:
			returnStatus = {}
			self.type = type

			self.DB_CONNECT()
			_SQL = ''
			if self.type == 'check' or self.type == 'register':
				_SQL = """SELECT * FROM api_users
					WHERE 1=1
					AND media = '{media}'
					AND user_login = '{user_login}'
					AND `password` = SHA2('{password}', 256)""".format(
						media = userData['media'],
						user_login = userData['user_login'],
						password = userData['password']
					)

				#print(_SQL)

			elif self.type == 'yn':
				_SQL = """SELECT * FROM api_users
					WHERE 1=1
					AND media = '{media}'
					AND user_login = '{user_login}'""".format(
						media = userData['media'],
						user_login = userData['user_login']
					)
				#print(_SQL)

			elif self.type == 'update':
				_SQL = """UPDATE api_users SET\n"""
    
				# if 'media' in userData:
				# 	_SQL += "media = '{media}',\n".format(
				# 		media = userData['media'])

				if 'user_name' in userData:
					_SQL += "user_name = '{user_name}',\n".format(
					user_name = userData['user_name'])

				if 'password' in userData:
					_SQL += "`password` = SHA2('{password}', 256),\n".format(
					password = userData['password'])

				_SQL += "update_date = NOW()\n"
				_SQL += "WHERE 1=1\n"
				_SQL += "AND user_login = '{user_login}'\n".format(
					user_login = userData['user_login'])
				_SQL += "AND media = '{media}'\n".format(
					media = userData['media'])
    
				#print(_SQL)
    
			elif self.type == 'get':
				_SQL = """SELECT * FROM api_users
					WHERE 1=1\n"""

				if 'media' in userData:
					_SQL += "AND media = '{media}'\n".format(
						media = userData['media'])

				if 'user_login' in userData:
					_SQL += "AND user_login = '{user_login}'\n".format(
						user_login = userData['user_login'])

				#print(_SQL)
				# if 'role' in userData:
				# 	_SQL += "AND role = '{role}'\n".format(
				# 		role = userData['role'])

			elif self.type == 'auth':
				_SQL = """SELECT * FROM api_users
					WHERE 1=1
					AND media = '{media}'
					AND user_login = '{user_login}'
					AND `password` = '{password}'""".format(
						media = userData['media'],
						user_login = userData['user_login'],
						password = userData['password']
					)

			curs = self.conn.cursor()
			curs.execute(_SQL)

			returnStatus = self.return_format(curs, userData)

		except Exception as exp :
			returnStatus['success'] = False
			returnStatus['message'] = str(exp)
		finally:
			self.conn.commit()
			self.conn.close()
			self.conn.cursor().close()
			return returnStatus

	def decode_token(self, auth, encodePwd):
		decoded = jwt.decode(auth, "yjmedia", algorithms="HS256")
		if encodePwd:
			pwd = decoded['password']
			pwdEncode = hashlib.sha256(pwd.encode())
			pwdEncode = pwdEncode.hexdigest()
			decoded['password'] = pwdEncode
		return self.find_user(decoded, "auth")
