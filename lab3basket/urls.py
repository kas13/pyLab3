from django.conf.urls import url
from django.contrib import admin
from lab3basket import views

urlpatterns = [
    url(r'^add_new_basket$', views.add_new_basket, name='add_new_basket'),
    url(r'^(?P<basket_id>[0-9]+)/$', views.view_basket, name="view_basket"),
    url(r'^box$', views.box, name='box'),
    url(r'^', views.first, name='first'),


]
