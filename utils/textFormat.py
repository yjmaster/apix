# -*- coding: utf-8 -*-
import re
import json
from utils.customWord import CustomWord
from bs4 import Tag, BeautifulSoup as bs

customWord = CustomWord()

class TextFormat:
	def __init__(self):
		self.temp_list = []
		self.sent_list = []

	def parse_data(self, request):
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

	def mappingSentIndex(self, sent):
		for qutoe in self.temp_list:
			format = qutoe['format']
			replaceSent = qutoe['sent']
			if format in sent:
				format = re.sub('\[', '\\[', format)
				format = re.sub('\]', '\\]', format)
				new_sent = re.sub(format, replaceSent, sent)
				sent = new_sent
		return sent

	def separateExtraction(self, content):
		for match in re.finditer(r'\"(.*?)\"', content):
			matchText = match.group()
			start = match.start()
			end = match.end()
			
			matchFormat = "[{}:{}]".format(start, end)
			content = content.replace(matchText, matchFormat)
			obj = {'sent': matchText, 'format': matchFormat}
			self.temp_list.append(obj)

		for match in re.finditer(r'\([^)]*\)', content):
			matchText = match.group()
			start = match.start()
			end = match.end()
			
			matchFormat = "[{}:{}]".format(start, end)
			content = content.replace(matchText, matchFormat)
			obj = {'sent': matchText, 'format': matchFormat}
			self.temp_list.append(obj)

		return content

	def quoteReplace(self, content):
		content = re.sub('\“', '\"', content)
		content = re.sub('\”', '\"', content)
		content = re.sub('\‘', '\'', content)
		content = re.sub('\’', '\'', content)
		content = content.replace("/n", "")

		return content

	def isHangul(self, text):
		hanCount = len(re.findall(u'[\u3130-\u318F\uAC00-\uD7A3]+', text))
		return hanCount > 0

	def removeBracket(self, content):
		for match in re.finditer(r'\((.*?)\)', content):
			matchText = match.group()
			removeText = matchText.lstrip('(')
			removeText = matchText.rstrip(')')   
			
			if(self.isHangul(removeText)):
				content = content.replace(matchText, "")
		return content

	def removeEmoji(self, content):
		emoji_pattern = re.compile("["
			u"\U0001F600-\U0001F64F"  # emoticons
			u"\U0001F300-\U0001F5FF"  # symbols & pictographs
			u"\U0001F680-\U0001F6FF"  # transport & map symbols
			u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
		"]+", flags=re.UNICODE)

		findEmoji = emoji_pattern.findall(content)
		if len(findEmoji) > 0:
			content = emoji_pattern.sub(r'', content)
		return content

	def contentAnalysis(self, content):
		self.temp_list = []
		self.sent_list = []
		fullSent_list = []
		# textLen = 0

		# ()안에 문장이 한글이면 삭제
		#content = self.removeBracket(content)
		content = self.quoteReplace(content)
		content = self.removeEmoji(content)

		# (), "" 문구 안에 문장이 짤리면 안됨
		content = self.separateExtraction(content)

		# 문장별 분석
		temp_list = re.split(r'다\.', content)
		for sent in temp_list:
			if len(sent) != 0 :
				lastWord = sent[-1].strip()
				if (lastWord != '.') and (len(lastWord) != 0):
					sent += '다.'
				self.sent_list.append(sent)
    
		for idx, sent in enumerate(self.sent_list):
			fullSent = self.mappingSentIndex(sent)
			fullSent = fullSent.strip()
			if len(fullSent) != 0:
				# textLen += len(fullSent)
				# if textLen <= 1024:
				fullSent_list.append(fullSent)
		
		for idx, sent in enumerate(fullSent_list):
			if(idx == 0 and re.match(r"\".+\"", sent)):
				fullSent_list.pop(0)

		# for idx, sent in enumerate(fullSent_list):
		# 	if idx < 3:
		# 		returnStatus["summary"] += sent

		return fullSent_list

	def keywordsIncludeContent(self, contents, keywords):
		refinedWord = []
		keywords = list(set(keywords))
		for keyword in keywords:
			removeText = [r"\)",r"\("]
			for rt in removeText:
				checkRe = re.search(rt, keyword)
				if checkRe:
					keyword = keyword.replace(checkRe.group(0),"")
					hangul = re.compile('[^ ㄱ-ㅣ가-힣]+') # 한글과 띄어쓰기를 제외한 모든 글자
					keyword = hangul.sub('', keyword) # 한글과 띄어쓰기를 제외한 모든 부분을 제거

			word = re.compile(keyword)
			existWord = word.search(contents)
			if existWord :
				refinedWord.append(keyword)

		return refinedWord

if __name__ == "__main__":
    text = """
    "2020년 3월 코로나 바이러스의 (괄호1 테스트 입니다.) 본격 확산 이후 증시에 입성했던 공모 ‘대어’ 주가가 줄줄이 곤두박질치는 중" 금융정보업체 에프앤가이드에 따르면, 2020년 코로나 확산 이후 증시에 상장한 종목은 모두 186개다. 이 가운데 10월 26일 종가 기준 (괄호2 테스트 입니다.) 공모가를 밑도는 종목이 71%(132개)다. 이들 종목의 공모가 대비 평균 하락률은 40%를 훌쩍 웃돈다. 2020년 3월 이후 증시에 입성한 10개 종목 중 7개 (괄호3 테스트 입니다.) 주가가 공모가 대비 40% 이상 하락했다는 의미다. 앞으로 미국 기준금리 인상이 수차례 남았고 경기 침체가 본격화하지 않았다는 점 등을 고려하면 낙폭은 더 깊어질 가능성이 높다. "특히 조 단위 시가총액 (괄호4 테스트 입니다.) 공모주를 일컫는 ‘대어’의 성적표는 더욱 처참하다." 카카오뱅크, 카카오페이 등은 공모가 대비 60% 이상 하락했고 SK아이이테크놀로지(SK IET)도 50%대 하락률을 기록 중이다. 손실률은 공모가를 기준으로 한 것이므로 상장 이후 시장가를 기준으로 잡으면 낙폭은 훨씬 더 크다.
    """
    
    textFormat = TextFormat()
    result = textFormat.contentAnalysis(text)
    print(result)

