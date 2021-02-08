from datetime import datetime
from django.db import models


class UrlTiming(models.Model):
    url = models.CharField(max_length=30, blank=True, null=True)
    req_time = models.DateTimeField(blank=True, null=True)
    resp_time = models.DateTimeField(blank=True, null=True)
    resp_duration = models.FloatField(blank=True,null=True)
    username = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'url_timing'


class Stats_Middleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request_dtime = datetime.now()
        response = self.get_response(request)
        response_dtime = datetime.now()
        duration = response_dtime - request_dtime
        obj = UrlTiming(url = request.build_absolute_uri(),req_time = request_dtime,resp_time = response_dtime,resp_duration = duration.total_seconds(),username = request.user, )
        obj.save()
        return response





