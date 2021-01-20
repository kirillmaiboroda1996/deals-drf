#! /usr/bin/env python
import os
import sys

from .models import Deal
sys.path.append(os.path.realpath('.'))

from deals_api.celery import app


@app.task
def import_from_csv(json_data):
    """The function creates objects of Deal model from given DictReader obj."""
    for row in json_data:
        Deal.objects.create(**row)
