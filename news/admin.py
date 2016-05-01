from django.contrib import admin
from news.models import *

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'nav_display')

class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'pub_date')

admin.site.register(Category, CategoryAdmin)
admin.site.register(News, NewsAdmin)
