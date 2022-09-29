import json
from datetime import datetime

class reqFormat:
    
	def parse_data(request):
		"""
		flask의 request에서 데이터를 가져옴
			주의: flask-restplus 모듈을 이용하여 swagger ui를 이용하는 패러미터
				패싱이 제대로 안되어 본 함수 이용 (0.10.1)
		:param request: Flask의 request
		:return: parameter dict
		"""
		if not hasattr(request, 'method'):
			return None
		if request.method.upper() != 'GET':
			if request.data:
				try : 
					return json.loads(request.data.decode('utf-8'), strict=False)
				except:
					return json.loads(request.data.decode('cp949'), strict=False)
		if 'json' in request.args:
			return json.loads(request.args['json'])
		if request.args:
			return request.args     # note: type is ImmutableMultiDict
		return {}
