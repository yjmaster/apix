from elasticsearch import Elasticsearch

# 'http://192.168.0.190:9200/'
class LoadElastic:
	def __init__(self, host='http://192.168.0.190:9200',
		http_auth=('yjmedia', '#yjm0115.c0m')):
		self.host = host
		self.http_auth = http_auth

	def es_conn(self):
		return Elasticsearch([self.host], http_auth=self.http_auth)
		