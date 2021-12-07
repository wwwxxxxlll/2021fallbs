from django.contrib import admin
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'content', 'time']
# Register your models here.
