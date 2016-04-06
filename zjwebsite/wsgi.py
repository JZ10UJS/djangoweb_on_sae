# coding: utf-8
import os
import sys
root = os.path.dirname(os.path.dirname(__file__))

# 当时sae未支持django1.8.x, 所以自己上传了django1.8.x 到自建文件夹·site-packages`
sys.path.insert(0, os.path.join(root, 'site-packages'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "zjwebsite.settings")


from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
