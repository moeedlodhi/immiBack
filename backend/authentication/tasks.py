from django.conf import settings
from django.db import transaction
from celery import shared_task
from time import sleep
import time





@shared_task
def long_running_task(data=None):
    with transaction.atomic():
        try:
            print(data)
            print('starting')
            time.sleep(5)
            print('hellllooo')
        except Exception as e:
            raise Exception(str(e))
