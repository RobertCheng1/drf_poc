# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse
from models import DegreeCourse,NormalCourse, PricePolicy

# Create your views here.
def poc_contenttype(request):
    # 需求1: 为学位课"Python Full Stack" 添加一个价格策略：一个月 9 元
    # 直观的想法：怎么获取  content_type  和 object_id 的值？
    # obj = DegreeCourse.objects.filter(title = 'Python Full Stack').first()
    # cobj = ContentType.objects.filter(model='degreecourse').first()
    # PricePolicy.objects.create(price=9, peroid=30, content_type=cobj, object_id=obj.id)
    # PricePolicy.objects.create(price=9, peroid=30, content_type_id=cobj.id, object_id=obj.id)
    #
    # 而在用了 Content type 这个 app 后，好多工作 app 帮你做了
    # 在创建 PricePolicy 对象的时候，并不用显示的给 content_type  object_id 赋值，只需给 content_object 赋值即可
    # 猜测 django.contrib.contenttypes 可能会根据 degree_obj 所属的model，从 django_content_type 表里找到该 model 的记录
    # 从而获取该记录在 django_content_type 中的 id, 然后为 PricePolicy 中的列 content_type 赋值， 当然还有列 object_id
    # degree_obj = DegreeCourse.objects.filter(title='Django Full Stack').first()
    # PricePolicy.objects.create(price=9, peroid=30, content_object=degree_obj)
    #
    # 需求2: 为普通课"Django Rest framwork"添加一个价格策略: 一个月 6 元
    # normal_obj = NormalCourse.objects.filter(title='Django Rest framwork').first()
    # PricePolicy.objects.create(price=6, peroid=30, content_object=normal_obj)
    #
    # 需求3: 根据课程 ID 得到所有的价格策略
    degree_obj = DegreeCourse.objects.filter(id=1).first()
    polices = degree_obj.price_policy_list.all()

    print 'polices = {0}'.format(polices)

    # # So cool:
    # pp = PricePolicy.objects.filter(id = 1).first()
    # # pp.content_object = DegreeCourse object
    # print 'pp.content_object = {0}'.format(pp.content_object)
    return HttpResponse('This in the poc_contenttype of app03')


