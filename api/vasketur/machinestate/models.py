from django.db import models


class History(models.Model):
    machine_type = models.CharField(max_length=20)
    machine_num = models.IntegerField()
    machine_status = models.CharField(max_length=20)
    machine_time_value = models.CharField(max_length=10)
    timestamp = models.DateTimeField(auto_now_add=True)
