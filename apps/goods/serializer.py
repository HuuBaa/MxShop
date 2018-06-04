# _*_ coding: utf-8 _*_
__author__ = 'Huu'
__date__ = '2018/6/4 20:11'

from rest_framework import serializers

from goods.models import Goods,GoodsCategory


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=GoodsCategory
        fields="__all__"

class GoodsSerializer(serializers.ModelSerializer):
    category=CategorySerializer()

    class Meta:
        model=Goods
        fields="__all__"


    # goods_sn = serializers.CharField(max_length=50, default="")
    # name = serializers.CharField(required=True, max_length=100)
    # goods_front_image = serializers.ImageField() \
    #
    # def create(self, validated_data):
    #     """
    #     Create and return a new `Goods` instance, given the validated data.
    #     """
    #     return Goods.objects.create(**validated_data)
