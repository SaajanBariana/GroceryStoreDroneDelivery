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

def creditcard(request):
    template = loader.get_template('home/creditcard.html')
    context = {}
    if request.method == 'POST':
        if request.POST['submit_payment'] == "submit_payment":
            conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='grocery_store')
            cur = conn.cursor()

            CreditCardNumber = request.POST['Credit_Card_Number']
            try:
                CreditCardNumber = "'" + CreditCardNumber + "'"
            except ValueError:
                pass  # it was a string, not an int.

            CSV = request.POST['CSV']
            try:
                CSV = "'" + CSV + "'"
            except ValueError:
                pass  # it was a string, not an int.

            ExpirationDate = request.POST['ExpirationDate']
            try:
                ExpirationDate =  "'" + ExpirationDate + "'"
            except ValueError:
                pass  # it was a string, not an int.

            NameOnCard = request.POST['NameOnCard']
            try:
                NameOnCard = "'" + NameOnCard + "'"
            except ValueError:
                pass  # it was a string, not an int.

            CardZipcode = request.POST['Card_Zipcode']
            try:
                CardZipcode = "'" + CardZipcode + "'"
            except ValueError:
                pass  # it was a string, not an int.

#            query = "DROP Table if exists Payments;"
            query = "INSERT INTO Payments (Credit_Card_Number, CSV, Expiration_Date, Name_on_Card, Card_Zipcode) VALUES (" + CreditCardNumber + ", " + CSV+ ", " + ExpirationDate + ", " + NameOnCard + ", " + CardZipcode + ")"
            try:
                cur.execute(query)
                conn.commit()
                response = ("1",UserID)


            except Exception as e:
                response = ("0",e)
                #raise

            items = [];
            i = 0
            cur.execute("SELECT * FROM Payments")
            for row in cur.fetchall():
                items.append(("name" + str(i), str(row[4])))
                i = i + 1
            context = dict(items)
            #return HttpResponse(template.render(context, request))

            return HttpResponse("hello post from inside method")
    elif request.method == 'GET':
        return HttpResponse(template.render(context, request))
    return response

def confirmation(request):
    template = loader.get_template('home/confirmation.html')
    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='grocery_store')
    cur = conn.cursor()
    items = [];
    i = 0
    cur.execute("SELECT * FROM Payments")
    for row in cur.fetchall():
        item.append(("name" + str(i), str(row[4])))
        i = i + 1

    context = dict(items)
    return HttpResponse(template.render(context, request))

# Create your views here.
