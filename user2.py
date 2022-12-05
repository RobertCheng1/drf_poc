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

def change_it():
    url = 'http://192.168.56.101:8082/hello1/'
    # res = requests.post(url, data=input_dict, headers={'Content-type': 'application/json'})
    res = requests.get(url)
    print 'res.status_code = {0}'.format(res.status_code)


for i in range(300):
    change_it()


