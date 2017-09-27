# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render_to_response
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .forms import *
from models import *
import os
import json
import sys

from lab2.files.myrm import *
from lab2.files.Load_config import load_config
config = load_config()
basket_path = config['trash_path']
info_path = config['information_path']
log_path = config['log_path']
# Create your views here.

@csrf_exempt
def add_new_basket(request):
    print "add_new_basket"
    update_basket2()
    information = update_basket2()
    if request.POST:
        if request.POST.get('add_basket'):
            test_path = request.POST.get("basket_path")
            m = BasketModel(basket_name="1", path=test_path)
            m.save()
            print "add basket"
    basket_models = BasketModel.objects.all()
    context = {'basket_models': basket_models}
    return render(request, 'basket/add_new_basket.html', locals())


def view_basket(request, basket_id):
    current_basket_path = BasketModel.objects.get(id=basket_id)
    current_basket_path = str(current_basket_path)
    if not os.path.exists(current_basket_path):
        os.makedirs(current_basket_path)
        create_json(current_basket_path)
    current_information_path = create_json_path(current_basket_path)
    information = update_basket2(current_information_path)
    print current_basket_path
    print "from veiw basket"
    basket_models = BasketModel.objects.all()
    context = {'basket_models': basket_models}
    return render(request, 'basket/add_new_basket.html', locals())


def first(request):
    print "first"
    update_basket2()
    if (request.POST):
        if (request.POST.get("delete")):
            path = request.POST.get("file_path")
            del_file(path, basket_path, info_path, False, 10000000)
            print path
    information = update_basket2()
    form = BasketForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        data = form.cleaned_data
        new_form = form.save()
        print "first"
    basket_models = BasketModel.objects.all()
    context = {'basket_models': basket_models}
    return render(request, 'basket/add_new_basket.html', locals())


def addbasket(request):
    print "addbasket"
    new_basket_path = request.POST.get('basket_name')
    form = BasketForm(request.POST or None)
    if request.POST and form.is_valid():
        print "addbasketPOST"
        form.files = {"first"}
        new_form = form.save()
    return render(request, 'basket/base.html', locals())

@csrf_exempt
def box(request):
    print "box"
    information = update_basket2()
    copypost = request.POST.copy()
    items = copypost.pop('checkbox')
    lines = getinfo()
    for i in items:
        s = int(i)
        item = lines.__getitem__(s-1)
        item = json.loads(item)
        print item['oldPath']
        restore_file(item['fileName'], basket_path, info_path)
        #restore_file_django(basket_path, info_path, item['fileName'], item['conflict'])
    #print request.POST.get('chbox')
    if request.POST:
        print request.POST
        information = update_basket2()
    return render(request, 'basket/base.html', locals())


def update_basket2(info_path=info_path):
    lines = getinfo(info_path)
    information = []
    for line in lines:
        info = json.loads(line)
        information.append("filename: {0}  old path: {1}".format(info['fileName'], info['oldPath']) + "\n")
    return information


def getinfo(info_path=info_path):
    file = open(info_path, "r")
    info = file.readlines()
    file.close()
    return info