import logging
from datetime import datetime
from django.core.mail import EmailMultiAlternatives
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.core.mail import mail_managers
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django_apscheduler import util
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution, DjangoJob


from news.models import Post,Category

logger = logging.getLogger(__name__)


def my_job():
    # получаем последний запуск нашего регламентного заданияя
    for e in DjangoJobExecution.objects.filter(job="my_job", status="Executed").values("run_time").order_by('-id')[:1]:
        time_last_execution = e["run_time"]

    # если это первый запуск-, тогда текущая дата.
    if not time_last_execution:
        time_last_execution = datetime.now()

    # находим список всех статей с последнего запуска
    post_list = Post.objects.filter(date__gte = time_last_execution )
    print(post_list)
    # находим список всех категорий статей
    categories = set(post_list.values_list('category__name', flat = True))
    print(categories)
    # находим подписчиков
    subscriber = set(Category.objects.filter(name__in = categories).values_list('subscriber__user__email', flat = True))
    print(subscriber)


    html_content = render_to_string(
        'daily_post.html',
        {
            'link': settings.SITE_URL,
            'posts': post_list,
        }
    )

    msg = EmailMultiAlternatives(
        subject= "Посты за неделю",
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to = subscriber,
    )

    msg.attach_alternative(html_content,'text/html')
    msg.send()


@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            trigger=CronTrigger(day_of_week="fri", hour="18", minute="00"),
            id="my_job",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

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