from flask import request
from . import kobart_v1

from kobart_modules.inference2 import kobart_inference_API
kobart_api = kobart_inference_API()

from classification_modules.inference2 import classification_inference_API
classification_api = classification_inference_API()

from utils.textFormat import TextFormat
from utils.customWord import CustomWord

textFormat = TextFormat()
customWord = CustomWord()

@kobart_v1.route('/keyword', methods=['POST'])
def keyword():
	try:
		res = {"success": True, "extractor": ""}
		params = request.get_json()
		title = params['title']
		content = params['content']
		summary = params['summary']

		total_contents = (title + ' ' + content)
		keyword1 = kobart_api.kobart_keyword(total_contents)
		if not keyword1['success']:
			res = keyword1
			return

		keyword2 = kobart_api.kobart_keyword(summary)
		if not keyword2['success']:
			res = keyword2
			return

		k1 = keyword1["extractor"].split("/")
		k2 = keyword2["extractor"].split("/")

		keywords = (k1 + k2)
		keywords = customWord.countryNameParsing(total_contents, keywords)
		keywords = textFormat.keywordsIncludeContent(total_contents, keywords)

		res["extractor"] = keywords

	except Exception as exp:
		res = {"success": False, "code": 400, "message": str(exp)}
	finally:
		return res

@kobart_v1.route('/topic', methods=['POST'])
def topic():
	try:
		res = {"success": True, "extractor": ""}
		params = request.get_json()
		title = params['title']
		content = params['content']

		total_contents = (title + ' ' + content)
		topic = classification_api.topic(total_contents)
		if not topic['success']:
			res = topic
			return

		res["extractor"] = topic["extractor"]

	except Exception as exp:
		res = {"success": False, "code": 400, "message": str(exp)}
	finally:
		return res