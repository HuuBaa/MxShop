"""MxShop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_jwt.views import obtain_jwt_token

import xadmin
from goods.views import GoodsListViewSet,CategoryViewSet
from users.views import SmsSendViewSet,UserViewSet
from user_operation.views import UserFavViewSet,UserLeavingMessageViewSet,UserAddressViewSet
from trade.views import ShoppingCartViewSet,OrderInfoViewSet

# from django.contrib import admin
router=DefaultRouter()
router.register(r'goods',GoodsListViewSet,base_name="goods")
router.register(r'categorys',CategoryViewSet,base_name="categorys")
router.register(r'codes',SmsSendViewSet,base_name="codes")
router.register(r'users',UserViewSet,base_name="users")
router.register(r'userfavs',UserFavViewSet,base_name="userfavs")
router.register(r'messages',UserLeavingMessageViewSet,base_name="messages")
router.register(r'address',UserAddressViewSet,base_name="address")
router.register(r'shopcarts',ShoppingCartViewSet,base_name="shopcarts")
router.register(r'orders',OrderInfoViewSet,base_name="orders")


urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls')),
    url(r'^doc/', include_docs_urls(title="慕学生鲜")),

    url(r'^',include(router.urls)),
    #drf自带token认证
    url(r'^api-token-auth/',obtain_auth_token),
    #jwt认证
    url(r'^login/',obtain_jwt_token)

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
