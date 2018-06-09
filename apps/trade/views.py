from django.shortcuts import render

# Create your views here.

import time,random

from .models import ShoppingCart,OrderInfo,OrderGoods
from rest_framework import viewsets,mixins
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from utils.permissions import IsOwnerOrReadOnly

from .serializers import ShoppingCartSerializer,ShoppingCartSDetailSerializer,OrderInfoSerializer,OrderInfoDetailSerializer



class ShoppingCartViewSet(viewsets.ModelViewSet):
    """
    购物车功能
    list:
        获取购物车详情
    create:
        加入购物车
    delete:
        删除商品
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    lookup_field = "goods_id"

    def get_serializer_class(self):
        if self.action=="list":
            return ShoppingCartSDetailSerializer
        return ShoppingCartSerializer

    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user)

class OrderInfoViewSet(mixins.RetrieveModelMixin,mixins.ListModelMixin,mixins.DestroyModelMixin,mixins.CreateModelMixin,viewsets.GenericViewSet):
    """
    订单管理
    list:
        获取个人全部订单
    create:
        创建订单
    delete:
        删除订单
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = OrderInfoSerializer

    def get_queryset(self):
        return OrderInfo.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action=="retrieve":
            return OrderInfoDetailSerializer
        return OrderInfoSerializer

    def perform_create(self, serializer):
        order=serializer.save()
        #根据购物车创建订单
        shop_carts=ShoppingCart.objects.filter(user=self.request.user)
        for shop_cart in shop_carts:
            order_goods=OrderGoods()
            order_goods.goods=shop_cart.goods
            order_goods.goods_num = shop_cart.nums
            order_goods.order = order
            order_goods.save()
            shop_cart.delete()
        return order