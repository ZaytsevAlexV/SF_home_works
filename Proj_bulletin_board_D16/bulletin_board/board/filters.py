from django_filters import FilterSet
from .models import RestponsToPost, Post

# Создаем свой набор фильтров для модели откликов.
class ResponseToPostFilter(FilterSet):
   class Meta:
       # В Meta классе мы должны указать Django модель,
       # в которой будем фильтровать записи.
       model = RestponsToPost
       # В fields мы описываем по каким полям модели
       # будет производиться фильтрация.
       fields = {
           'post__title':  ['contains'],
           'post__category': [],
           'status': ['in'],
           'user':['in'],
       }
