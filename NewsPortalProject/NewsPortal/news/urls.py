from django.urls import path
# Импортируем созданное нами представление
from .views import NewsList, NewsDetail, NewsSerchList,NewsCreate, NewsEdit, NewsDelete, ArticleCreate, ArticleEdit, ArticleDelete,subscriptions
from django.views.decorators.cache import cache_page


urlpatterns = [
    # path — означает путь.
    # В данном случае путь ко всем товарам у нас останется пустым,
    # чуть позже станет ясно почему.
    # Т.к. наше объявленное представление является классом,
    # а Django ожидает функцию, нам надо представить этот класс в виде view.
    # Для этого вызываем метод as_view.
    path('', cache_page(60*1)(NewsList.as_view()), name='news_list'),
    path('<int:pk>', (NewsDetail.as_view()), name='onenews'),
    path('news/search/', cache_page(60*5)(NewsSerchList.as_view()), name='news_search'),
    path('news/create/', cache_page(60*5)(NewsCreate.as_view()), name='news_create'),
    path('news/<int:pk>/edit/', cache_page(60*5)(NewsEdit.as_view()), name='news_edit'),
    path('news/<int:pk>/delete/', cache_page(60*5)(NewsDelete.as_view()), name='news_delete'),
    path('articles/create/', ArticleCreate.as_view(), name='article_create'),
    path('articles/<int:pk>/edit/', ArticleEdit.as_view(), name='article_edit'),
    path('articles/<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),
    path('subscriptions/', subscriptions, name='subscriptions'),
]
