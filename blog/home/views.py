

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
    if request.method == 'GET':
        conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='HelloThisIsAnAI', db='grocery_store')
        cur = conn.cursor()

        user_filter_choice = request.GET.get('drop_down_filter', None)
        user_search_input = request.GET.get('search_bar', None)
        # Change fruit to whatever table we want to search

        print(str(user_filter_choice))

        #query = 'SELECT * FROM fruit WHERE name = ' + '"' + user_search_input + '"'
            # SELECT * FROM fruit WHERE name = "user_input"; gives us exact result of input

        query = 'SELECT * FROM fruit WHERE name LIKE ' + '"%' + user_search_input + '%"'
            # SELECT * FROM fruit WHERE name LIKE "%user_input%"

        #query = 'SELECT * FROM fruit WHERE LOCATE(' + "'" + 'name' + "', '{$" + user_search_input + "}') > 0"
        #query = "SELECT * FROM fruit WHERE LOCATE('{$" + str(user_search_input) + "}','name') > 0"
        #print(query)

        cur.execute(query)

        items = []
        """ Hello """
        for row in cur.fetchall():
            fruit = {"name": str(row[1]),
                    "weight": str(row[2]),
                    "cost": str(row[3]),
                    "quantity": str(row[4]),
                    "tags": str(row[5]),
                    "image": str(row[6]),
                    "description": str(row[7])
                     }
            items.append(fruit)

        cur.close()
        conn.close()


        template = loader.get_template('home/search_result.html')
        context = {"items":items}
        return HttpResponse(template.render(context, request))



# def get_search(request):
#     conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='password1234', db='grocery_store')
#     cur = conn.cursor()
#
#     #query = 'SELECT name FROM fruit'# WHERE price = 3'
#     #cur.execute(query)
#
#     info = []
#
#     for r in cur.fetchall():
#         info.append(( "name", r[0]))
#
#     cur.close()
#     conn.close()
#
#
#
#     template = loader.get_template('home/search_result.html')
#     context = dict(info)
#     return HttpResponse(template.render(context, request))

# Create your views here.
