text = '''
500대 기업 기부금 내역 공시한 기업 257곳 중 1635억원 증가.삼성전자·SK하이닉스·LG생활건강·현대차·포스코 등 순.교보생명 기부금 증가액 가장 커...보험사 '자존심' 지켰다
'''
from konlpy.tag import Kkma
kkma = Kkma()
s = kkma.sentences(text)
print(s)