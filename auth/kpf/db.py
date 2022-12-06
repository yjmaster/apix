import math
import pymysql

class KpfDb:
	# def __init__(self, host='118.67.150.92', user='kpf', password='kpf123', db='newsai'):
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

	def total(self, params):
		try:
			result = {"success": True}

			_SQL = """SELECT count(*)
				FROM news_ai_log
				WHERE 1=1
				AND request_date >= '{sdate} 00:00:00'
				AND request_date <= '{edate} 23:59:59'""".format(
					sdate = params['sdate'],
					edate = params['edate']
				)

			# print(_SQL)

			curs = self.conn.cursor()
			curs.execute(_SQL)
			total = curs.fetchone()

			cnt = int(total[0])
			display = int(params['display'])

			last_page = math.floor(cnt/display)

			result['cnt'] = cnt
			result['last_page'] = last_page

		except Exception as exp:
			result = {"success": False, "message": str(exp)}
		finally:
			return result

	def select(self, params):
		try:
			result = {"success": True}

			self.connect_db()
			totalInfo = self.total(params)
			result = totalInfo
			if not totalInfo['success']: return

			display = int(params['display'])
			page = int(params['page'])
			start = (page -1) * display

			_SQL = """SELECT *
				FROM news_ai_log
				WHERE 1=1
				AND request_date >= '{sdate} 00:00:00'
				AND request_date <= '{edate} 23:59:59'
				ORDER BY request_date DESC
				LIMIT {start}, {display}""".format(
					sdate = params['sdate'],
					edate = params['edate'],
					start = start,
					display = display
				)

			# print(_SQL)

			curs = self.conn.cursor()
			curs.execute(_SQL)

			logs = []
			for idx, row in enumerate(curs) :
				request_date = row[3].strftime("%Y-%m-%d %H:%M:%S")
				response_date = row[4].strftime("%Y-%m-%d %H:%M:%S")
				logs.append({
					'uid': row[0],
					'media': row[1],
					'router': row[2],
					'request_date': request_date,
					'response_date': response_date,
					'response_code': row[5],
					'error_msg': row[6]
				})

			result['list'] = logs

		except Exception as exp:
			result = {"success": False, "message": str(exp)}
		finally:
			self.conn.close()
			return result