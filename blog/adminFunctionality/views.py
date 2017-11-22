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

f = open('../blog/SQLSetup.txt', "r")
SQL_username = f.readline()
SQL_username = SQL_username[0: len(SQL_username)-1]
# usernameArray = usernameLine.split(":")
# SQL_username = str(usernameArray[1]).strip()
# if SQL_username.startswith("\"") and SQL_username.endswith("\""):
#     SQL_username = SQL_username[1:len(SQL_username) - 1]
SQL_password = f.readline()

print("username: " + SQL_username + "\npassword: " + SQL_password)
# passwordArray = passwordLine.split(":")
# SQL_password = str(passwordArray[1]).strip()
# if SQL_password.startswith("\"") and SQL_password.endswith("\""):
#     SQL_password = SQL_password[1:len(SQL_password) - 1]

db = MySQLdb.connect(host="localhost", user= SQL_username, passwd= SQL_password, db="grocery_store")   # name of the database
cur = db.cursor() # creates a cursor to execute queries


def adminHomePage(request):
    template = loader.get_template('home/adminHomePage.html')
    context = getQuery()

    if request.method == 'POST':
        delete_input = request.COOKIES.get("Deleting")
        if delete_input == "" or delete_input is None:
            name = str(request.POST.get('add_name_field'))
            weight = str(request.POST.get('add_weight_field'))
            cost = str(request.POST.get('add_cost_field'))
            quantity = str(request.POST.get('add_quantity_field'))
            category = str(request.POST.get('add_category_field'))
            image = str(request.POST.get('add_image_field'))
            desc = str(request.POST.get('add_desc_field'))

            add_item_to_db(name, weight, cost, quantity, category, image, desc)
            template = loader.get_template("home/adminHomePage.html")
            context = getQuery()
            return HttpResponse(template.render(context, request))
        elif delete_input != "":
            delete_from_db(int(delete_input))
            print("In deleting statement")
    array = request.GET.get('item_array');

    if array is not None:
        the_items = array.split(" , ")
        the_items = the_items[0:len(the_items) - 1]
        i = 1
        the_array = []
        for theItem in the_items:
            item_stuff = theItem.split("<>")
            the_array.append(item_stuff)
            i += 1
        print("the_array length: : "+ str(len(the_array)))
        for item in the_array:
            if "'" in str(item[7]):
                desc = str(item[7]).replace("'", "")
            else:
                desc = item[7]

            conn = pymysql.connect(host='localhost', port=3306, user=SQL_username, passwd=SQL_password, db='grocery_store')
            cur = conn.cursor()
            query = "UPDATE items " \
                "SET name = '" + item[1] + "' , weight = '" + item[2] + \
                "' , cost = '"+ (item[3]) + \
                "' , quantity = '" + (item[4]) + \
                "' , categories = '" + item[5] + \
                "' , description = '" + desc + \
                "' WHERE itemID = " + item[0] + ";"
            print(query)
            try:
                cur.execute(query)
                conn.commit()
                cur.close()
                conn.close()

            except Exception as e:
                print(e)
    context = getQuery()
    return HttpResponse(template.render(context, request))

def getQuery():
    items = []
    conn = pymysql.connect(host='localhost', port=3306, user=SQL_username, passwd=SQL_password, db='grocery_store')
    cur = conn.cursor()
    cur.execute("SELECT * FROM Items")
    for row in cur.fetchall():
        item = {"id": str(row[0]), "name": str(row[1]), "weight": str(row[2]), "cost": str(row[3]),
                "quantity": str(row[4]),
                "tags": str(row[5]), "image": str(row[6]), "description": str(row[7])}
        items.append(item)
    context = {"items": items}
    cur.close()
    conn.close()
    return context

def  add_item_to_db(name, weight, cost, quantity, category, image, desc):
    query = "INSERT INTO items " \
            "( name, weight, cost, quantity, categories, image, description) " \
            "VALUES('" + name + "', '" + weight + "', '" + cost + "', '"\
            + quantity + "', '" + category + "', '" + image + "', '" + desc + "');"
    print(query)
    conn = pymysql.connect(host='localhost', port=3306, user=SQL_username, passwd=SQL_password, db='grocery_store')
    cur = conn.cursor()
    cur.execute(query)
    conn.commit()
    cur.close()
    conn.close()

def delete_from_db(id):
    query = "DELETE FROM items WHERE itemID = " + str(id)
    conn = pymysql.connect(host='localhost', port=3306, user=SQL_username, passwd=SQL_password, db='grocery_store')
    cur = conn.cursor()
    cur.execute(query)
    conn.commit()
    cur.close()
    conn.close()



def login_controller(request):
    username = request.POST['Username']
    password = request.POST['Password']
        #first_person = Person.objects.raw("SELECT * FROM register_user where userid = 'username' ")[0]
    print("username: " + username + "\npassword: " + password)
    if username == 'admin@admin.com':
        if password == 'admin':
            print("This is the admin")
    conn = pymysql.connect(host='localhost', port=3306, user= SQL_username, passwd=SQL_password, db='grocery_store')
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


# Login controller if request is login then

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
        template = loader.get_template('home/adminLogin.html')
        context = {}
        return HttpResponse(template.render(context, request))

def login_register(request):
    template = loader.get_template('home/adminLogin.html')
    context = {}
    return HttpResponse(template.render(context, request))
