# -*- coding: utf-8 -*-
import math
import pymysql
import configparser

class KpfDb:
	def __init__(self):
		config = configparser.ConfigParser()    
		config.read('config.ini', encoding='utf-8')

		kpfdb = config['kpfdb']
		self.host = kpfdb['host']
		self.user = kpfdb['user']
		self.password = kpfdb['password']
		self.db = kpfdb['db']

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

			_CODE = ""
			code = params['code']
			if code != '':
				_CODE = "AND response_code = '{}'".format(params['code'])

			_KEY = ""
			key = params['id_client']
			if key and key != "881143FD-49DC-4F0B-9946-2E831A359C80":
				_KEY = "AND id_client = '{id_client}'".format(
					id_client = key
				)

			_SQL = """SELECT count(*)
				FROM news_ai_log
				WHERE 1=1
				{_CODE}
				{_KEY}
				AND request_date >= '{sdate} 00:00:00'
				AND request_date <= '{edate} 23:59:59'""".format(
					_CODE = _CODE,
					_KEY = _KEY,
					sdate = params['sdate'],
					edate = params['edate']
				)

			# print(_SQL)

			curs = self.conn.cursor()
			curs.execute(_SQL)
			total = curs.fetchone()

			cnt = int(total[0])
			display = int(params['display'])

			last_page = math.ceil(cnt/display)

			result['cnt'] = cnt
			result['last_page'] = last_page

		except Exception as exp:
			result = {"success": False, "message": str(exp)}
		finally:
			return result

	def get_options(self, params):
		try:
			self.connect_db()
			result = {"success": True}

			id_client_sql = ""
			id_client = params['id_client']
			if id_client != "881143FD-49DC-4F0B-9946-2E831A359C80":
				id_client_sql = "AND id_client = '{}'".format(id_client)

			_SQL = """SELECT
				DISTINCT media, response_code
				FROM news_ai_log
				WHERE 1=1
				{id_client_sql}
				AND request_date >= '{sdate} 00:00:00'
				AND request_date <= '{edate} 23:59:59'
				ORDER BY request_date DESC""".format(
					id_client_sql = id_client_sql,
					sdate = params['sdate'],
					edate = params['edate']
				)

			# print(_SQL)

			curs = self.conn.cursor()
			curs.execute(_SQL)

			options, media, code = {}, [], []
			for idx, row in enumerate(curs) :
				mediaTxt = row[0]
				if mediaTxt is None:
					mediaTxt = "(NULL)"
				media.append(mediaTxt)
				code.append(row[1])

			media = list(set(media))
			code = list(set(code))

			options['media'] = media
			options['code'] = code

			result['options'] = options

		except Exception as exp:
			result = {"success": False, "message": str(exp)}
		finally:
			self.conn.cursor().close()
			self.conn.close()
			return result

	def get_log(self, params):
		try:
			self.connect_db()
			result = {"success": True}

			totalInfo = self.total(params)
			result = totalInfo
			if not totalInfo['success']: return

			display = int(params['display'])
			page = int(params['page'])
			start = (page -1) * display

			_CODE = ""
			code = params['code']
			if code != '':
				_CODE = "AND response_code = '{}'".format(params['code'])
    
			_LIMIT = ""
			excel = params['excel']
			if not excel :
				_LIMIT = "LIMIT {start}, {display}".format(
					start = start,
					display = display
				)

			_KEY = ""
			key = params['id_client']
			if key and key != "881143FD-49DC-4F0B-9946-2E831A359C80":
				_KEY = "AND id_client = '{id_client}'".format(
					id_client = key
				)

			_SQL = """SELECT *
				FROM news_ai_log
				WHERE 1=1
				AND request_date >= '{sdate} 00:00:00'
				AND request_date <= '{edate} 23:59:59'
				{_CODE}
				{_KEY}
				ORDER BY request_date DESC
				{_LIMIT}""".format(
					sdate = params['sdate'],
					edate = params['edate'],
					_CODE = _CODE,
					_KEY = _KEY,
					_LIMIT = _LIMIT
				)

			# print(_SQL)

			curs = self.conn.cursor()
			curs.execute(_SQL)

			logs = []
			for idx, row in enumerate(curs) :
				request_date = row[3].strftime("%Y-%m-%d %H:%M:%S")
				response_date =  row[4]
				if response_date:
					response_date = response_date.strftime("%Y-%m-%d %H:%M:%S")
				else: response_date = ""
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
			self.conn.cursor().close()
			self.conn.close()
			return result