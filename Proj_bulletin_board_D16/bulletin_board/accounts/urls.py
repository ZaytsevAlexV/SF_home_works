from django.urls import path
from .views import SignUp, login_new, login_ConfirmCode,logout_view

urlpatterns = [
    path('signup/', SignUp.as_view(), name='signup'),
    path('login/', login_new, name='login_new'),
    path('login/confirm/', login_ConfirmCode, name='login_confirm'),
    path('logout/', logout_view, name='logout_view'),
]