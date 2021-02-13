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

class flag:
    pointer = 0
    url_exception_list = ['http://127.0.0.1:8000/']    # This URl inserted for testing purpose - can remove if required.

def url_timing_decorator(func):
    @wraps(func)
    def inner(*args,**kwargs):
        flag.pointer = 1
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
        if (flag.pointer == 1) and (url_now not in flag.url_exception_list):
            obj = UrlTiming(url=url_now, req_time=request_dtime, resp_time=response_dtime,
                        resp_duration=duration.total_seconds(), username=user_name)
            obj.save()
            flag.pointer = 0
        return response