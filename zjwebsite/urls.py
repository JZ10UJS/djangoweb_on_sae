"""zjwebsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from rest_framework import routers

from news import views 

router = routers.DefaultRouter()
router.register(r'news', views.NewsViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'categorys', views.CategoryViewSet)

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^news/', include('news.urls', namespace='news')),
    url(r'^$', 'news.views.home', name='home'),
    url(r'^login/$', 'news.views.user_login', name='login'),
    url(r'^logout/$', 'news.views.user_logout', name='logout'),
    url(r'^register/$', 'news.views.register', name='register'),
    #url(r'^search/$', 'news.search', name='search'),
    url(r'^auth/username/check-username/$', 'news.views.username_check', name='username_check'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-info/', include(router.urls)),
    url(r'^ueditor/',include('DjangoUeditor.urls' )),
]

from django.conf import settings

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(
            settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
        )