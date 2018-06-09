# _*_ coding: utf-8 _*_
__author__ = 'Huu'
__date__ = '2018/6/9 14:29'

import time,random
from rest_framework import serializers

from goods.models import Goods
from .models import ShoppingCart,OrderInfo,OrderGoods
from goods.serializer import GoodsSerializer

class ShoppingCartSDetailSerializer(serializers.ModelSerializer):
    goods=GoodsSerializer()
    class Meta:
        model=ShoppingCart
        fields="__all__"


class ShoppingCartSerializer(serializers.Serializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    nums=serializers.IntegerField(required=True,min_value=1,error_messages={
        "min_value":"商品数量不能小于1",
        "required":"请选择购买数量"
    })
    goods=serializers.PrimaryKeyRelatedField(required=True,queryset=Goods.objects.all())

    def create(self, validated_data):
        user=self.context["request"].user
        nums=validated_data["nums"]
        goods=validated_data["goods"]

        existed=ShoppingCart.objects.filter(goods=goods,user=user)
        if existed:
            existed=existed[0]
            existed.nums+=nums
            existed.save()
        else:
            existed=ShoppingCart.objects.create(**validated_data)
        return existed

    def update(self, instance, validated_data):
        instance.nums=validated_data["nums"]
        instance.save()
        return instance

class OrderInfoSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    pay_status=serializers.CharField(read_only=True)
    trade_no = serializers.CharField(read_only=True)
    order_sn = serializers.CharField(read_only=True)
    pay_time = serializers.DateTimeField(read_only=True)
    add_time = serializers.DateTimeField(read_only=True)

    def generate_order_sn(self):
        order_sn="{time_str}{userid}{randstr}".format(time_str=time.strftime("%Y%m%d%H%M%S"),userid=self.context["request"].user.id,randstr=random.Random().randint(10,99))
        return  order_sn

    #生成并添加订单号
    def validate(self, attrs):
        attrs["order_sn"]=self.generate_order_sn()
        return attrs

    class Meta:
        model=OrderInfo
        fields="__all__"

class OrderGoodsSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer()
    class Meta:
        model = OrderGoods
        fields = "__all__"


class OrderInfoDetailSerializer(serializers.ModelSerializer):
    goods=OrderGoodsSerializer(many=True)
    class Meta:
        model=OrderInfo
        fields="__all__"