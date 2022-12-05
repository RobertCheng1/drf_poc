#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.utils.deprecation import MiddlewareMixin
class RobertMiddleware(MiddlewareMixin):
    def process_request(self, request):
        print 'In the process_request of RobertMiddleware--------'
        # If you return HttpResponse directly in the process_request, The real view func from views.py will NOT executed
        # The output of middle ware is like:
        # In the process_request of RobertMiddleware--------
        # In the process_response of RobertMiddleware-------
        # return HttpResponse('Return from the process_request of RobertMiddleware')


    # def process_view(self, request, callback, callback_args, callback_kwargs):
    def process_view(self, request, view_func, view_func_args, view_func_kwargs):
        print 'In the process_view of RobertMiddleware-------'
    def process_response(self,request, response):
        print 'In the process_response of RobertMiddleware-------'
        return response