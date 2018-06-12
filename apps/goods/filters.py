# _*_ coding: utf-8 _*_
__author__ = 'Huu'
__date__ = '2018/6/5 13:13'

from django.db.models import Q

import django_filters
from .models import Goods

class GoodsFilter(django_filters.rest_framework.FilterSet):
    """
    商品过滤类
    """

    pricemin=django_filters.NumberFilter(name="shop_price",lookup_expr="gt",help_text="最低价格")
    pricemax = django_filters.NumberFilter(name="shop_price", lookup_expr="lt")
    #name=django_filters.CharFilter(name="name",lookup_expr="icontains")
    top_category=django_filters.NumberFilter(method="top_category_filter")

    def top_category_filter(self,queryset,name,value):
        queryset=queryset.filter(Q(category_id=value)|
                                 Q(category__parent_category__parent_category_id=value)|
                                 Q(category__parent_category_id=value))
        return queryset

    class Meta:
        model=Goods
        fields=["pricemin","pricemax","top_category","is_hot","is_new"]
