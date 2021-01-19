from django.db import models


class Deal(models.Model):
    customer = models.CharField(max_length=250)
    item = models.CharField(max_length=250)
    total = models.IntegerField()
    quantity = models.IntegerField()
    date = models.DateTimeField(max_length=250)
