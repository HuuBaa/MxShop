from django.shortcuts import render
from rest_framework import mixins,viewsets
from .serializer import UserFavSerializer,UserFavDetailSerializer,UserLeavingMessageSerializer,UserAddressSerializer
from .models import UserFav,UserLeavingMessage,UserAddress
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from utils.permissions import IsOwnerOrReadOnly


# Create your views here.
class UserFavViewSet(mixins.RetrieveModelMixin,mixins.CreateModelMixin,mixins.ListModelMixin,mixins.DestroyModelMixin,viewsets.GenericViewSet):
    """
    list:
        用户收藏列表
    retrieve:
        判断某个商品是否收藏
    create:
        收藏商品
    """
    permission_classes =(IsAuthenticated,IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication,SessionAuthentication)
    lookup_field = "goods_id"

    def get_serializer_class(self):
        if self.action=="list":
            return UserFavDetailSerializer
        return UserFavSerializer

    def get_queryset(self):
        return UserFav.objects.filter(user=self.request.user)

class UserLeavingMessageViewSet(mixins.CreateModelMixin,mixins.ListModelMixin,mixins.DestroyModelMixin,viewsets.GenericViewSet):
    """
    list:
        获取用户留言
    create:
        创建用户留言
    delete:
        删除用户留言
    """
    serializer_class = UserLeavingMessageSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get_queryset(self):
        return UserLeavingMessage.objects.filter(user=self.request.user)

class UserAddressViewSet(viewsets.ModelViewSet):
    """
    收货地址管理
    list:
        获取收货地址
    create:
        创建收货地址
    delete:
        删除收货地址
    update:
        更新收货地址
    """
    serializer_class = UserAddressSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)