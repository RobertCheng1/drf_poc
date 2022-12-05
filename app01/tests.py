# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
import requests
import json
import time, threading
import datetime
import mysql
import mysql.connector
# Create your tests here.
# ============REST api test======================
# url = 'http://127.0.0.1:8080/api/v1/auth/'
# url = 'http://127.0.0.1:8080/api/v1/order/'
# url = 'http://192.168.56.101:8082/api/v1/HelloCBV/'
# # res = requests.get(url)
# input_dict = {'name':'robert', 'age':22}
# input_dict = {'name':'robert', 'age':['abc', 'def']}
# res = requests.post(url, data=json.dumps(input_dict), headers={'Content-type': 'application/json'})
# print 'type(res.text) = {0}'.format(type(res.text))
# print 'res.status_code = {0}'.format(res.status_code)
# print 'res.text = {0}'.format(res.text)
# ============MySQL test======================
CONN_USER = 'root'
CONN_PASSWD = 'start01all'
host = '192.168.56.1'
port = 3306
db = 'robertdb'

def fetchAll(host, port, db, sql, user=CONN_USER, passwd=CONN_PASSWD):
    conn = mysql.connector.connect(host=host, user=user, passwd=passwd,
                                   db=db, port=port, charset='utf8', connection_timeout=10 * 60, buffered=True)
    cursor = conn.cursor()
    cursor.execute(sql)
    values_list = cursor.fetchall()
    cursor.close()
    conn.close()
    print 'values_list = {0}'.format(values_list)
    return values_list
binlog_format = "SELECT DATE_SUB(NOW(),INTERVAL 1 month)"
data = fetchAll(host=host, port=port, db=db, user=CONN_USER, passwd=CONN_PASSWD, sql=binlog_format)
raw_end_point_naive = data[0][0]
print raw_end_point_naive, type(raw_end_point_naive)
raw_end_point_naive = raw_end_point_naive.strftime("%Y-%m-%d %H:%M:%S")
print raw_end_point_naive
if isinstance(raw_end_point_naive, datetime.date):
    print 'fasf'


# =================misc test=====================
# def change_it():
#     url = 'http://192.168.56.101:8082/hello/'
#     # res = requests.post(url, data=input_dict, headers={'Content-type': 'application/json'})
#     res = requests.get(url)
#     print 'res.status_code = {0}'.format(res.status_code)
#
#
# def run_thread():
#     for i in range(100000):
#         change_it()
#
# t1 = threading.Thread(target=run_thread)
# t2 = threading.Thread(target=run_thread)
# t1.start()
# t2.start()
# t1.join()
# t2.join()
# print 'endddding'

from django.contrib.sessions.middleware import SessionMiddleware
from django.middleware.common import CommonMiddleware