# coding: utf-8
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

from rest_framework import viewsets

from news.bing_search import run_query
from news.models import *
from news.forms import *
from news.serializers import *


def home(req):
    username = 'ZJ'
    news_list = News.objects.all().order_by('-pub_date')[:10]
    return render(req, 'news/home.html', {'username':username,'news_list':news_list})
    

def index(req):
    pass

def search(request):
    result_list = []

    if request.method == 'GET':
        query = request.GET['query'].strip()
        if query:
            # Run our Bing function to get the results list!
            result_list = run_query(query)
    return render(request, 'news/search.html', {'news_list': result_list})    

def author_display(req, user_id):
    user = get_object_or_404(User, id=user_id)
    news_list = user.news.all()
    return render(req,'news/author_display.html', {'news_list':news_list,'username':user})

def display(req, category_name):
    category = get_object_or_404(Category, name=category_name.lower())
    news_list = category.news_set.all().order_by('-pub_date')[:5]
    return render(req, 'news/display.html', {'category':category,'news_list':news_list})


def detail(req, category_name, news_id):
    category = get_object_or_404(Category, name=category_name)
    news = category.news_set.get(id=news_id)
    return render(req, 'news/detail.html', {'news':news})
    
@login_required
def add_news(req):
    if req.method == 'POST':
        form = AddPageForm(req.POST)
        if form.is_valid():
            news = form.save(commit=False)
            news.author = req.user
            news.save()
            return HttpResponseRedirect(reverse('home'))        
    else:
        form = AddPageForm()
    return render(req, 'news/add_news.html', {'form':form})


def register(req):
    if req.method == 'POST':
        user_form = RegisterForm(data=req.POST)
        print req.POST
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user.password)
            user.save()
            return HttpResponseRedirect('/login/')
    return render(req, 'news/register.html')
    
def user_login(req):
    if req.method == 'POST':
        username = req.POST.get('username')
        password = req.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(req, user)
                return HttpResponseRedirect(reverse('home'))
            else:
                return HttpResponse('not active')
        else:
            return HttpResponseRedirect('/login/')
    else:
        form = RegisterForm()
    return render(req, 'news/login.html', {'form':form})

@login_required    
def user_logout(req):
    logout(req)
    return HttpResponseRedirect(reverse('home'))
    

def username_check(request):
    alpha = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    digit = '0123456789'
    underline = '_'
    al = alpha+digit+underline
    
    response = {}
    username = request.GET['username'].strip()
    response['is_allowed'] = False

    if username[0] not in alpha+underline:
        response['info'] = u'必须以字母或下划线开始'
    elif not all([1 if x in al else 0 for x in username]):
        response['info'] = u'只能包含数字 字母 _'
    elif User.objects.filter(username=username):
        response['info'] = u'该用户名已经注册'
    else:
        response['is_allowed'] = True
        response['info'] = u'该用户名可以使用'

    return JsonResponse(response)


# RESTful api

class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer