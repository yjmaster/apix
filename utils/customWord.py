# -*- coding: utf-8 -*-
import re
class CustomWord:
	def __init__(self):
		self.countries = {
			'한중':['한국','중국'],
			'한미':['한국','미국'],
			'미중':['미국','중국']
		}

	def countryNameParsing(self, contents, keywords):
		isCountryInKeywords = False
		for idx, keyword in enumerate(keywords):
			if keyword in self.countries:
				isCountryInKeywords = True
				country_detail = self.countries[keyword]
    
				for name in country_detail:
					isCountryInContent = False
					word = re.compile(name)
					existWord = word.search(contents)
					if existWord:
						if existWord.group() in country_detail:
							isCountryInContent = True
				if isCountryInContent:
					del keywords[idx]
					for detail in country_detail:
						keywords.insert(idx, detail)
						idx += 1

					keywords = list(set(keywords))
					return keywords
				else:
					return keywords

		if not isCountryInKeywords:
			return keywords

# if __name__ == "__main__":
#     contents = """
# 	회식 자리에서 미국 중국 술을 마신 뒤 차량을 몰다가 사고를 내고 도주한 현직 경찰관이 음주운전으로 수사를 받았으나 증거가 없어 결국 무혐의 처분을 받았다.

# 	인천경찰청 교통조사계는 중부경찰서 소속 A 경장을 도로교통법상 사고 후 미조치 혐의로만 검찰에 송치하고 음주운전 혐의는 불송치 결정을 했다고 21일 밝혔다.

# 	A 경장은 지난 9월 14일 오전 0시 30분께 인천시 중구 신흥동 한 도로에서 술을 마신 상태로 차량을 몰다가 중앙분리대를 들이받고 도주한 혐의를 받고 있다.

# 	그는 사고를 낸 당일 새벽 경찰관의 전화를 받고 뒤늦게 경찰서에 출석했지만 음주 측정을 받지 않고 그냥 집으로 돌아갔다.

# 	아침이 돼서야 경찰서 안에 소문이 퍼지면서 오후 무렵 음주 측정을 받았지만, 사고를 내고 이미 10시간 넘게 지난 뒤여서 혈중알코올농도 수치가 전혀 나오지 않았다.

# 	경찰은 음주운전을 한 의혹이 있는 A 한중 경장을 상대로 '위드마크' 공식을 적용해 2개월가량 수사를 했다.

# 	위드마크 공식은 마신 술의 농도, 음주량, 체중, 성별 등을 고려해 시간 경과에 따른 혈중알코올농도를 역추산하는 수사 기법이다.

# 	A 경장은 경찰 조사에서 소주와 맥주를 번갈아 가면서 여러 잔을 마시고 운전한 사실을 인정했고, 경찰도 회식 장소 내 폐쇄회로(CC)TV를 통해 그의 음주 장면을 확인했다.

# 	그러나 위드마크 공식을 적용해 추정한 사고 당시 A 경장의 혈중알코올농도는 처벌 기준(0.03%)을 넘지 않았다.

# 	경찰 관계자는 "피의자도 술을 마시고 운전한 사실은 인정했지만 사고 당시 측정된 혈중알코올농도 수치가 없어 수사가 오래 걸렸다"며 "결국 증거 불충분으로 혐의없음 처분을 할 수밖에 없었다"고 말했다.

# 	인천경찰청 감찰계는 경찰서 소환 직후 A 경장을 상대로 음주 측정을 하지 않고 그냥 집으로 돌려보낸 중부서 교통조사팀 소속 B 경사를 최근 직무유기 혐의로 불구속 입건했다.

# 	또 B 경사에게 "한번 봐 달라"며 음주 측정을 하지 말아 달라고 부탁한 중부서 소속 C 경감도 같은 혐의로 입건했다.

# 	B 경사와 C 경감은 같은 경찰서에서 근무하며 서로 알고 지낸 사이였으며 C 경감은 A 경장이 당시 근무한 부서 팀장이었다.

# 	조사 결과 B 경사는 A 경장을 소환한 사고 당일 C 경감에게 먼저 전화를 걸어 "부하직원이 조사받고 있다"고 알린 것으로 드러났다.

# 	경찰 관계자는 "A 경장의 사고 후 미조치 사건과 별도로 다른 경찰관들을 직무유기 혐의로 계속 수사하고 있다"며 "직무유기 혐의와 관련해서는 확인할 부분이 많이 시간이 더 걸릴 예정"이라고 말했다.
# 	"""

# keywords = ['중부서', '음주운전', '회식', '인천경찰청', '미중','한중']
# # keywords = ['중부서', '음주운전', '회식', '인천경찰청']
# customWord = CustomWord()
# res = customWord.countryNameParsing(contents, keywords)

# print(res)
