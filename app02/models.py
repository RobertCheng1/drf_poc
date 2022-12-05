# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.
class ConsumerGroup(models.Model):
    title = models.CharField(max_length=32)


class ConsumerInfo(models.Model):
    uset_type_choices = (
        (1, '普通用户'),
        (2, 'VIP'),
        (3, 'SVIP')
    )
    user_type = models.IntegerField(choices=uset_type_choices)
    group = models.ForeignKey("ConsumerGroup")

    username = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=32)

    roles = models.ManyToManyField('Role')


class ConsumerToken(models.Model):
    consumer = models.OneToOneField(to='ConsumerInfo')
    token = models.CharField(max_length=64)


class Role(models.Model):
    # 这个 model 可以理解为 Consumer 喜欢的角色，不要理解为 consumer 的分类
    role_name = models.CharField(max_length=32)
    role_desc = models.CharField(max_length=32)
