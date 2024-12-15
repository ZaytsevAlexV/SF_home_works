from django.contrib import admin
from .models import Post, Comment, Category


# создаём новый класс для представления новостей в админке

class PostAdmin(admin.ModelAdmin):
    # list_display - это список или кортеж со всеми полями, которые вы хотите видеть в таблице статьями
    list_display = ('pk', 'title','preview')
    list_filter = ('title',)
    search_fields = ('title',)
    
admin.site.register(Post,PostAdmin)
admin.site.register(Comment)
admin.site.register(Category)