from django.conf.urls import url
from news import views

urlpatterns = [
    #url(r'^$', views.index, name='index'),
    url(r'^search/$', views.search, name='search'),
    url(r'^(?P<category_name>\w+)/$', views.display, name='display'),
    url(r'^(?P<category_name>\w+)/(?P<news_id>\d+)/$', views.detail, name='detail'),
    url(r'^add-news/$', views.add_news, name='add_news'),
    url(r'^user/(?P<user_id>\d+)/display/$', views.auther_display, name='auther_display'),

]
