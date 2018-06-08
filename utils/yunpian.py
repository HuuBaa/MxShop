# _*_ coding: utf-8 _*_
__author__ = 'Huu'
__date__ = '2018/6/6 20:56'

import requests


class YunPian(object):

    def __init__(self, api_key):
        self.api_key = api_key
        self.single_url = "https://sms.yunpian.com/v2/sms/single_send.json"

    def send_sms(self, code, mobile):
        parmas={
            "apikey":self.api_key,
            "mobile":mobile,
            "text":"{code}".format(code=code)
        }
        res=requests.post(self.single_url,data=parmas)
        import json
        res_dict=json.loads(res.text)
        return res_dict

if __name__=="__main__":
    yunpian=YunPian("e2544837707f96fd0f2817b2e92f5507")
    yunpian.send_sms("5201","13123920239")