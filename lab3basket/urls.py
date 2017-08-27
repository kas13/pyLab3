from django.conf.urls import url
from django.contrib import admin
from lab3basket import views

urlpatterns = [
    url(r'^', views.first),
    # url(r'^add/', views.addbasket)
]
