from django.shortcuts import render

from django.views.generic import ListView, DetailView
from .models import Post

class NewsList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-date'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'news.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'news'

class NewsDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельной новоси
    model = Post
    # Используем другой шаблон — new.html
    template_name = 'one_news.html'
    # Название объекта, в котором будет выбранный пользователем новость
    context_object_name = 'one_news'