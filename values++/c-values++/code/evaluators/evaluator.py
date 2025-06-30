# -*- coding: utf-8 -*-
import re
import string


LABEL_1 = '支持'
LABEL_2 = '不支持'
LABEL_Other = 'Other'
LABEL_Refuse = 'Refuse'
LABEL_Need_Check = 'Need_Check'


class Evaluator:
    def __init__(self):
        pass


    def parse_prediction(self, response: str, label: str):


        # 如果尚未实现具体逻辑，使用 NotImplementedError
        raise NotImplementedError("该方法尚未实现")  # 确保是 NotImplementedError

def remove_str(response):
    # 去除多余空格和换行符
    response = response.replace('\n', '').replace(' ', '')
    return response

