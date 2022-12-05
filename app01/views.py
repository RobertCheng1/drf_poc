# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.db import transaction
from rest_framework.views import APIView
from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.parsers import JSONParser,FormParser,MultiPartParser
import logging
import json
import time

from models import UserInfo
from models import UserToken
from utils import my_md5
from utils import MyAuthentication
from utils import VIPPermission
from utils import VisitThrottle
from utils import VIPVisitThrottle
from utils import MyVersioning
import random
import mysql.connector
import multiprocessing

GLOBAL_VAR = 6
logger = logging.getLogger('drf_poc')


def hang():
    print 'In the hang'
    time.sleep(10)
    print 'End In the hang'

# Create your views here.
def misctest(request):
    logger.info("In the misctest")
    # conn = mysql.connector.connect(host='192.168.56.1', port=3306, db='robertdb', user='root', passwd='start01all', buffered=True)
    # cursor = conn.cursor()
    # # cursor.execute('select * from student')
    # # cursor.execute("select COLUMN_NAME, COLUMN_KEY, EXTRA, COLUMN_COMMENT from information_schema.columns where TABLE_SCHEMA='robertdb' and TABLE_NAME='student'")
    # # cursor.execute("select *  from information_schema.columns where TABLE_SCHEMA='robertdb' and TABLE_NAME='student'")
    # cursor.execute("select id from student limit 2")
    # data = cursor.fetchall()
    # conn.commit()
    # cursor.close()
    # conn.close()
    tmp = multiprocessing.Process(target=hang)
    tmp.start()
    return JsonResponse({'name':22})
    return HttpResponse('In the get of the misctest')

def hello(request):
    """
    主要是为了确定是否需要给全局变量 GLOBAL_VAR 加锁
    对 GLOBAL_VAR 只加不减, 看看它的值会不会累计或者再增加一个hello1接口试试
    """
    print 'In hello type(request) = {0},type(request.POST) = {0}'.format(type(request), request.POST)
    from django.core.handlers.wsgi import WSGIRequest
    # tmp = random.randint(1, 10)
    tmp = 1
    # https://www.cnblogs.com/summer-cool/p/3884595.html
    # 因为函数中也可定义同名的变量，这样局部的变量就覆盖了全局的变量，
    # 要想改变全局变量的值，需要在函数中 global GLOBAL_VAR 说明 GLOBAL_VAR 是全局变量
    global GLOBAL_VAR
    logger.info('GLOBAL_VAR = {0}, tmp = {1}'.format(GLOBAL_VAR, tmp))
    GLOBAL_VAR = GLOBAL_VAR + tmp
    # GLOBAL_VAR = GLOBAL_VAR - tmp
    logger.info('GLOBAL_VAR is = {0}'.format(GLOBAL_VAR))
    return HttpResponse('hello')
def hello1(request):
    # tmp = random.randint(1, 10)
    tmp = 1
    global GLOBAL_VAR
    logger.info('In hello1 GLOBAL_VAR = {0}, tmp = {1}'.format(GLOBAL_VAR, tmp))
    GLOBAL_VAR = GLOBAL_VAR + tmp
    # GLOBAL_VAR = GLOBAL_VAR - tmp
    logger.info('In hello1 GLOBAL_VAR is = {0}'.format(GLOBAL_VAR))
    return HttpResponse('hello')

def signal_poc(request):
    from signal_poc import pizza_done
    # pizza_done.send(sender='seven', toppings=123, size=456)
    pizza_done.send(sender=signal_poc, toppings=123, size=456)
    return HttpResponse('signal_poc')

def concurrence(request):
    print 'In the concurrence'
    # 为了验证悲观锁 select_for_update 对锁的持有情况：
    # 1. 在浏览器里访问相应的 URL，触发视图函数执行，视图函数仅仅让 user_type 增加 1
    # 2. 快速打开一个mysql client, 连接同一个数据库，看到 id = 4 的记录的 user_type 原始值是 1
    # mysql> select * from app01_userinfo where id = 4;
    # +----+-----------+---------------+----------+
    # | id | user_type | username      | password |
    # +----+-----------+---------------+----------+
    # |  4 |         1 | gwwww         | 3252     |
    # +----+-----------+---------------+----------+
    # 1 row in set (0.00 sec)
    # mysql>
    #
    # 3. 然后再快速执行 update app01_userinfo set user_type = user_type + 1 where id = 4 即视图函数处理的那条记录
    # 可以看到这条普通的 update SQL 居然执行了 4.54 second，且最后 user_type 的值变成了 3 ：
    # 正好和该视图函数中 sleep 时间吻合，完美验证了 select_for_update 对锁的持有，其他请求需要等待锁释放。
    #
    # mysql> update app01_userinfo set user_type = user_type + 1 where id = 4;
    # Query OK, 1 row affected (4.54 sec)
    # Rows matched: 1  Changed: 1  Warnings: 0
    # mysql>
    # mysql> select * from app01_userinfo where id = 4;
    # +----+-----------+---------------+----------+
    # | id | user_type | username      | password |
    # +----+-----------+---------------+----------+
    # |  4 |         3 | gwwww         | 3252     |
    # +----+-----------+---------------+----------+
    # 1 row in set (0.00 sec)
    # mysql>
    with transaction.atomic():
        db = UserInfo.objects.select_for_update().get(id=4)
        print 'db = {0}'.format(db)
        # In production code: maybe you should update some properties of the db object
        db.user_type = db.user_type + 1
        db.save()
        time.sleep(5)
        print 'after sleep'
    # 为了验证乐观锁的使用情况：使用乐观锁时必须设置数据库的隔离级别是Read Committed(可以读到其他线程已提交的数据)。
    # 如果隔离级别是Repeatable Read(可重复读，读到的数据都是开启事务时刻的数据，即使其他线程提交更新数据，
    # 该线程读取的数据也是之前读到的数据)，乐观锁如果第一次尝试失败,那么不管尝试多少次都会失败。
    # (Mysql数据库的默认隔离级别是Repeatable Read，需要修改成Read Committed)。
    # 乐观锁其实并不是锁。通过SQL的where子句中的条件是否满足来判断是否满足更新条件来更新数据库，
    # 通过受影响行数判断是否更新成功，如果更新失败可以再次进行尝试，如果多次尝试失败就返回更新失败的结果。
    # s1 = transaction.savepoint()
    # print 'begin: {0}'.format(time.time())
    # retry_time = 1
    # for i in range(retry_time):
    #     db = UserInfo.objects.filter(id=4).first()
    #     old_balance = int(db.password)
    #     new_balance = old_balance - 1
    #     # 用 password 列来模拟余额, 在 sleep 期间把通过 mysql client 修改数据库的值
    #     time.sleep(10)
    #     res = UserInfo.objects.filter(id=4, password=str(old_balance)).update(password=str(new_balance))
    #     if res == 0:
    #         if i == retry_time - 1:
    #             print 'update failed: {0}'.format(time.time())
    #             transaction.savepoint_rollback(s1)
    #             return HttpResponse('update failed')
    #         continue
    #     else:
    #         print 'update successfully: {0}'.format(time.time())
    #         return HttpResponse('update successfully')
    return HttpResponse('concurrence test')


class HelloCBVView(APIView):
    """
    Just for test how to get the data wrapped in the request
    """
    authentication_classes = []
    permission_classes = []
    throttle_classes = []
    def get(self, request, *args, **kwargs):
        print '------------In the get of  helloCBVView ------'
        print 'In helloCBVView type(request) = {0}'.format(type(request))
        from rest_framework.request import Request
        print "In helloCBVView，request.META['CONTENT_TYPE'] = {0}".format(request.META['CONTENT_TYPE'])

        print 'request.GET = {0}'.format(request.GET)
        print 'request.query_params = {0}'.format(request.query_params)
        print 'request.POST = {0}'.format(request.POST)
        print 'request.data = {0}'.format(request.data)
        get_data = request.GET
        # get_data = request.query_params
        for key, value in get_data.items():
            print 'key = {0}, type(key) = {1}'.format(key, type(key))
            print 'value = {0}, type(value) = {1}'.format(value, type(value))
        return HttpResponse('helloCBVView View: order get')
    def post(self, request, *args, **kwargs):
        print '------------In the post of  helloCBVView ------'
        print "In helloCBVView，request.META['CONTENT_TYPE'] = {0}".format(request.META['CONTENT_TYPE'])
        print 'request.GET = {0}'.format(request.GET)
        print 'request.query_params = {0}'.format(request.query_params)
        print 'request.POST = {0}, type(request.POST) = {1}'.format(request.POST, type(request.POST))
        print 'request.data = {0}, type(request.data) = {1}'.format(request.data, type(request.data))
        # get_data = request.POST
        get_data = request.data

        data = request.data
        data.pop('name')
        print 'data ==========={0}'.format(data)

        for key, value in get_data.items():
            print 'key = {0}, type(key) = {1}'.format(key, type(key))
            print 'value = {0}, type(value) = {1}'.format(value, type(value))
        # return HttpResponse('helloCBVView View: order post')
        # How to response:
        res = {'star':'Jordan', 'score':32}
        # res = [True, 'Good Thing!']
        return Response(res)
        return HttpResponse(json.dumps(res))

class AuthView(APIView):
    # 这是登录请求，不用认证就可以访问,
    # 请求body 带上: 用户名和密码; 返回给前端 token
    authentication_classes = []
    permission_classes = []
    # The next can be commented because it is equivalent to the default configuration
    throttle_classes = [VisitThrottle,]

    def get(self, request, *args, **kwargs):
        print request.query_params.get('age')
        print type(request.query_params.get('age'))
        print 'request.user = {0}'.format(request.user)
        print 'request.user.id = {0}'.format(request.user.id)
        print 'request._authenticator = {0}'.format(request._authenticator)
        print id(request.user), id(request._request.user)
        return Response('Please use the POST request to get the token')

    def post(self, request, *args, **kwargs):
        ret = {'code': 1000, 'msg': None}
        try:
            print 'request._request.POST = {0}'.format(request._request.POST)
            print 'request.data = {0}'.format(request.data)
            username = request._request.POST.get('username')
            password = request._request.POST.get('password')
            print 'username = {0}'.format(username)

            obj = UserInfo.objects.filter(username=username, password=password).first()
            if not obj:
                ret['code'] = 1001
                ret['msg'] = '用户名或密码错误'
            # 为登录用户创建 token
            token = my_md5(username)
            #  存在就更新，不存在就创建
            UserToken.objects.update_or_create(user=obj, defaults={'token': token})
            ret['token'] = token
        except Exception as e:
            ret['code'] = 1002
            ret['msg'] = '请求异常'
            print e
        return JsonResponse(ret)


class OrderView(APIView):
    def get(self, request, *args, **kwargs):
        return HttpResponse('General View: order get')


class BonusView(APIView):
    # 配置文件里有定义 REST_FRAMEWORK -> DEFAULT_PERMISSION_CLASSES -> MyPermission
    # 如果某视图不想用配置文件的默认权限类，可以自定义权限类即定义 permission_classes 并赋新值
    permission_classes = [VIPPermission,]
    throttle_classes = [VIPVisitThrottle,]
    def get(self, request, *args, **kwargs):
        return HttpResponse('VIP View: bonuse get')


# 为了研究版本
class EvolView(APIView):
    versioning_class = MyVersioning
    def get(self, request, *args, **kwargs):
        # http://192.168.56.101:8082/api/EvolView/?version=v2&token=2c9e3cf41cd8e44c830b5bd736ea0a3d
        print 'In EvolView kwargs = {0}'.format(kwargs)
        print 'version = {0}'.format(request.version)
        return HttpResponse('evolView: get')
class EvolEnView(APIView):
    def get(self, request, *args, **kwargs):
        # 视图函数的 kwargs 是 URL 中正则匹配的信息：21min18sec of https://www.bilibili.com/video/av28871471?t=918&p=33
        # http://192.168.56.101:8082/api/v2/EvolEnView/?token=2c9e3cf41cd8e44c830b5bd736ea0a3d
        print 'In EvolEnView kwargs = {0}'.format(kwargs)
        print 'version = {0}'.format(request.version)
        return HttpResponse('evolEnView: get')


class ParserView(APIView):
    parser_classes = [JSONParser, FormParser]
    def post(self, request, *args, **kwargs):
        # http://192.168.56.101:8082/api/ParserView/?version=v123&token=2c9e3cf41cd8e44c830b5bd736ea0a3d
        print 'In ParserView kwargs = {0}'.format(kwargs)
        print 'request.data = {0}'.format(request.data)
        # request.data 会触发下面 5 件事：
        # 1. 获取请求头
        # 2. 获取请求体
        # 3. 根据请求头 和 parser_classes 中的解析器类支持的 media_type 比较，选出合适的解析器
        # 4. 选出的解析器调用自己 parse 方法解析请求体
        # 5. 把解析结果赋值给 request.data
        return HttpResponse('ParserView: post')


