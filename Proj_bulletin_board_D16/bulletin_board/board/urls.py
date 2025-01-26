from django.urls import path


from .views import (PostList, PostOne, PostCreate, PostEdit, postdelete, subscriptions,
                    RespToPostlist, create_resp, resp_deactiv,resp_accept)

urlpatterns = [
    path('', PostList.as_view(), name='post_list'),
    path('<int:pk>/', PostOne.as_view(), name='post'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('<int:pk>/edit', PostEdit.as_view(), name='post_edit'),
    path('<int:pk>/delete', postdelete, name='post_delete'),
    path('subscriptions/', subscriptions, name='subscriptions'),
    path('responses/', RespToPostlist.as_view(), name='resp_list'),
    path('<int:pk>/responses/create', create_resp, name='create_resp'),
    path('responses/<int:resp_id>/deactiv', resp_deactiv, name='resp_deactiv'),
    path('responses/<int:resp_id>/accept', resp_accept, name='resp_accept'),
]


