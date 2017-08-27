# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render_to_response
from django.shortcuts import render, redirect
from .forms import *
from models import *

# Create your views here.
name = "da"


def first(request):
    form = BasketForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        data = form.cleaned_data
        new_form = form.save()
        print "first"
    return render(request, 'basket/base.html', locals())


def addbasket(request):
    print "addbasket"
    form = BasketForm(request.POST or None)
    if request.POST and form.is_valid():
        print "addbasketPOST"
        form.files = {"first"}
        new_form = form.save()
    return render(request, 'basket/base.html', locals())
