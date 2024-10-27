from django.db import models
from django.contrib.auth import models as auth_models
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


# Модель Author
class Author(models.Model):
    author = models.OneToOneField(auth_models.User, on_delete=models.DO_NOTHING)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        sum_post_rating = 0
        sum_coment_rating = 0
        sum_coment = 0

        # post_rating = Post.objects.filter(author=self).values("rating")
        # coment_rating =Comment.objects.filter(author = auth_models.User(pk = self.pk)).values("rating")

        for post_rating in Post.objects.filter(author=self).values("rating"):
            sum_post_rating += post_rating["rating"]

        for coment_rating in Comment.objects.filter(author=auth_models.User(pk=self.pk)).values("rating"):
            sum_coment_rating += coment_rating["rating"]

        for coment_post_auth in Comment.objects.filter(post__author_id = self.pk).values("rating"):
            sum_coment += coment_post_auth["rating"]

        self.rating = (sum_post_rating * 3) + (sum_coment_rating) + (sum_coment)

        self.save()

    def __str__(self):
        return f'{self.author.username}'

# Модель Category
class Category(models.Model):
    name = models.CharField(unique=True, max_length=255)

    def __str__(self):
        return f'{self.name}'

news = 'N'
arts = 'A'

TYPE_POST = [(news ,'новость'),(arts,'статья')]

# Модель Post
class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.DO_NOTHING)
    type = models.CharField(max_length=10, choices=TYPE_POST)
    date = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return f'{self.text[0:124]}...'
# добавлеям для того чтобы правильно выводился на странице

    def __str__(self):
        return f'{self.title}: {self.text[:20]}'

    def get_absolute_url(self):
        return reverse('onenews', args=[str(self.id)])


# Модель PostCategory
class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)



#Модель Comment
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(auth_models.User, on_delete=models.DO_NOTHING)
    text = models.TextField()
    datatime = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

class Subscriber(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)