from flask import request, make_response, render_template
from flask_restx import Resource, Namespace
# -*- coding: utf-8 -*-
import torch
from transformers import PreTrainedTokenizerFast
from transformers.models.bart import BartForConditionalGeneration

todos = {}
count = 1


Kobart = Namespace(
    name="kobart",
    description="kobart 테스트 API.",
)

model = BartForConditionalGeneration.from_pretrained('./kobart_summary_epoch0')
tokenizer = PreTrainedTokenizerFast.from_pretrained('gogamza/kobart-base-v1')

@Kobart.route('')
class KobartGet(Resource):
    def get(self):
        """kobart 모델을 통해 제목을 가져옵니다."""

        
        text = request.args.get("text")
        input_ids = tokenizer.encode(text)
        input_ids = torch.tensor(input_ids)
        input_ids = input_ids.unsqueeze(0)
        output = model.generate(input_ids, eos_token_id=1, max_length=30, num_beams=5)
        output = tokenizer.decode(output[0], skip_special_tokens=True)
        
        return {
            'title': output,
        }, 200
        
@Kobart.route('/test')
class KobartTest(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('test.html'),200,headers)

