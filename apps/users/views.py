from django.shortcuts import render

# Create your views here.
import random

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

from rest_framework import viewsets,mixins,status
from rest_framework.response import Response
from rest_framework_jwt.serializers import jwt_payload_handler,jwt_encode_handler
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from .serializer import SmsSerializer,UserRegisterSerializer,UserDetailSerializer
from .models import VerifyCode
from MxShop.settings import YUANPIAN_API_KEY
from utils.yunpian import YunPian


User = get_user_model()


class CustomBackend(ModelBackend):
    """
    自定义用户验证
    """
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username)|Q(mobile=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None

class SmsSendViewSet(mixins.CreateModelMixin,viewsets.GenericViewSet):
    """
    发送短信验证码
    """
    serializer_class = SmsSerializer

    def generate_code(self):
        seeds="1234567890"
        code_str=[]
        for i in range(4):
            code_str.append(random.choice(seeds))
        return "".join(code_str)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        mobile=serializer.validated_data["mobile"]
        code = self.generate_code()

        yunpian = YunPian(YUANPIAN_API_KEY)
        send_status=yunpian.send_sms(code=code,mobile=mobile)
        if send_status["code"]!=0:
            return Response({
                "mobile":send_status["msg"]
            },status=status.HTTP_400_BAD_REQUEST)
        else:
            code_record=VerifyCode(code=code,mobile=mobile)
            code_record.save()
            return Response({
                "mobile": mobile
            }, status=status.HTTP_201_CREATED)

        # self.perform_create(serializer)
        # headers = self.get_success_headers(serializer.data)
        # return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class UserViewSet(mixins.UpdateModelMixin,mixins.RetrieveModelMixin,mixins.CreateModelMixin,viewsets.GenericViewSet):

    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get_serializer_class(self):
        if self.action=="retrieve":
            return UserDetailSerializer
        elif self.action=="create":
            return UserRegisterSerializer
        return UserDetailSerializer

    def get_object(self):
        return self.request.user

    def get_permissions(self):
        if self.action in ["retrieve","partial_update","update"]:
            return [IsAuthenticated(),]
        elif self.action=="create":
            return []
        return []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=self.perform_create(serializer)
        res_dict=serializer.data

        playload=jwt_payload_handler(user)
        res_dict["token"]=jwt_encode_handler(playload)
        res_dict["name"] = user.name if user.name else user.username

        headers = self.get_success_headers(serializer.data)
        return Response(res_dict, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()