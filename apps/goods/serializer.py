# _*_ coding: utf-8 _*_
__author__ = 'Huu'
__date__ = '2018/6/4 20:11'

from rest_framework import serializers

from goods.models import Goods,GoodsCategory,GoodsImage

class CategorySerializer3(serializers.ModelSerializer):
    class Meta:
        model=GoodsCategory
        fields="__all__"


class CategorySerializer2(serializers.ModelSerializer):
    sub_cat = CategorySerializer3(many=True)
    class Meta:
        model=GoodsCategory
        fields="__all__"

class CategorySerializer(serializers.ModelSerializer):
    sub_cat=CategorySerializer2(many=True)
    class Meta:
        model=GoodsCategory
        fields="__all__"


class GoodsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model=GoodsImage
        fields=("image",)

class GoodsSerializer(serializers.ModelSerializer):
    category=CategorySerializer()
    images=GoodsImageSerializer(many=True)
    class Meta:
        model=Goods
        fields="__all__"


