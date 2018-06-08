from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,mixins,generics,viewsets,filters
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

from .models import Goods,GoodsCategory
from .serializer import GoodsSerializer,CategorySerializer
from .filters import GoodsFilter

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    page_query_param = "page"
    max_page_size = 100

class CategoryViewSet(mixins.RetrieveModelMixin,mixins.ListModelMixin,viewsets.GenericViewSet):
    """
    list:
        一级分类数据列表
    retrieve:
        单个类别详情
    """
    queryset = GoodsCategory.objects.all().order_by("id").filter(category_type=1)
    serializer_class = CategorySerializer



class GoodsListViewSet(mixins.RetrieveModelMixin,mixins.ListModelMixin,viewsets.GenericViewSet):
    """
    列出所有商品,分页，搜索，过滤，排序
    """
    queryset = Goods.objects.all().order_by("id")
    serializer_class = GoodsSerializer
    pagination_class = StandardResultsSetPagination

    filter_backends = (DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter)

    filter_class=GoodsFilter
    search_fields=("name","goods_brief","goods_desc")
    ordering_fields=("sold_num","shop_price")


