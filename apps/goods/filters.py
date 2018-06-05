# _*_ coding: utf-8 _*_
__author__ = 'Huu'
__date__ = '2018/6/5 13:13'

import django_filters
from .models import Goods

class GoodsFilter(django_filters.rest_framework.FilterSet):
    """
    商品过滤类
    """
    price_min=django_filters.NumberFilter(name="shop_price",lookup_expr="gt")
    price_max = django_filters.NumberFilter(name="shop_price", lookup_expr="lt")
    #name=django_filters.CharFilter(name="name",lookup_expr="icontains")
    class Meta:
        model=Goods
        fields=["price_min","price_max"]
