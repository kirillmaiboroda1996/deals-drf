from django.db import models


class Deal(models.Model):
    customer = models.CharField(max_length=250)
    item = models.CharField(max_length=250)
    total = models.CharField(max_length=50)
    quantity = models.IntegerField()
    date = models.DateTimeField()
