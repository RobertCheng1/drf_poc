# -*- coding: utf-8 -*-
# Generated by Django 1.11.21 on 2019-07-21 12:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ConsumerGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='ConsumerInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_type', models.IntegerField(choices=[(1, '\u666e\u901a\u7528\u6237'), (2, 'VIP'), (3, 'SVIP')])),
                ('username', models.CharField(max_length=32, unique=True)),
                ('password', models.CharField(max_length=32)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app02.ConsumerGroup')),
            ],
        ),
        migrations.CreateModel(
            name='ConsumerToken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=64)),
                ('consumer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app02.ConsumerInfo')),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role_name', models.CharField(max_length=32)),
            ],
        ),
        migrations.AddField(
            model_name='consumerinfo',
            name='roles',
            field=models.ManyToManyField(to='app02.Role'),
        ),
    ]
