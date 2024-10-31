from datetime import datetime, timedelta
from celery import shared_task

from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import Post, Category, Subscriber, PostCategory
from django.conf import settings

@shared_task
def new_post_email(oid):
    post = Post.objects.get(pk = oid)
    category = Post.objects.filter(pk = oid).values_list("category__id", flat= True)

    emails = User.objects.filter(
                                subscriber__category=category[0]
                                ).values_list('email', flat=True)

    subject = f'[celery] Новый пост в категории {post.category}'

    text_content = (
        f'Пост [celery] : {post.title}\n'
        f' {post.preview()}\n\n'
        f'Ссылка на post[celery] : http://127.0.0.1:8000{post.get_absolute_url()}'
    )
    html_content = (
        f'Пост[celery] : {post.title}<br>'
        f' {post.preview()}<br><br>'
        f'<a href="http://127.0.0.1:8000{post.get_absolute_url()}">'
        f'Ссылка на пост [celery] </a>'
    )
    for email in emails:
        msg = EmailMultiAlternatives(subject, text_content, None, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

@shared_task
def daily_post_email():
    post_list = Post.objects.filter(date__gte=datetime.now() - timedelta(weeks = 1))
    #print(post_list)
    # находим список всех категорий статей
    categories = set(post_list.values_list('category__name', flat=True))
    #print(categories)
    # находим подписчиков
    subscriber = set(Category.objects.filter(name__in=categories).values_list('subscriber__user__email', flat=True))
    #print(subscriber)

    html_content = render_to_string(
        'daily_post.html',
        {
            'link': settings.SITE_URL,
            'posts': post_list,
        }
    )

    msg = EmailMultiAlternatives(
        subject="[celery] Daily new posts ",
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscriber,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()


