# _*_ coding: utf-8 _*_
__author__ = 'Huu'
__date__ = '2018/6/4 19:04'

import json

from django.views.generic.base import View
#from django.views.generic import ListView
from goods.models import Goods
from django.http import  HttpResponse,JsonResponse
from django.forms.models import model_to_dict
from django.core import serializers


class GoodsListView(View):
    def get(self,request):
        """
        通过django的view实现商品列表页
        :param request:
        :return:
        """

        goods=Goods.objects.all()[:10]

        # json_list=[]
        # for good in goods:
        #     json_dict=model_to_dict(good)
        #     json_list.append(json_dict)

        json_data=serializers.serialize("json",goods)
        json_data=json.loads(json_data) #转换成dict类型
        return JsonResponse(json_data,safe=False)