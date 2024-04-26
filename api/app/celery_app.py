import os
import time
from celery import Celery

# Initialize Celery
celery = Celery(
    "worker",
    broker=os.getenv("CELERY_BROKER_URL"),
    backend=os.getenv("CELERY_RESULT_BACKEND"),
    broker_connection_retry_on_startup=True,
)


@celery.task()
def func1(arg):
    time.sleep(15)
    return 1
