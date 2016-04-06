import sae
from zjwebsite import wsgi

application = sae.create_wsgi_app(wsgi.application)


