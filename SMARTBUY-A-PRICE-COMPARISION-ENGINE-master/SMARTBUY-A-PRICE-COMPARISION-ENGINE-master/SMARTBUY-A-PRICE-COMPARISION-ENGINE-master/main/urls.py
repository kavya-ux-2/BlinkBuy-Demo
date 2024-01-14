from django.urls import path
from .views import  *
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import include, path
from django.views.generic.base import RedirectView
from django.conf import settings
urlpatterns = [
    path('',home,name='home'),
    path('product/<str:product>',product,name='product'),
    path('<str:search>/',p_list,name= 'list'),
    path(
        "favicon.ico",
        RedirectView.as_view(url=staticfiles_storage.url("favicon.ico")),
    ),
]
