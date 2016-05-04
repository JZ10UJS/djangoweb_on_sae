# coding: utf-8
from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import User

from DjangoUeditor.models import UEditorField

class Category(models.Model):
    name = models.CharField(max_length=32)
    nav_display = models.BooleanField(u'导航显示', default=True)
    
    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('news:display', args=(self.name,))
        
    
class News(models.Model):
    title = models.CharField(max_length=64)
    author = models.ForeignKey(User, related_name='news')
    summary = models.CharField(max_length=256)
    content = UEditorField(u'内容', height=300, width=1000,
        default=u'', blank=True, imagePath="uploads/images/",
        toolbars='normal', filePath='uploads/files/')
    views = models.IntegerField(default=0)
    pub_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category)
    
    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['-id']
        

