# _*_ coding: utf-8 _*_
__author__ = 'Huu'
__date__ = '2018/6/4 20:11'

from rest_framework import serializers

from django.db.models import Q
from goods.models import Goods,GoodsCategory,GoodsImage,Banner,GoodsCategoryBrand,IndexAd

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


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Banner
        fields="__all__"

class BrandsSerializer(serializers.ModelSerializer):
    class Meta:
        model=GoodsCategoryBrand
        fields="__all__"

class IndexAdSerializer(serializers.ModelSerializer):
    class Meta:
        model=IndexAd
        fields="__all__"

class IndexCategorySerializer(serializers.ModelSerializer):
    brands=BrandsSerializer(many=True)
    goods=serializers.SerializerMethodField()
    sub_cat=CategorySerializer2(many=True)
    ad_goods=serializers.SerializerMethodField()

    def get_ad_goods(self,obj):
        ad_goods=IndexAd.objects.filter(category_id=obj.id)
        if ad_goods:
            ad_goods=ad_goods[0].goods
            goods_json=GoodsSerializer(ad_goods,many=False,context={'request':self.context['request']}).data
            return goods_json


    def get_goods(self,obj):
        all_goods=Goods.objects.filter(Q(category_id=obj.id)|
                                 Q(category__parent_category__parent_category_id=obj.id)|
                                 Q(category__parent_category_id=obj.id))
        goods_serializer=GoodsSerializer(all_goods,many=True,context={'request':self.context['request']})
        return goods_serializer.data

    class Meta:
        model=GoodsCategory
        fields="__all__"