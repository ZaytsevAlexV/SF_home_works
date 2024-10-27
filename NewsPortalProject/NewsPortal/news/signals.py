from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from .models import PostCategory, Subscriber


@receiver(m2m_changed, sender=PostCategory)
def post_created(instance, **kwargs):
    sub_email = []
    if kwargs['action'] == 'post_add':
        categories = instance.category.all()
        for cat in categories:
            email = User.objects.filter(subscriber__category = cat).values('email')
            sub_email += email

        subject = f'Новый пост в категории {instance.category}'

        text_content = (
            f'Пост: {instance.title}\n'
            f'Ссылка на post: http://127.0.0.1:8000{instance.get_absolute_url()}'
        )
        html_content = (
            f'Пост: {instance.title}<br>'
            f'<a href="http://127.0.0.1:8000{instance.get_absolute_url()}">'
            f'Ссылка на пост</a>'
        )
        for email in sub_email:
            msg = EmailMultiAlternatives(subject, text_content, None, [email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()