# -*- coding: utf-8 -*-
import re
import json
from bs4 import Tag, BeautifulSoup as bs
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

	def parse_content(media, content):
		content = bs(content, 'html.parser')

		if media == 'asiatimes':
			# 이미지 제거
			for img in content.select('img') : img.extract()
			# 이미지 설명 제거
			for figcaption in content.select('figcaption') : figcaption.extract()
			# 테이블 제거
			for table in content.select('table') : table.extract()
			# 3줄요약 제거
			for summary in content.select('div.article_summary_container') : summary.extract()
			# 중간제목 제거
			for mtitle in content.select('div.middle_title_box') : mtitle.extract()
			# 편집자 주 제거
			for editor in content.select('div.article_editor_container') : editor.extract()
			# 바이라인 제거
			content = re.sub(r'\[아시아타임즈=(.+)]', '', content.text).strip()

		return content
