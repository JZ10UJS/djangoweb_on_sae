from django.contrib import admin
from news.models import *

admin.site.register(Category)
admin.site.register(News)
admin.site.register(UserFile)