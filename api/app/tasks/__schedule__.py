from celery.schedules import crontab


BEAT_SCHEDULE = {
    # "check-password-expiration": {
    #     "task": "app.tasks.email.check_password_expired",
    #     "schedule": crontab(minute="*/1"),
    # }
}
