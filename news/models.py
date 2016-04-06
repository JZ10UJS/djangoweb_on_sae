from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=32)
    
    def __unicode__(self):
        return self.name
        
    
class News(models.Model):
    title = models.CharField(max_length=64)
    auther = models.ForeignKey(User)
    summary = models.CharField(max_length=256)
    content = models.TextField()
    views = models.IntegerField(default=0)
    pub_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category)
    
    def __unicode__(self):
        return self.title
        


class UserFile(models.Model):
    user = models.OneToOneField(User)
    
    def __unicode__(self):
        return self.user.name