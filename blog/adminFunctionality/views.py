# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader, RequestContext
from home.models import Cart
from django.template.response import TemplateResponse

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import MySQLdb
import time
import pymysql

dbpswd = "enter password"
db = MySQLdb.connect(host="localhost", user="root", passwd= dbpswd, db="grocery_store")   # name of the database
cur = db.cursor() # creates a cursor to execute queries


def adminHomePage(request):
    context = {}
    return TemplateResponse(request, 'home/adminHomePage.html')

    # template = loader.get_template('home/adminHomePage.html')
    # context = {}
    # return HttpResponse(template.render(context, request))



def login_controller(request):
    username = request.POST['Username']
    password = request.POST['Password']
        #first_person = Person.objects.raw("SELECT * FROM register_user where userid = 'username' ")[0]

    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd=dbpswd, db='grocery_store')
    cur = conn.cursor()

    query = 'SELECT name,userid  FROM register_user where email = "' + str(username) +  '" AND password = "' + str(password) + '"'
    #return HttpResponse(query)
    cur.execute(query)

    name = ""

    for r in cur:
        name = (r[0],r[1])

    cur.close()
    conn.close()

    if(name != ""):
        return ("1",name)
    else:
        return ("0","error")

def shoppingcart(request):
    context = RequestContext(request)
    data = Cart.objects.all()
    #if request.method == 'POST':
    #do something
    return TemplateResponse(request, 'home/shoppingcart.html', {"data" : data})
# Create your views here.
