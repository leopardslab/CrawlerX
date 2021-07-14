from celery import shared_task


@shared_task(bind=True)
def schedule_cron_job(self, **kwargs):
    print(kwargs)
    print("Hello World")