import datetime

from django.contrib.auth.models import User
from django.db.models import Exists, OuterRef, Subquery
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_protect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin

from .models import Post,Subscriber, Category, RestponsToPost
from .forms import PostForm, RespForm
from .filters import ResponseToPostFilter

#Посмотреть весь список статей
class PostList(ListView):
    queryset = Post.objects.filter(status='A')
    ordering = '-create_date'
    template_name = 'posts_list.html'
    context_object_name = 'posts'
    paginate_by = 5

#Посмотреть статью
class PostOne(LoginRequiredMixin,DetailView):
    raise_exception = True
    permission_required("board.view_post",)
    queryset = Post.objects.filter(status='A')
    template_name = 'post.html'
    context_object_name = 'post'
    # Переопределяем функцию получения, добавляем список откликов
    def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       context['resp'] = RestponsToPost.objects.filter(post = context['post'])
       return context



#Форма добавления объявления
class PostCreate(PermissionRequiredMixin,CreateView):
    raise_exception = True
    permission_required = ("board.add_post",)
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        Post = form.save(commit=False)
        Post.status = 'A'
        Post.create_date = datetime.datetime.now()
        Post.update_date = datetime.datetime.now()
        return super().form_valid(form)

#Форма редактирования объявления
class PostEdit(PermissionRequiredMixin,UpdateView):
    raise_exception = True
    permission_required = ("board.change_post",)
    form_class = PostForm
    queryset = Post.objects.filter(status='A')
    template_name = 'post_edit.html'
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        Post = form.save(commit=False)
        Post.update_date = datetime.datetime.now()
        return super().form_valid(form)

# Представление удаляющее товар.
@csrf_protect
@login_required
@permission_required('board.delete_post',raise_exception=True)
def postdelete(request, pk):
    if request.method == 'GET':
         # получаем все значения модели
         post = Post.objects.get(pk = pk,status='A')
         return render(request, 'post_delete.html', {'post': post})
    if request.method == 'POST':
        post = Post.objects.get(pk=pk)
        post.status = 'NA'
        post.update_date = datetime.datetime.now()
        post.save()
        return render(request, 'post_deleted.html', {'post': post})


#@login_required
@csrf_protect
@login_required
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscriber.objects.create(users=request.user, category=category)
        elif action == 'unsubscribe':
            Subscriber.objects.filter(
                users=request.user,
                category=category,
            ).delete()

    categories_with_subscriptions = Category.objects.annotate(
        user_subscribed=Exists(
            Subscriber.objects.filter(
                users=request.user,
                category=OuterRef('pk'),
            )
        )
    ).order_by('name')
    return render(
        request,
        'subscriptions.html',
        {'categories': categories_with_subscriptions},
    )

# Просмотр списка отклика

class RespToPostlist(PermissionRequiredMixin, ListView):
    raise_exception = True
    permission_required = ("board.view_restponstopost",)
    model = RestponsToPost
    template_name = 'RespToPost_list.html'
    context_object_name = 'resp'
    paginate_by = 5

    # Переопределяем функцию получения списка откликов
    def get_queryset(self):
       # Получаем обычный запрос

       queryset = super().get_queryset()
       print(self.request.user)
       # сделал подзапрос, для того чтобы отфильтровать отклики только по статьям текушего пользователя.
       post_user = Post.objects.filter(author__username =self.request.user).values('id')
       queryset = queryset.filter(post__id__in=Subquery(post_user))
       # Используем наш класс фильтрации.
       # self.request.GET содержит объект QueryDict
       # Сохраняем нашу фильтрацию в объекте класса,
       # чтобы потом добавить в контекст и использовать в шаблоне.
       self.filterset = ResponseToPostFilter(self.request.GET, queryset)
       # Возвращаем из функции отфильтрованный список товаров
       return self.filterset.qs

    def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       # Добавляем в контекст объект фильтрации.
       context['filterset'] = self.filterset
       return context

@csrf_protect
@login_required
@permission_required("board.add_restponstopost",raise_exception=True,)
def create_resp(request, pk, resp=None):
    if request.method == 'GET':
        post = Post.objects.get(pk=pk, status='A')
        form = RespForm()
        return render(request, 'resp_create.html',
                      {'post': post,
                               'form': form,
                              })

    if request.method == 'POST':
        post = Post.objects.get(pk=pk)
        resp = None
        form = RespForm(data= request.POST)
        if form.is_valid():
            # Создаем объект отклика из формы
            resp = form.save(commit=False) # без записи в БД
            # Назначаем Пост отклику
            resp.post = post
            # назначаем автора
            resp.user = request.user
            resp.status = 'n'
            resp.update_date = datetime.datetime.now()
            resp.save()

            #отправка письма автору поста, на отклик
            email = post.author.email
            subject = f'Новый отзыв добавлен на пост {post.title}'
            text_content = (
                f'Текст: {resp.text}\n'
                f'Пользователь:{resp.user}\n\n'
                f'Ссылка на товар:http://127.0.0.1:8000{post.get_absolute_url()}'
            )

            html_content = (
                f'Текст: {resp.text}<br>'
                f'Пользователь: {resp.user}<br><br>'
                f'<a href="http://127.0.0.1:8000{post.get_absolute_url()}">'
                f'Ссылка на объявление с откликом</a>'
            )
            msg = EmailMultiAlternatives(subject, text_content, None, [email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            response = redirect(post)
            return response


@csrf_protect
@login_required
@permission_required("board.add_post",raise_exception=True,)#тут типа я автор, т.к. имею права добавлть посты, а следовательном могу и с откликами работать
def resp_deactiv(request, resp_id):
    if request.method == 'POST':
       resp = RestponsToPost.objects.get(pk=resp_id)
       resp.status = 'de'
       resp.update_date = datetime.datetime.now()
       resp.save()
       response = redirect('resp_list')
       return response
@csrf_protect
@login_required
@permission_required("board.add_post",raise_exception=True,) #тут типа я автор, т.к. имею права добавлть посты, а следовательном могу и с откликами работать
def resp_accept(request, resp_id):
    if request.method == 'POST':
       resp = RestponsToPost.objects.get(pk=resp_id)
       resp.status = 'ac'
       resp.update_date = datetime.datetime.now()
       resp.save()

       post = resp.post

       # отправка письма владельцу отклика
       email = resp.user.email
       subject = f' Принят ваш отклик по объявлению  {post.title}'
       text_content = (
           f'Объявление: {post}\n'
           f'Дата принятия: {resp.update_date}\n'
           f'Текст отклика: {resp.text}\n'
           f'Пользователь:{post.author.username}\n\n'
           f'Ссылка на объявление:http://127.0.0.1:8000{post.get_absolute_url()}'
       )

       html_content = (
           f'Объявление: {post}<br>'
           f'Дата принятия: {resp.update_date}<br>'
           f'Текст отклика: {resp.text}<br>'
           f'Пользователь: {post.author.username}<br><br>'
           f'<a href="http://127.0.0.1:8000{post.get_absolute_url()}"> Ссылка на объявление с откликом </a>'
       )
       msg = EmailMultiAlternatives(subject, text_content, None, [email])
       msg.attach_alternative(html_content, "text/html")
       msg.send()

       response = redirect('resp_list')
       return response

