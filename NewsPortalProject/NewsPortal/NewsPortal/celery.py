import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPortal.settings')

app = Celery('NewsPortal')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

# ставим по расписанию постановку задания на отправку еженедельной рассылки
app.conf.beat_schedule = {
    'send_daily_email_newpost': {
        'task': 'news.tasks.daily_post_email',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
    },
}