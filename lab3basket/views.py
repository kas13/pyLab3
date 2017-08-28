# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render_to_response
from django.shortcuts import render, redirect
from .forms import *
from models import *
import os
import json
import sys

from files.Load_config import Load_config
config = Load_config()
basket_path = config['trash_path']
info_path = config['information_path']
log_path = config['log_path']
# Create your views here.



def first(request):
    print "load"
    listdir = os.listdir(basket_path)
    lines = getinfo()
    information = []
    numb = []
    for line in lines:
        info = json.loads(line)
        print lines.index(line)
        numb.append(int(information.__len__()))
        information.append("filename: {0}  old path: {1}".format(info['fileName'], info['oldPath'])+"\n")
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


def box(request):
    print "box"
    copypost = request.POST.copy()
    items = copypost.pop('checkbox')
    lines = getinfo()
    for i in items:
        s = int(i)
        item = lines.__getitem__(s-1)
        item = json.loads(item)
        print item['oldPath']
    #print request.POST.get('chbox')
    if request.POST:
        print request.POST
    return render(request, 'basket/base.html', locals())


def getinfo(info_path=info_path):
    file = open(info_path, "r")
    info = file.readlines()
    file.close()
    return info