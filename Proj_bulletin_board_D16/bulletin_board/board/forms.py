from django import forms
from .models import Post, RestponsToPost


# форма поста
class PostForm(forms.ModelForm):
   class Meta:
       model = Post
       fields = [
           'title',
           'author',
           'category',
           'text_post',
           'media',
       ]

# форма отклика
class RespForm(forms.ModelForm):
    class Meta:
        model = RestponsToPost
        fields = ['text',]