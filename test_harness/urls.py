#Generic Django imports for url functionality
from django.conf.urls import url, include
from django.views.generic import TemplateView
from django.contrib import admin
from application import views, magic_link, payment
#from application.forms import ContactEmail
from django.views.generic.edit import FormView
from functools import partial
#Views import from test_harness app
from test_harness import views
from test_harness import dispatcher
from soapfish.django_ import django_dispatcher
dispatcher2 = django_dispatcher(dispatcher.OfstedOnlineWSSoap_SERVICE)

urlpatterns = [
    url(r'^$', dispatcher2),
   ]


