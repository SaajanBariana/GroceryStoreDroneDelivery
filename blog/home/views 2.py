# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import MySQLdb
import pymysql

db = MySQLdb.connect(host="localhost", user="root", passwd="ENTER HERE", db="grocery_store")   # name of the database
cur = db.cursor() # creates a cursor to execute queries

@api_view(['GET', 'POST'])

def index(request):
    if request.method == 'POST':
        username = request.POST['Username']
        first_person = Person.objects.raw("SELECT * FROM register_user where userid = 'username' ")[0]
        return HttpResponse("This is post request Hello :  " + myvalue)

    else :
        #return HttpResponse("This is get request")
        template = loader.get_template('home/index.html')
        items = []
        #num = 1;
        cur.execute("SELECT * FROM Items")
        for row in cur.fetchall():
            # item["name" + str(num)] = str(row[1])
            # item["weight" + str(num)] = str(row[2])
            # item["cost" + str(num)] = str(row[3])
            # item["quantity" + str(num)] = str(row[4])
            # item["description" + str(num)] = str(row[5])
            item = {"name": str(row[1]), "weight": str(row[2]), "cost": str(row[3]), "quantity": str(row[4]), "tags": str(row[5]), "image": str(row[6]), "description": str(row[7])}
            items.append(item)


            # if (num % 3 == 0):
            #     items.append(item)
            #     num = 1
            #     item.clear()


            # names.append(str(row[1]))
            # weights.append(str(row[2]))
            # costs.append(str(row[3]))
            # quantities.append(str(row[4]))
            # descriptions.append(str(row[5]))
            # items.append(("Number" + str(num), str(row[0])))
            # items.append(("Name" + str(num), str(row[1])))
            # items.append(("Weight" + str(num), str(row[2])))
            # items.append(("Cost" + str(num), str(row[3])))
            # items.append(("Quantity" + str(num), str(row[4])))
            # items.append(("Description" + str(num), str(row[5])))
            # num = num + 1
#            items.append(item)
        context = {"items" : items}
        #context = {"Names" : names, "Weights" : weights, "Costs" : costs, "Quantities" : quantities, "Descriptions" : descriptions}
        return HttpResponse(template.render(context, request))

def hiSaajan(request):
    cur.execute("SELECT * FROM Items where Name = 'Apples' ")
    message = [];
    for row in cur.fetchall():
        message.append("Number: " + str(row[0]) + " Name: " + str(row[1]) + " Weight: " + str(row[2]) + " Cost: " + str(row[3]) + " Quantity: " + str(row[4]) + " Description: " + str(row[5]) + "\n")
    return HttpResponse(message)

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


def search(request):
    if request.method == 'GET':
        # password1234 HelloThisIsAnAI
        conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='saajan1', db='grocery_store')
        cur = conn.cursor()

        # user_filter_choice = request.POST['drop_down_filter']
        # user_search_input = request.POST['search_bar']
        user_filter_choice = request.GET['drop_down_filter']
        user_search_input = request.GET.get('search_bar', None)
        actual_input = user_search_input
        if user_search_input.endswith('s'):
            user_search_input = user_search_input[:len(user_search_input) - 1]


        # Change fruit to whatever table we want to search


        #query = 'SELECT * FROM fruit WHERE name = ' + '"' + user_search_input + '"'  # SELECT * FROM fruit WHERE name = "user_input"; gives us exact result of input


        query = 'SELECT * FROM items WHERE name LIKE ' + '"%' + user_search_input + '%"' # SELECT * FROM fruit WHERE name LIKE "%user_input%"0

        #TODO: Use the filter in the query to filter through results

        cur.execute(query)

        items = []
        """ Hello """
        for row in cur.fetchall():
            item = {"name": str(row[1]), "weight": str(row[2]), "cost": str(row[3]), "quantity": str(row[4]), "tags": str(row[5]), "image": str(row[6]), "description": str(row[7])}
            items.append(item)
        context = {"items" : items, "search" : actual_input}

        # for row in cur.fetchall():
        #     fruit = {"name": str(row[1]),
        #             "weight": str(row[2]),
        #             "cost": str(row[3]),
        #             "quantity": str(row[4]),
        #             "tags": str(row[5]),
        #             "image": str(row[6]),
        #             "description": str(row[7])
        #              }
        #     items.append(fruit)
        #
        # cur.close()
        # conn.close()
        #
        #
        # template = loader.get_template('home/search.html')
        # context = {"items":items}
        template = loader.get_template('home/search.html')
        return HttpResponse(template.render(context, request))



# Create your views here.
