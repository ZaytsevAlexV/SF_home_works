import random

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.views.generic.edit import CreateView
from .forms import SignUpForm, loginForm, loginFormConfirmCode
from django.shortcuts import render, redirect
from .models import ConfirmCode
from bulletin_board import settings


class SignUp(CreateView):
    model = User
    form_class = SignUpForm
    success_url = '/accounts/login'
    template_name = 'registration/signup.html'

def login_new(request):
    if request.method == 'GET':
        form = loginForm()
        return render(request, 'registration/login.html',
                      {'form': form})
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # генерируем код
            random_code = ''.join([random.choice('0123456789ABCDEF') for x in range(4)])
            ConfirmCode.objects.create(code=random_code,user=user)

            #  отправляем письмо с кодом
            html_content = render_to_string(
                'registration/confirm_code.html',
                {
                       'code': random_code
                }
            )

            msg = EmailMultiAlternatives(
                subject="Подвтерждение входа",
                body='',
                from_email=settings.DEFAULT_FROM_EMAIL,
                to= (user.email,)
            )

            msg.attach_alternative(html_content, 'text/html')
            msg.send()
            response = redirect('/accounts/login/confirm')
            return response
        else:
            response = redirect('login_new')
            return response

def login_ConfirmCode(request):
    if request.method == 'GET':
        form = loginFormConfirmCode()
        return render(request, 'registration/login_by_confirm_code.html',
                      {'form': form})
    if request.method == 'POST':
        user_r = request.POST.get('user')
        print(user_r)
        code = request.POST.get('code')

        if ConfirmCode.objects.filter(code=code, user__id=user_r):
            login(request, User.objects.get(id=user_r))
            response = redirect('post_list')
            return response
        else:
            response = redirect('login_new')
            return response

def logout_view(request):
    logout(request)
    return redirect('post_list')  # Перенаправление на главную страницу после выхода