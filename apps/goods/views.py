from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, mixins, generics, viewsets, filters
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_extensions.mixins import CacheResponseMixin
from rest_framework.throttling import UserRateThrottle,AnonRateThrottle
from .models import Goods, GoodsCategory, Banner
from .serializer import GoodsSerializer, CategorySerializer, BannerSerializer, IndexCategorySerializer
from .filters import GoodsFilter


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    page_query_param = "page"
    max_page_size = 100


class CategoryViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    list:
        一级分类数据列表
    retrieve:
        单个类别详情
    """
    queryset = GoodsCategory.objects.all().order_by("id").filter(category_type=1)
    serializer_class = CategorySerializer


class GoodsListViewSet(CacheResponseMixin,mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    列出所有商品,分页，搜索，过滤，排序
    """
    queryset = Goods.objects.all().order_by("id")
    serializer_class = GoodsSerializer
    pagination_class = StandardResultsSetPagination
    throttle_classes = (UserRateThrottle,AnonRateThrottle)

    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)

    filter_class = GoodsFilter
    search_fields = ("name", "goods_brief", "goods_desc")
    ordering_fields = ("sold_num", "shop_price")

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.click_num += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class BannerViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    商品轮播图
    """
    serializer_class = BannerSerializer
    queryset = Banner.objects.all().order_by("index")


class IndexCategoryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    主页展示类
    """
    queryset = GoodsCategory.objects.filter(is_tab=True, name__in=["酒水饮料", "生鲜食品"])
    serializer_class = IndexCategorySerializer
