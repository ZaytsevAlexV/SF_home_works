from django_filters import FilterSet, DateTimeFilter
from django.forms import DateTimeInput
from .models import Post

# Создаем свой набор фильтров для модели Product.
# FilterSet, который мы наследуем,
# должен чем-то напомнить знакомые вам Django дженерики.
class NewsFilter(FilterSet):
    added_after = DateTimeFilter(
        field_name='date',
        lookup_expr='gt',
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'},
            ),
    )

    class Meta:
       model = Post
       fields = {
           # поиск по названию
           'title': ['contains'],
           'category': ['exact'],
       }