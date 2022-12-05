# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation

# Create your models here.
# Please refer to https://blog.csdn.net/aaronthon/article/details/81714496
# 我们知道某张表的列 ForeignKey  和 ManyToManyField 只能关联到一张表，这是有一定局限性的，
# 如果业务要求某张表需要关联多张表，怎么操作?
# 当然可以用多个列来关联多张表，这有的浪费空间。同时随着业务发展如果又需要新关联别的表，则就要再加一列了。
# 这样表结构就会频繁的被修改，如果数据量大的话是很被动的。
# 发散下思路：
# 只增加两列：一个是关联的表名、一个是其中的 id， 这样好像就规避了上述频繁修改表结构的问题。
# 不过如果被关联的表名发生变更的话，则需要修改所有 外键到变更表 的记录，这也不是很完美。
# 后来有想了下：
# 再创建以一个表，用来记录项目中的所有表(all_table)，因为有了all_table 之后，记录关联的就是 all_table 中的 id
# 这样就解决了被关联的表名发生变更，需要修改所有 外键到变更表 的记录。
# 其实这就是 django 的 content type 的思路
#
class DegreeCourse(models.Model):
    title = models.CharField(max_length=32)
    # Best practice: Please note the default para object_id_field and content_type_field of class GenericRelation
    # 仅仅是帮助你做反向查找，根据课程 ID 得到所有的价格策略， 并不在数据库表中生成这一列
    # price_policy_list = GenericRelation('PricePolicy')
    #
    # The following is also workable:
    price_policy_list = GenericRelation('PricePolicy', object_id_field='object_idd', content_type_field='content_typee')

class NormalCourse(models.Model):
    title = models.CharField(max_length=32)
    # 仅仅是帮助你做反向查找，根据课程 ID 得到所有的价格策略， 并不在数据库表中生成这一列
    price_policy_list = GenericRelation('PricePolicy')

class PricePolicy(models.Model):
    price = models.IntegerField()
    peroid = models.IntegerField()

    # Best practice: Please note the column name, and the para name of class GenericForeignKey is very GOOD
    # content_type = models.ForeignKey(ContentType, verbose_name='关联的表名称')
    # object_id = models.IntegerField(verbose_name='关联的表中的数据行的ID')
    # # 仅仅是帮助你快速 content type 的相关操作，并不在数据库表中生成这一列
    # content_object = GenericForeignKey('content_type', 'object_id')
    #
    # The following is also workable:
    content_typee = models.ForeignKey(ContentType, verbose_name='关联的表名称')
    object_idd = models.IntegerField(verbose_name='关联的表中的数据行的ID')
    content_object = GenericForeignKey('content_typee', 'object_idd')

