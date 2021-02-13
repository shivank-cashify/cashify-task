from datetime import datetime
from django.db import models
from functools import wraps


class UrlTiming(models.Model):
    url = models.CharField(max_length=30, blank=True, null=True)
    req_time = models.DateTimeField(blank=True, null=True)
    resp_time = models.DateTimeField(blank=True, null=True)
    resp_duration = models.FloatField(blank=True,null=True)
    username = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'url_timing'

class Flag:
    pointer = 0
    url_exception_list = []  # Place here the rejection urls

class Url_Test:
    def __init__(self,url_requested):
        self.url_requested = url_requested
        urlobj = UrlTiming.objects.filter(url=self.url_requested)
        if urlobj:
            if self.url_requested not in Flag.url_exception_list:
                Flag.url_exception_list.append(self.url_requested)


def url_timing_decorator(func):
    @wraps(func)
    def inner(*args,**kwargs):
        Flag.pointer = 1
        return func(*args,**kwargs)
    return inner


class Url_Stats_Middleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request_dtime = datetime.now()
        response = self.get_response(request)
        response_dtime = datetime.now()
        duration = response_dtime - request_dtime
        url_now = request.build_absolute_uri()
        try:
            user_name = request.user
        except:
            pass
        if duration.total_seconds() > 1:
            raise Exception(' Sorry The Url Requested is taking too long to load..... Contact Admin ')
        Url_Test(url_now)
        if (Flag.pointer == 1) and (url_now not in Flag.url_exception_list):
            obj = UrlTiming(url=url_now, req_time=request_dtime, resp_time=response_dtime,
                        resp_duration=duration.total_seconds(), username=user_name)
            obj.save()
            Flag.pointer = 0
        return response



