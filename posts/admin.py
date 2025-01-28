from django.contrib import admin
from .models import Article, Category

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date_posted')

admin.site.register(Article, ArticleAdmin)
admin.site.register(Category)
# Register your models here.
