# -*- coding: utf-8 -*-
"""drf_poc URL Configuration

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
from django.conf.urls import url, include
from django.contrib import admin

# app01: 是为了研究权限、认证、节流
# app02: 是为了研究序列化，所以 app02 的 views 中的视图类的
# authentication_classes   permission_classes    throttle_classes 是空
# app03: 是为了研究 django 的 content type
from app01 import views
from app02 import views as app02_view
from app03 import views as app03_view
from rest_framework import routers
app02_router = routers.DefaultRouter()
app02_router.register(r'autoregister', app02_view.RoleViewSet)

from rest_framework.authtoken import views as drf_auth_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^misctest$', views.misctest),
    url(r'^hello/', views.hello),
    url(r'^hello1/', views.hello1),
    url(r'^signal_poc/', views.signal_poc),
    url(r'^concurrence/', views.concurrence),
    # 认证 View: 请求body 带上用户名和密码; 返回给前端 token
    url(r'^api/v1/auth/', views.AuthView.as_view()),
    # 业务 View
    url(r'^api/v1/order/', views.OrderView.as_view()),
    url(r'^api/v1/bonus/', views.BonusView.as_view()),
    # other test
    url(r'^api/v1/HelloCBV/', views.HelloCBVView.as_view()),

    # 获取版本:
    # case 1: 通过 get 请求 URL 中问号后的参数来获取版本
    url(r'^api/EvolView/', views.EvolView.as_view()),
    # case 2: 通过 URL 本身来获取即正则解析 URL 从中获取版本的信息，推荐该方式
    url(r'^api/(?P<version>[v1|v2]+)/EvolEnView/', views.EvolEnView.as_view()),
    # 获取解析器
    url(r'^api/ParserView/', views.ParserView.as_view()),

    # 学习 serializer
    url(r'^api/app02/role/$', app02_view.RoleView.as_view()),
    url(r'^api/app02/consumer/$', app02_view.ConsumerView.as_view()),
    # 因为在 settings.py 中配置了 DEFAULT_VERSIONING_CLASS = rest_framework.versioning.URLPathVersioning，
    # 所以在测试 serializers.HyperlinkedIdentityField 时，如果其参数 view_name 对应的 url 的定义是:
    # url(r"^api/app02/group/(?P<pk>\d+)/$", app02_view.ConsumerGroupView.as_view(), name="gpd"),
    # 则会报错：Reverse for 'gpd' with keyword arguments '{u'pk': 1L, 'version': 'v1'}' not found. 1 pattern(s) tried: ['api/app02/group/(?P<pk>\\d+)/$']
    # 原因参考代码 rest_framewor/versioning.py 类 URLPathVersioning 的 reverse，所以改成下面的写法
    url(r"^api/(?P<version>[v1|v2]+)/app02/group/(?P<pk>\d+)/$", app02_view.ConsumerGroupDetailView.as_view(), name="gpd"),
    url(r"^api/(?P<version>[v1|v2]+)/app02/group/$", app02_view.ConsumerGroupView.as_view()),

    # 分页
    url(r"^api/app02/pagenumberpage/$", app02_view.PageNumberView.as_view()),
    # url(r"^api/app02/limitoffsetpage/$", app02_view.LimitOffsetView.as_view()),
    url(r"^api/app02/cursorpage/$", app02_view.CursorView.as_view()),

    # 视图：
    url(r"^api/app02/viewset/$", app02_view.RoleViewSet.as_view({'get':'list','post':'create'})),
    url(r"^api/app02/viewset/(?P<pk>\d+)$", app02_view.RoleViewSet.as_view({'get':'retrieve','delete':'destroy',
                                                                            'put':'update', 'patch':'partial_update'})),
    # 用自动注册的方法会帮生成 4 个 URL, 可以通过故意输错 URL http://192.168.56.101:8082/autoregisterrrr 来看到
    # http://192.168.56.101:8082/autoregister
    # http://192.168.56.101:8082/autoregister.json
    # 来自 P53: day131-06 rest framework之视图
    url(r'^', include(app02_router.urls)),

    # 学习 django 的 content-type,注意在settings.py 的 INSTALLED_APPS 中已安装了 contenttypes
    url(r"^api/app03/poc_contenttype/$", app03_view.poc_contenttype),

    # 学习 restframework 的 login 和 TokenAuthentication
    # https://blog.csdn.net/qq_39980136/article/details/89503850
    url(r'^drf/', include('rest_framework.urls')),
    url(r'^drf_token/', drf_auth_views.obtain_auth_token),
    url(r'^auth/', include('django.contrib.auth.urls')),
]


