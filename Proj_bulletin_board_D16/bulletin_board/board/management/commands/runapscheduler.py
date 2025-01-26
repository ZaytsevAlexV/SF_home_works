import logging

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.core.management.base import BaseCommand
from django_apscheduler import util
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from django.template.loader import render_to_string
from datetime import datetime, timedelta
from board.models import Post,Subscriber,Category
from accounts.models import ConfirmCode


logger = logging.getLogger(__name__)

def my_job():
    # если это первый запуск-, тогда текущая дата.
    time_last_execution = datetime.now()
    # получаем последний запуск нашего регламентного заданияя
    for e in DjangoJobExecution.objects.filter(job="my_job", status="Executed").values("run_time").order_by('-id')[:1]:
        time_last_execution = e["run_time"]

    # находим список всех статей с последнего запуска
    post_list = Post.objects.filter(create_date__gte = time_last_execution ) # для теста - Post.objects.all()
    #print(post_list)
    # находим список всех категорий статей
    categories = set(post_list.values_list('category__name', flat = True))
    # находим подписчиков
    subscriber = set(Category.objects.filter(name__in = categories).values_list('subscriber__users__email', flat = True))
    #print(subscriber)


    html_content = render_to_string(
        'daily_post.html',
        {
            'link': settings.SITE_URL,
            'posts': post_list,
        }
    )

    msg = EmailMultiAlternatives(
        subject= "Объявления за неделю",
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to = subscriber,
    )

    msg.attach_alternative(html_content,'text/html')
    msg.send()

def my_job_clean_code():
    less_min= datetime.now() - timedelta(minutes=5)
    codeToDel = ConfirmCode.objects.filter(create_date__lt= less_min).delete()

@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    """
    This job deletes APScheduler job execution entries older than `max_age`
    from the database.
    It helps to prevent the database from filling up with old historical
    records that are no longer useful.

    :param max_age: The maximum length of time to retain historical
                    job execution records. Defaults to 7 days.
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            trigger=CronTrigger(day_of_week="mon", hour="12", minute="00"), # направляю рассылку каждый понедельник в полдень # для теста trigger=CronTrigger(second="*/10"),
            id="my_job",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        #Подключаю тут новый джоб для того чтобы чистить коды.

        scheduler.add_job(
            my_job_clean_code,
            trigger=CronTrigger(minute="*/1"),  # каждую минуту
            id="my_job_clean_code",  #
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job_clean_code'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'delete_old_job_executions'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")