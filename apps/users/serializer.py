# _*_ coding: utf-8 _*_
__author__ = 'Huu'
__date__ = '2018/6/7 9:35'

import datetime
import re

from rest_framework import  serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator

from MxShop.settings import MOBILE_REG
from .models import VerifyCode


User=get_user_model()

class SmsSerializer(serializers.Serializer):
    mobile=serializers.CharField(max_length=11,label="手机号码",help_text="手机号码")

    def validate_mobile(self, mobile):

        if not re.match(MOBILE_REG,mobile):
            raise serializers.ValidationError("手机号码不合法")

        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError("用户已经存在")

        one_minute_ago=datetime.datetime.now()-datetime.timedelta(minutes=1)
        if VerifyCode.objects.filter(add_time__gt=one_minute_ago,mobile=mobile).count():
            raise  serializers.ValidationError("距离上一次发送未超过1分钟")

        return mobile

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["name","gender","birthday","email","mobile"]


class UserRegisterSerializer(serializers.ModelSerializer):
    code=serializers.CharField(write_only=True,max_length=4,min_length=4,required=True,label="验证码",error_messages={
            "required":"请填写验证码",
            "max_length":"验证码格式错误",
            "min_length":"验证码格式错误"
        },help_text="验证码")
    username=serializers.CharField(label="用户名",validators=[
        UniqueValidator(queryset=User.objects.all(),message="用户已经存在")
    ])
    mobile=serializers.CharField(required=False,allow_null=True,label="手机号码")
    password=serializers.CharField(write_only=True,required=True,label="密码",style={
        "input_type":"password"
    })

    def validate_code(self,code):
        code_record=VerifyCode.objects.filter(mobile=self.initial_data["username"]).order_by("-add_time")
        if code_record:
            last_code=code_record[0]

            five_minute_ago = datetime.datetime.now() - datetime.timedelta(minutes=5)
            if last_code.add_time < five_minute_ago:
                raise serializers.ValidationError("验证码过期")

            if last_code.code!=code:
                raise serializers.ValidationError("验证码错误")
        else:
            raise serializers.ValidationError("验证码错误")

    def validate(self, attrs):
        username=attrs["username"]
        attrs["mobile"]=username
        del attrs["code"]
        return attrs


    class Meta:
        model=User
        fields=["username","password","code","mobile"]