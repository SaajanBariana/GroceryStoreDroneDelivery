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

#f = open('SQLSetup.txt', "r")
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
        update_input = str(request.COOKIES.get("Updating"))
        if delete_input == "" or delete_input is None:              # Not Deleting
            if update_input != "":                                  # Updating
                name = str(request.COOKIES.get("Name"))
                weight = str(request.COOKIES.get("Weight"))
                cost = str(request.COOKIES.get("Cost"))
                quantity = str(request.COOKIES.get("Quantity"))
                category = str(request.COOKIES.get("Category"))
                image = str(request.COOKIES.get("Image"))
                desc = str(request.COOKIES.get("Desc"))

                update_db(name, weight, cost, quantity, category, image, desc, update_input)
                print("In updating statement")
                template = loader.get_template("home/adminHomePage.html")
                context = getQuery()
                return HttpResponse(template.render(context, request))

            elif update_input == "" or update_input is None:        # Adding
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
    array = request.GET.get('item_array')

    #
            #update_db(name, weight, cost, quantity, category, image, desc, idNo)if array is not None:
    #     the_items = array.split(" , ")
    #     the_items = the_items[0:len(the_items) - 1]
    #     i = 1
    #     the_array = []
    #     for theItem in the_items:
    #         item_stuff = theItem.split("<>")
    #         the_array.append(item_stuff)
    #         i += 1
    #     print("the_array length: : " + str(len(the_array)))
    #     for item in the_array:
    #         if "'" in str(item[7]):
    #             desc = str(item[7]).replace("'", "")
    #         else:
    #             desc = str(item[7])
    #
    #         name = str(item[1])
    #         weight = str(item[2])
    #         cost = str(item[3])
    #         quantity = str(item[4])
    #         category = str(item[5])
    #         image = str(item[6])
    #         idNo = str(item[0])
            # query = "UPDATE grocery_store.items " + \
            #         "SET name = " + str(item[1]) + \
            #         " , weight = " + str(item[2]) + \
            #         " , cost = " + str(item[3]) + \
            #         " , quantity = " + str(item[4]) + \
            #         " , categories = " + str(item[5]) + \
            #         " , image = " + str(item[6]) + \
            #         " , description = " + str(desc) + \
            #         " WHERE itemID = " + str(item[0]) + ";"
            # print(query)
            # try:
            #     cur.execute(query)
            #     conn.commit()
            #     cur.close()
            #     conn.close()
            #
            # except Exception as e:
            #     print(e)

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

def update_db(name, weight, cost, quantity, category, image, desc, idNo):
    query = "UPDATE items SET name = '" + name + "' , weight = '" + weight + "', cost = '" + cost + \
            "', quantity = '" + quantity + "', categories = '" + category + "', image = '" + image + \
            "', description = '" + desc + "' WHERE itemID = " + idNo + ";"
    print(query)
    conn = pymysql.connect(host='localhost', port=3306, user=SQL_username, passwd=SQL_password, db='grocery_store')
    cur = conn.cursor()
    cur.execute(query)
    conn.commit()
    cur.close()
    conn.close()
    # delete_from_db(idNo)
    # add_item_to_db(name, weight, cost, quantity, category, image, desc)


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
    if username is 'admin@admin.com':
        if password is 'admin':
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


def sign_up_controller(request):
    email = request.POST['email']
    email = "'"+str(email)+"'"

    name = request.POST['name']
    token = name
    realname = name
    name = "'"+str(name)+"'"

    password = request.POST['password']
    token = token + password

    token = "'"+token+"'"

    password = "'"+str(password)+"'"

    repeat_password = request.POST['repeat_password']
    repeat_password = "'"+str(repeat_password)+"'"



    #first_person = Person.objects.raw("SELECT * FROM register_user where userid = 'username' ")[0]

    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd=dbpswd, db='grocery_store')
    cur = conn.cursor()

    #query = 'SELECT name  FROM register_user where email = "' + str(username) +  '" AND password = "' + str(password) + '"'
    query = "INSERT INTO register_user (name,email,password,token) VALUES ( " + name +","+ email +","+ password+","+ token + ")"
    #return HttpResponse(query)

    try:
        cur.execute(query)
        conn.commit()
        response = ("1",realname)


    except Exception as e:
        response = ("0",e)
    #raise
    else:
        pass
    finally:
        cur.close()
        conn.close()


    return response



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
