# _*_ coding: utf-8 _*_
__author__ = 'Huu'
__date__ = '2018/6/7 20:27'

import re
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from MxShop.settings import MOBILE_REG
from .models import UserFav,UserAddress,UserLeavingMessage
from goods.serializer import GoodsSerializer

class UserFavDetailSerializer(serializers.ModelSerializer):
    goods=GoodsSerializer()
    class Meta:
        model=UserFav
        fields=["goods","id"]

class UserFavSerializer(serializers.ModelSerializer):
    user=serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model=UserFav
        validators=[
            UniqueTogetherValidator(queryset=UserFav.objects.all(),
                                    fields=['goods','user'],message="已经收藏")
        ]
        fields=["user","goods","id"]

class UserLeavingMessageSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    add_time=serializers.DateTimeField(read_only=True,format="%Y-%m-%d %H:%M")

    class Meta:
        model=UserLeavingMessage
        fields="__all__"

class UserAddressSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    add_time = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M")

    def validate_signer_mobile(self, signer_mobile):
        if not re.match(MOBILE_REG,signer_mobile):
            raise serializers.ValidationError("手机号码不合法")
        return signer_mobile

    class Meta:
        model=UserAddress
        fields = "__all__"
