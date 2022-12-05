# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
import requests
import json
import time, threading

# Create your tests here.
# url = 'http://127.0.0.1:8080/api/v1/auth/'
# url = 'http://127.0.0.1:8080/api/v1/order/'
# # res = requests.post(url, data=input_dict, headers={'Content-type': 'application/json'})
# res = requests.get(url)
# print 'type(res.text) = {0}'.format(type(res.text))
# print 'res.status_code = {0}'.format(res.status_code)
# print 'res.text = {0}'.format(res.text)
#==========

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

#=========================
# url = "http://192.168.56.101:8082/hello/"
# input_dict = {'name':'Robert', 'age':22}
# res = requests.get(url, params=input_dict)
# print res.text


url = "http://192.168.56.101:8082/api/v1/helloCBV/"
input_dict = {'name':'Robert', 'age':22}
res = requests.get(url, params=input_dict)
print res.text



url = "http://192.168.56.101:8082/api/v1/helloCBV/"
input_dict = {'name':'Robert', 'age':223}
# res = requests.post(url, data=json.dumps(input_dict))
# res = requests.post(url, data=input_dict)
# res = requests.post(url, json=input_dict)
res = requests.post(url, data=json.dumps(input_dict), headers={'Content-type': 'application/json'})
print res.text
data = json.loads(res.text)
print data.get('score')
print type(data.get('score'))