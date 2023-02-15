from django.contrib import admin
from .forms import ArticleForm
from .models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    form = ArticleForm
