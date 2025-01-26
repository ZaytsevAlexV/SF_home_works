from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

#Объявление(Post)
class Post(models.Model):
    title = models.CharField(unique=True, max_length=255)
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    category = models.ForeignKey('Category', on_delete=models.DO_NOTHING)
    text_post = models.TextField()
    media = models.FileField(null=True)
    status = models.CharField(null=True, max_length=2)  # (A-активное, NA - не активоное)
    create_date = models.DateTimeField(null=True, auto_now_add=True)
    update_date = models.DateTimeField(null=True)

    def __str__(self):
        return f'{self.title}: {self.text_post[:20]}'
    def get_absolute_url(self):
        return reverse('post', args=[str(self.id)])



#Категория (Category)
class Category(models.Model):
    name = models.CharField(unique=True, max_length=40)

    def __str__(self):
        return f'{self.name}'

#Подписки (Subscriber)
class Subscriber(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    users = models.ForeignKey(User, on_delete=models.CASCADE)

#Отклик (RestponsToPost)
class RestponsToPost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    text = models.TextField()
    status = models.CharField(max_length=2)# (n -новый, ac - принят, de - отклонен)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(null=True)



