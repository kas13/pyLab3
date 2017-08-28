from django.conf.urls import url
from django.contrib import admin
from lab3basket import views

urlpatterns = [
    url(r'^box$', views.box, name='box'),
    url(r'^', views.first, name='first'),

]
