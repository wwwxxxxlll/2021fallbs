from django.contrib import admin
from index.models import Article
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'content', 'time']
admin.site.register(Article, ArticleAdmin)
# Register your models here.
