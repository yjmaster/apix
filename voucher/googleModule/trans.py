import html
import requests

class Trans():
    def __init__(self):
        self.param = {
            "key":"AIzaSyDvbDSm-fEoQRyTBFmweKdzVAxwe0eCrrw",
            "alt": "json",
            "target":"ko" # 번역 할 언어
        }
        
        self.url = "https://translation.googleapis.com/language/translate/v2"

    def translate(self, obj, source):
        self.param["q"] = obj["text"]
        self.param["source"] = source # 번역대상 언어

        response = requests.get(self.url, self.param)
        if response.status_code == 200 :
            response = response.json()
            response = response['data']['translations'][0]['translatedText']
            text = html.unescape(response)
            result = {"success" : True, "text" : text}
            return result
