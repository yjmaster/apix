import json
import requests
from urllib import parse
from datetime import datetime
from datetime import timedelta
from ASIA_TIMES_data_voucher.eng_senti.infer_senti import eng_senti

ASIA_TIMES_ENG_SENTI = eng_senti()


class GSE():
    def __init__(self, issueDB, newsDB):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/61.0.3163.100 Safari/537.36'}

        self.emotion_url = "http://192.168.0.118:10001/extractor/AT_SENTI"

        self.API_KEY = "AIzaSyDJTDI0bV5D6o9Unagq9Qm8kPbEyQY_8KI"
        self.SEARCH_ENGINE_ID = "4223efd72e7964b36"
        
        self.itemList = []
        self.query = ""
        self.area = ""
        self.start = 1

        self.issueDB = issueDB
        self.newsDB = newsDB

        self.result = {"success" : True}

    def saveItemList(self, status=None):
        try:
            if status is None:
                insert_resut = self.newsDB.INSERT(self.itemList)
                if insert_resut["success"] :
                    self.result["message"] = "수집이 완료되었습니다."
                    self.result["success"] = True
                    print("================== INSERT OK ==================" , end='\n')
         
            elif "error" in status :
                if status["error"]["code"] == 429 :
                    self.result["message"] = "호출 횟수를 초과하였습니다."
                    self.result["success"] = False
                    print("================== LIMIT ERROR ==================")
            else:
                self.result["message"] = "수집된 기사가 없습니다."
                self.result["success"] = False
                print("================== NO RESULT ==================")
        except Exception as exp:
            self.result["message"] = exp
            self.result["success"] = False
            print("================== INSERT FAIL ==================")
        return

    def siteAnalysis(self, url):
        try:
            today = datetime.now()
            response = requests.get(url, headers=self.headers)  
            siteInfo = json.loads(response.text)

            if "items" in siteInfo :
                for idx, item in enumerate(siteInfo["items"]) :
                    image = ""
                    try: image = item["pagemap"]["cse_image"][0]["src"]
                    except KeyError : pass

                    summary = item["snippet"].split(' ... ', 1)

                    date = ""
                    if "days" in summary[0] :
                        days = int(summary[0].split(" ")[0])
                        date = (today - timedelta(days)).strftime('%Y-%m-%d')
                    else :
                        date = today.strftime('%Y-%m-%d')

                    senti_param = {"contents":item["title"]}
                    gpt = ASIA_TIMES_ENG_SENTI.eng_senti_infer(str(item["title"]))
                    emotion = gpt 
                    #response = requests.post(url = self.emotion_url,
                    #    data=json.dumps(senti_param), headers={'Content-Type': 'application/json'})

                    #if response.status_code == 200 :
                    #    res = response.json()
                    #    emotion = res["extractor"]

                    obj = {
                        "title" : item["title"],
                        "link" : item["link"],
                        "date" : date,
                        "summary" : summary[1],
                        "image" : image,
                        "keyword" : self.query,
                        "area" : self.area,
                        "emotion": emotion
                    }

                    self.itemList.append(obj)

                if "nextPage" in siteInfo["queries"] :
                    nextPage = siteInfo["queries"]["nextPage"][0]
                    startIndex = nextPage["startIndex"]
                    self.start = startIndex
                    self.parseUrl()
                else : #pass
                    self.saveItemList()
            else : #pass
                self.saveItemList(siteInfo)

        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)
         
    def parseUrl(self):
        url = "https://www.googleapis.com/customsearch/v1?key={}&cx={}&q={}"\
            "&dateRestrict=d1&filter=0&sort=date&start={}"\
            .format(self.API_KEY, self.SEARCH_ENGINE_ID, self.searchTerms, self.start)

        print(url, end='\n\n')
        print('=====================================================================')

        self.siteAnalysis(url) 

    def setParameter(self, obj):
        startTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print("[{}] start collecting articles".format(startTime), end='\n')
        
        IssueList = self.issueDB.SELECT(obj)
        for row in IssueList:
            self.start = 1
            link_list = row["links"]

            siteKeyword = ""
            for idx, links in enumerate(link_list):
                siteKeyword += "site:"+links["link"] + (" OR " if idx != len(link_list)-1 else "") 

            self.query = row["keyword"]
            self.area = row["area"]

            print('searching about "{}"'.format(self.query), end='\n')
            siteKeyword += " intitle:{}".format(self.query)
            print(siteKeyword, end='\n\n')

            self.searchTerms = parse.quote(siteKeyword)

            self.parseUrl()

        return self.result