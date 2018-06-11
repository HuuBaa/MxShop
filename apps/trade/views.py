from django.shortcuts import render

# Create your views here.

import time, random
from datetime import datetime
from django.shortcuts import redirect
from .models import ShoppingCart, OrderInfo, OrderGoods
from rest_framework import viewsets, mixins, views
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from utils.permissions import IsOwnerOrReadOnly

from utils.alipay import AliPay
from MxShop.settings import private_key_path, ali_pub_key_path
from .serializers import ShoppingCartSerializer, ShoppingCartSDetailSerializer, OrderInfoSerializer, \
    OrderInfoDetailSerializer


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
        if self.action == "list":
            return ShoppingCartSDetailSerializer
        return ShoppingCartSerializer

    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user)


class OrderInfoViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin,
                       mixins.CreateModelMixin, viewsets.GenericViewSet):
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
        if self.action == "retrieve":
            return OrderInfoDetailSerializer
        return OrderInfoSerializer

    def perform_create(self, serializer):
        order = serializer.save()
        # 根据购物车创建订单
        shop_carts = ShoppingCart.objects.filter(user=self.request.user)
        for shop_cart in shop_carts:
            order_goods = OrderGoods()
            order_goods.goods = shop_cart.goods
            order_goods.goods_num = shop_cart.nums
            order_goods.order = order
            order_goods.save()
            shop_cart.delete()
        return order


class ReturnAlipayView(views.APIView):
    def get(self, request):

        processed_query = {}

        for key, value in request.GET.items():
            processed_query[key] = value

        ali_sign = processed_query.pop("sign", None)

        alipay = AliPay(
            appid="2016091300501657",
            app_notify_url="http://139.224.235.140:8000/alipay/return/",
            app_private_key_path=private_key_path,
            alipay_public_key_path=ali_pub_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url="http://139.224.235.140:8000/alipay/return/"
        )

        verify_re = alipay.verify(processed_query, ali_sign)
        print(verify_re)
        if verify_re is True:
            order_sn = processed_query.get('out_trade_no', None)
            trade_no = processed_query.get('trade_no', None)
            trade_status = processed_query.get('trade_status', None)

            existed_orders = OrderInfo.objects.filter(order_sn=order_sn)
            for existed_order in existed_orders:
                existed_order.pay_status = 'TRADE_SUCCESS'
                existed_order.trade_no = trade_no
                existed_order.pay_time = datetime.now()
                existed_order.save()

            response = redirect('/index/#/app/home/member/order')
            #response.set_cookie("nextPath", "pay", max_age=3)
            return response
        else:
            response = redirect('index')
            return response

    def post(self, request):

        processed_query = {}

        for key, value in request.POST.items():
            processed_query[key] = value

        ali_sign = processed_query.pop("sign")

        alipay = AliPay(
            appid="2016091300501657",
            app_notify_url="http://139.224.235.140:8000/alipay/return/",
            app_private_key_path=private_key_path,
            alipay_public_key_path=ali_pub_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url="http://139.224.235.140:8000/alipay/return/"
        )

        verify_re = alipay.verify(processed_query, ali_sign)
        if verify_re is True:
            order_sn = processed_query.get('out_trade_no', None)
            trade_no = processed_query.get('trade_no', None)
            trade_status = processed_query.get('trade_status', None)

            existed_orders = OrderInfo.objects.filter(order_sn=order_sn)
            for existed_order in existed_orders:
                existed_order.pay_status = 'TRADE_SUCCESS'
                existed_order.trade_no = trade_no
                existed_order.pay_time = datetime.now()
                existed_order.save()

            return Response('success')
