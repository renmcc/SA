#!/usr/bin/env python
#coding:utf8
#__time__:2019/8/913:47
#__author__:"ren_mcc"
from rest_framework.pagination import PageNumberPagination

class Pagination(PageNumberPagination):
    def get_page_size(self, request):
        try:
            page_size = int(request.query_params.get("page_size", -1))
            if page_size < 0:
                return self.page_size
            return page_size
        except:
            pass
        return self.page_size


class DefaultPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    page_query_param = "page"
    max_page_size = 100