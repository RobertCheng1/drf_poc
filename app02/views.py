# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse
from rest_framework.views import APIView
from rest_framework import serializers, generics
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.pagination import CursorPagination
from rest_framework.viewsets import ModelViewSet
# from rest_framework.decorators import list_route
from rest_framework.decorators import action
import logging
import json

from models import ConsumerGroup
from models import ConsumerInfo
from models import ConsumerToken
from models import Role
logger = logging.getLogger('drf_poc')


# Create your views here.
# Here1 Base:  序列化类继承的是 serializers.Serializer NOT serializers.ModelSerializer
class RoleSerializer(serializers.Serializer):
    role_name = serializers.CharField()

class RoleView(APIView):
    authentication_classes = []
    permission_classes = []
    throttle_classes = []

    def get(self, request, *args, **kwargs):
        # 方法 1:
        # objs = Role.objects.all()
        # logger.info('objs = {0}, type(objs) = {1}'.format(objs, type(objs)))
        #
        # values = Role.objects.all().values()
        # logger.info('values = {0}, type(values) = {1}'.format(values, type(values)))
        #
        # value_list = Role.objects.all().values_list()
        # logger.info('value_list = {0}, type(value_list) = {1}'.format(value_list, type(value_list)))
        # # 如果不用 serializer, 则可以先 xxx.objects.all().values(), 然后 list() ,在返回给前端
        # data = list(values)
        # # ensure_ascii 参数的作用:如果 data 里面有中文的话，返回到前端时也是显示中文
        # ret = json.dumps(data, ensure_ascii=False)
        #
        # 方法 2: 继承 APIView，然后定义一个 RoleSerializer(serializers.Serializer) 类
        objs = Role.objects.all()
        logger.info('objs = {0}, type(objs) = {1}'.format(objs, type(objs)))
        ser = RoleSerializer(instance=objs, many=True)
        ret = json.dumps(ser.data)
        return HttpResponse(ret)

# Here1 Advance:  序列化类继承的是 serializers.Serializer NOT serializers.ModelSerializer
# class ConsumerSerializer(serializers.Serializer):
#     id = serializers.CharField()
#     # 1. 对于指定 source 参数的 field, 其名字就不必和 model 中的列名一样了
#     # 2. 对于 source 的值是 callable, 框架会自动帮你调用，所以 get_user_type_display 是不用带括号的
#     # 3. 对于 source 可以一直 . 下去
#     # user_type = serializers.IntegerField()
#     user_type_desc = serializers.CharField(source='get_user_type_display')
#     # group = serializers.CharField()
#     group = serializers.CharField(source='group.title')
#     # rolesss = serializers.CharField(source='roles.all') # this is wrong
#     username = serializers.CharField()
#     password = serializers.CharField()
#     # 4. 想返回给用户不属于 model 的信息 或者 复杂的信息
#     other = serializers.SerializerMethodField()
#
#     def get_other(self, obj):
#         return 'this does NOT existed DB'
#
# Here2:  2_1. 序列化类继承的是 serializers.ModelSerializer NOT serializers.Serializer
#            其进步的地方在不用手写各个 field，框架会帮你自动构造的
#         2_2. 另外也可自定义 field 类,同时实现 to_representation 方法，实际用处不大，完全可用 SerializerMethodField 来做
class MyField(serializers.CharField):
    def to_representation(self, value):
        # 把对应的值转为大写
        logger.info('In the MyFiled, value = {0}'.format(value))
        return value.upper()
class ConsumerSerializer(serializers.ModelSerializer):
    # 2_3. 为某个字段生成超链接, 注意配置文件中配置了 DEFAULT_VERSIONING_CLASS
    # 所以 如果其参数 view_name 对应的 url 的定义是:
    # url(r"^api/app02/group/(?P<pk>\d+)/$", app02_view.ConsumerGroupView.as_view(), name="gpd"),
    # 则会报错：Reverse for 'gpd' with keyword arguments '{u'pk': 1L, 'version': 'v1'}' not found. 1 pattern(s) tried: ['api/app02/group/(?P<pk>\\d+)/$']
    # 原因参考代码 rest_framewor/versioning.py 类 URLPathVersioning 的 reverse，所以改成下面的写法
    # url(r"^api/(?P<version>[v1|v2]+)/app02/group/(?P<pk>\d+)/$", app02_view.ConsumerGroupView.as_view(), name="gpd"),
    #
    # group = serializers.CharField(source='group.title')
    group = serializers.HyperlinkedIdentityField(view_name="gpd", lookup_field="group_id", lookup_url_kwarg="pk")
    roles = serializers.SerializerMethodField()
    username = MyField()
    def get_roles(self, obj):
        role_list = obj.roles.all()
        ret = list()
        for role in role_list:
            ret.append({'id':role.id, 'role_name':role.role_name})
        return ret

    class Meta:
        model = ConsumerInfo
        # fields = '__all__'
        # exclude = ['id']
        fields = ['id', 'username', 'group', 'roles']

# Here3: 使用 depth 参数， 递归的深度， 可以把对应层次的 ForeignKey 的详情也返回出来
# class ConsumerSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ConsumerInfo
#         fields = '__all__'
#         depth = 1 # 该值默认是 0
#
class ConsumerView(APIView):
    authentication_classes = []
    permission_classes = []
    throttle_classes = []

    def get(self, request, *args, **kwargs):
        objs = ConsumerInfo.objects.all()
        print '---In the get of ConsumerView---'
        from rest_framework.versioning import URLPathVersioning
        version = getattr(request, 'version', None)
        scheme = getattr(request, 'versioning_scheme', None)
        print 'version = {0}'.format(version)
        print 'scheme = {0}, type(scheme) = {1}'.format(scheme, type(scheme))
        tmp = serializers.HyperlinkedIdentityField(view_name="gpd", lookup_field="group_id", lookup_url_kwarg="pk")
        url = tmp.get_url(objs[0], 'gpd', request, None)
        print '---url---= {0}'.format(url)
        # `HyperlinkedIdentityField` requires the request in the serializer context. Add `context={'request': request}` when instantiating the serializer.
        ser = ConsumerSerializer(instance=objs, many=True, context={'request': request})
        # 上面的 ser: 根据 many 的值会在 __new__ of BaseSerializer  会返回不同的对象
        # ser.data -> to_representation of Serializer -> attribute = field.get_attribute(instance) -> get_attribute normal function
        #                                                ret[field.field_name] = field.to_representation(attribute)
        ret = json.dumps(ser.data, ensure_ascii=False)
        return HttpResponse(ret)

# 这是为上面中的  HyperlinkedIdentityField 服务的
class ConsumerGroupDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsumerGroup
        fields = '__all__'
class ConsumerGroupDetailView(APIView):
    authentication_classes = []
    permission_classes = []
    throttle_classes = []
    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        group_obj = ConsumerGroup.objects.filter(pk=pk).first()
        ser = ConsumerGroupDetailSerializer(instance=group_obj, many=False)
        ret = json.dumps(ser.data,ensure_ascii=False)
        return HttpResponse(ret)


# Here 4: 这是讲 请求数据的验证的，又继承回了 serializers.ModelSerializer
class MyValidator(object):
    def __init__(self, suffix):
        self.suffix = suffix
    def __call__(self, value):
        if not value.startswith(self.suffix):
            message = 'Please start with {0}'.format(self.suffix)
            raise serializers.ValidationError(message)
class ConsumerGroupSerializer(serializers.Serializer):
    # 4_1 根据源码流程 to_internal_value of Serializer，
    # 可知会先执行字段中定义的 validators， 然后如果有 validate_xxx，再执行该方法
    title = serializers.CharField(validators=[MyValidator('Master'),])
    def validate_title(self, value):
        # 4_2 关于 validate_xxx 的返回值，
        # 如果参数 value 是合法的，则返回传入的参数；如果是非法的，则可以抛异常 serializers.ValidationError(message)
        # 因为在 to_internal_value of Serializer 会捕获异常
        return value + ' is Good'
class ConsumerGroupView(APIView):
    authentication_classes = []
    permission_classes = []
    throttle_classes = []

    def post(self, request, *args, **kwargs):
        ser = ConsumerGroupSerializer(data=request.data, many=False)
        # ser.is_valid ->  run_validation of Serializer -> value = self.to_internal_value(data) of Serializer
        if ser.is_valid():
            print 'ser.validated_data = {0}'.format(ser.validated_data)
        else:
            print 'ser.errors = {0}'.format(ser.errors)
        return HttpResponse('Test the validator with http post method')


# Here 5 测试分页的
class AdvRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'
class MyPageNumberPagination(PageNumberPagination):
    # 5_1 如果用原生的 PageNumberPagination， URL 中是不支持自定义 page_size 的
    page_size_query_param = 'page_size'
    max_page_size = 100
class PageNumberView(APIView):
    authentication_classes = []
    permission_classes = []
    throttle_classes = []
    def get(self, request, *args, **kwargs):
        print 'args = {0}, kwargs = {1}'.format(args, kwargs)
        # 在分页的源码中会看到类似这样的代码：猜测对于大量数据来说，应该也不慢
		# paginate_queryset -> self.page = paginator.page(page_number) -> return self._get_page(self.object_list[bottom:top], number, self)
        # 抽象成： tmp = Role.objects.all()[4:6] 其对应的 SQL 是
		# SELECT `app02_role`.`id`, `app02_role`.`role_name`, `app02_role`.`role_desc` FROM `app02_role` LIMIT 2 OFFSET 4;
        tmp = Role.objects.all()[4:6]
        print 'tmp = {0}'.format(tmp)
        # a. 获取所有数据
        queryset = Role.objects.all()

        # b. 创建分页对象
        # paginator = PageNumberPagination()
        paginator = MyPageNumberPagination()
        # c. 在数据库中获取分页的数据
        page = paginator.paginate_queryset(queryset=queryset,request=request,)

        # d.对数据进行序列化
        ser = AdvRoleSerializer(instance=page, many=True)
        return Response(ser.data)
        # return paginator.get_paginated_response(ser.data)

class MyLimitOffsetPagination(LimitOffsetPagination):
    # 5_2 如果用原生的 LimitOffsetPagination， 是不能对 max_limit 进行限制的，不能防止用户输入一个很大的值
    max_limit = 5
class LimitOffsetView(APIView):
    authentication_classes = []
    permission_classes = []
    throttle_classes = []

    def get(self, request, *args, **kwargs):
        queryset = Role.objects.all()
        paginator = LimitOffsetPagination()
        page = paginator.paginate_queryset(queryset=queryset, request=request, )
        ser = AdvRoleSerializer(instance=page, many=True)
        return paginator.get_paginated_response(ser.data)

class MyCursorPagination(CursorPagination):
    # 5_3 如果用原生的 CursorPagination， 默认是按照 -created 排序的，有可能自己的数据库表里没有该列
    ordering = 'id'
class CursorView(APIView):
    authentication_classes = []
    permission_classes = []
    throttle_classes = []

    def get(self, request, *args, **kwargs):
        queryset = Role.objects.all()
        paginator = MyCursorPagination()
        page = paginator.paginate_queryset(queryset=queryset, request=request, )
        ser = AdvRoleSerializer(instance=page, many=True)
        return paginator.get_paginated_response(ser.data)


# Here 6: 测试视图
class RoleViewSet(ModelViewSet):
    authentication_classes = []
    permission_classes = []
    throttle_classes = []

    queryset = Role.objects.all()
    serializer_class = AdvRoleSerializer
    pagination_class = PageNumberPagination


    @action(methods=['GET','POST'], detail=False)
    def test(self, request, *args, **kwargs):
        # Point 1:
        # 对于用 list_route 装饰器修改的函数: 在发送 requests.post 请求时如果 URL 不以斜杠 / 结尾，
        # 则请求 request.method 会被解析为 GET 也有可能会报错, 这可能取决于 Django 版本
        #
        # 如果 URL  http://x.x.x.x/TestModel/studentrest/business/?name=robert,则 request.query_params 会解析到内容
        # 如果 URL  http://x.x.x.x/autoregister/test/?name=robert,则 request.query_params 会解析到内容
        #
        # Point 2:
        # 我们知道，只要在浏览器输入 192.168.56.101:8080/autoregister/test/ 即可触发 test 视图方法
        # 但是如果业务需要这样的 URL:  192.168.56.101:8080/autoregister/1/test/  我们只需要用
        # @action(methods=['GET','POST'], detail=True) 装饰视图方法即可, 然后用 self.get_object() 来获取 url 中指定的对象
        # 这个灵感来自 http://mega.db.cbpmgt.com/entity/instance/16685/topo/
        print 'request.method = {0}'.format(request.method)
        print 'request.data = {0}'.format(request.data)
        print 'request.query_params = {0}'.format(request.query_params)
        print type(request.query_params)

        return Response('In the test of RoleViewSet')


# from rest_framework.versioning import URLPathVersioning
from rest_framework.generics import GenericAPIView
