from django.contrib.auth.models import User
from rest_framework import serializers

from news.models import News, Category


class NewsSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    class Meta:
        model = News
        fields = ('id','url','title','content','author')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    news = serializers.HyperlinkedRelatedField(many=True, view_name='news-detail', read_only=True)
    class Meta:
        model = User
        fields = ('id', 'url', 'username', 'news')

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    news = serializers.HyperlinkedRelatedField(many=True, view_name='news-detail', read_only=True)
    class Meta:
        model = Category
        fields = ('id', 'url', 'name', 'news')
