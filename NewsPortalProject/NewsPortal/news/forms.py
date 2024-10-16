from django import forms
from .models import Post
from django.core.exceptions import ValidationError

class NewsForm(forms.ModelForm):
   class Meta:
       model = Post
       fields = [
           'author',
           'category',
           'title',
           'text',
       ]

   def clean(self):
       cleaned_data = super().clean()
       post_text = cleaned_data.get("text")
       if post_text is not None and len(post_text) < 20:
           raise ValidationError({"post_text": "текст не может быть менее 20 символов."})

       return cleaned_data