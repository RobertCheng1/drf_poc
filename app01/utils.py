# -*- coding: utf-8 -*-
from __future__ import unicode_literals

'''
# The case code is to test the basic authentication And the the code is COPIED from BasicAuthentication
import base64
import binascii
from django.contrib.auth import authenticate, get_user_model
from django.middleware.csrf import CsrfViewMiddleware
from django.utils.six import text_type
from django.utils.translation import ugettext_lazy as _
from rest_framework import HTTP_HEADER_ENCODING, exceptions
def get_authorization_header(request):
    # Return request's 'Authorization:' header, as a bytestring.
    # Hide some test client ickyness where the header can be unicode.
    auth = request.META.get('HTTP_AUTHORIZATION', b'')
    if isinstance(auth, text_type):
        # Work around django test client oddness
        auth = auth.encode(HTTP_HEADER_ENCODING)
    return auth

class MyAuthentication(BaseAuthentication):
    # HTTP Basic authentication against username/password.
    www_authenticate_realm = 'api'
    def authenticate(self, request):
        # Returns a `User` if a correct username and password have been supplied
        # using HTTP Basic authentication.  Otherwise returns `None`.
        auth = get_authorization_header(request).split()
        # if not auth or auth[0].lower() != b'basic':
        #     return None
        if not auth:
            msg = _('Invalid basic header. No credentials provided.')
            raise exceptions.AuthenticationFailed(msg)
        try:
            auth_parts = base64.b64decode(auth[1]).decode(HTTP_HEADER_ENCODING).partition(':')
        except (TypeError, UnicodeDecodeError, binascii.Error):
            msg = _('Invalid basic header. Credentials not correctly base64 encoded.')
            raise exceptions.AuthenticationFailed(msg)
        userid, password = auth_parts[0], auth_parts[2]
        return self.authenticate_credentials(userid, password, request)

    def authenticate_credentials(self, userid, password, request=None):
        # Authenticate the userid and password against username and password
        # with optional request for context.
        credentials = {
            get_user_model().USERNAME_FIELD: userid,
            'password': password
        }
        user = authenticate(request=request, **credentials)
        if user is None:
            raise exceptions.AuthenticationFailed(_('Invalid username/password.'))
        if not user.is_active:
            raise exceptions.AuthenticationFailed(_('User inactive or deleted.'))
        return (user, None)

    def authenticate_header(self, request):
        return 'Basic realm="%s"' % self.www_authenticate_realm
'''

from rest_framework.authentication import BaseAuthentication
from rest_framework.permissions import BasePermission
from rest_framework.throttling import BaseThrottle
from rest_framework.throttling import SimpleRateThrottle
from rest_framework.versioning import BaseVersioning,QueryParameterVersioning, URLPathVersioning
from rest_framework import exceptions


from models import UserToken
import time
import hashlib


def my_md5(username):
    ctime = str(time.time())
    m = hashlib.md5(username)
    m.update(ctime)
    return m.hexdigest()

# 1. 认证类
class MyAllowAnyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        pass
# Notes: when define class like:  class MyAuthentication(object):
# 其方法 authenticate 下面为什么有波浪线提示: method authenticate may be static,
# 解决方案: # noinspection PyMethodMayBeStatic
# https://stackoverflow.com/questions/23554872/why-does-pycharm-propose-to-change-method-to-static
# class MyAuthentication(object):
class MyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        print '---In the MyAuthentication: request.method = {0}---'.format(request.method)
        token = request._request.GET.get('token')
        print 'token = {0}'.format(token)
        toke_obj = UserToken.objects.filter(token=token).first()
        if not toke_obj:
            raise exceptions.AuthenticationFailed('user failedd')
        return toke_obj.user, toke_obj

    # The function authenticate_header was defined in the BaseAuthentication
    # def authenticate_header(self, request):
    #     pass

# 2. 权限类
class MyPermission(BasePermission):
    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        if request.user.user_type >= 1:
            return True
        else:
            return False
    # The function has_object_permission was defined in the BasePermission and will be invoked by the CBV inherited from
    # ModelViewSet -> GenericViewSet -> GenericAPIView -> get_object -> check_object_permissions, 这是后来讲视图时补充的
    # def has_object_permission(self, request, view, obj):
    #     return True

class VIPPermission(BasePermission):
    message = 'You should be VIP,hiahia'
    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        if request.user.user_type >= 2:
            return True
        else:
            return False
    # The function has_object_permission was defined in the BasePermission and will be invoked by the CBV inherited from
    # ModelViewSet -> GenericViewSet -> GenericAPIView -> get_object -> check_object_permissions, 这是后来讲视图时补充的
    # def has_object_permission(self, request, view, obj):
    #     return True
# 3. 节流类
"""
# The code is to learn the process of the throttle of DjangoRestFramwork
VISIT_RECORD = dict()
FREQUENCE_PER_SECOND = 3
class VisitThrottle(BaseThrottle):
    def __init__(self):
        self.history = None
    def allow_request(self, request, view):
        # 比如一分钟允许访问 3 次
        remote_addr = request.META.get('REMOTE_ADDR')
        ctime = time.time()
        if remote_addr not in VISIT_RECORD:
            VISIT_RECORD[remote_addr] = [ctime,]
            return True
        history = VISIT_RECORD.get(remote_addr)
        self.history = history
        while history and history[-1] < ctime - 60:
            history.pop()
        if len(history) < FREQUENCE_PER_SECOND:
            history.insert(0, ctime)
            return True
        return False

    def wait(self):
        ctime = time.time()
        return 60 - (ctime - self.history[-1])
"""
# Actually after you know about the details of throttle and the built-in throttle class,You may want to inherit it
# If you inherit built-in throttle class, You must provide some attribute and overwrite some methods at the same time
# This is to give you the chance to customize the throttle configuration based on your business
# For example, If you inherit from SimpleRateThrottle: you should provide `scope` and overwrite `get_cache_key`
#
# About ScopedRateThrottle:  Any view that has the `throttle_scope` property set will bethrottled.
# 这个可以用来做：不同的视图用不同的访问频率配置，
# 只需要在VIEW 类里定义 throttle_scope，同时在配置文件的 DEFAULT_THROTTLE_RATES 中定义相应的 rate 即可
# 当然也可以定义多个限流类(VisitThrottle, VIPVisitThrottle)，老师是推荐定义多个限流类，我觉得未必吧
# https://www.bilibili.com/video/av28871471/?p=27 最后几分钟
class VisitThrottle(SimpleRateThrottle):
    scope = 'general_rate'
    def get_cache_key(self, request, view):
        return self.get_ident(request)
class VIPVisitThrottle(SimpleRateThrottle):
    scope = 'vip_rate'
    def get_cache_key(self, request, view):
        return self.get_ident(request)


# 4. 版本类
"""
# The code is to learn the process of the versioning of DjangoRestFramwork
class MyVersioning(BaseVersioning):
    def determine_version(self, request, *args, **kwargs):
        version = request.query_params.get('version')
        return version
"""
# Actually after you know about the details of versioning and the built-in versioning class, You may want to inherit it
class MyVersioning(QueryParameterVersioning):
    pass

# 解析器
# 参考配置文件 settings.py


