

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

import pymysql


@api_view(['GET', 'POST'])

def index(request):
    template = loader.get_template('home/index.html')
    context = {}
    return HttpResponse(template.render(context, request))

def hiSaajan(request):
    return HttpResponse("Hello saajan")

def tracking_home(request):
    # render simple static page
    template = loader.get_template('home/tracking_home.html')
    context = {}
    return HttpResponse(template.render(context, request))

def tracking(request):
	# render simple static page
    template = loader.get_template('home/tracking.html')
    context = {}
    return HttpResponse(template.render(context, request))

def contact_us(request):
    # render simple static page
    template = loader.get_template('home/contact.html')
    context = {}
    return HttpResponse(template.render(context, request))

def login_register_request(request):
    # render simple static page
    
    """
    Retrieve, update or delete a code snippet.
    """

    if request.method == 'GET':
        return HttpResponse("This is get request")

    elif request.method == 'POST':
         return HttpResponse("This is POST request")
    else :
        template = loader.get_template('home/login_register.html')
        context = {}
        return HttpResponse(template.render(context, request))

def login_register(request):
    template = loader.get_template('home/login_register.html')
    context = {}
    return HttpResponse(template.render(context, request))



def creditCard(request):
    template = loader.get_template('home/creditCard.html')
    context = {}
    return HttpResponse(template.render(context, request))
    
def confirmation(request):
    template = loader.get_template('home/confirmation.html')
    context = {}
    return HttpResponse(template.render(context, request))

def shopping_cart(request):
    template = loader.get_template('home/shopping_cart.html')
    context = {}
    return HttpResponse(template.render(context, request))

def search_bar(request):
    template = loader.get_template('home/search_bar.html')
    context = {}
    return HttpResponse(template.render(context, request))

def search_result(request):
    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='password1234', db='grocery_store')
    cur = conn.cursor()

    query = 'SELECT * FROM fruit WHERE fruit_id = 2'
    # return HttpResponse(query)
    cur.execute(query)

    info = []

    for r in cur.fetchall():
        info.append(("name", r[1]))
# info = {"name", "Apple"}

    cur.close()
    conn.close()

    # if(info != ""):
    #     dictionary = {info}
    # else:
    #     return("0", "error")

    template = loader.get_template('home/search_result.html')
    context = dict(info)
    return HttpResponse(template.render(context, request))







    # template = loader.get_template('home/search_result.html')
    # context = {}
    # return HttpResponse(template.render(context, request))

def get_search(request):
    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='password1234', db='grocery_store')
    cur = conn.cursor()

    query = 'SELECT name FROM fruit WHERE fruit_id = 1'
    #return HttpResponse(query)
    cur.execute(query)

    info = []

    for r in cur.fetchall():
        info.append(( "name", r[2]))

    cur.close()
    conn.close()


    # if(info != ""):
    #     dictionary = {info}
    # else:
    #     return("0", "error")

    template = loader.get_template('home/search_result.html')
    context = dict(info)
    return HttpResponse(template.render(context, request))

# Create your views here.
