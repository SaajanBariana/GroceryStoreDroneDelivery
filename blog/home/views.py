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

dbpswd = "saajan1"
db = MySQLdb.connect(host="localhost", user="root", passwd= dbpswd, db="grocery_store")   # name of the database
cur = db.cursor() # creates a cursor to execute queries

@api_view(['GET', 'POST'])

def index(request):
    template = loader.get_template('home/index.html')
    items = []
    cur.execute("SELECT * FROM Items")
    for row in cur.fetchall():
        item = {"name": str(row[1]), "weight": str(row[2]), "cost": str(row[3]), "quantity": str(row[4]), "tags": str(row[5]), "image": str(row[6]), "description": str(row[7])}
        items.append(item)

    if request.method == 'POST':
        if(request.POST['req_type'] == "Log-in"):
            tuple_response = login_controller(request)
        elif(request.POST['req_type'] == "sign-up"):
            tuple_response = sign_up_controller(request)
            #return sign_up_controller(request)
            #return HttpResponse(name)

        if(tuple_response[0] == "1"):
            context = {
                'username': tuple_response[1][0],
                'email': tuple_response[1][1],
                "items" : items

            }
            template = loader.get_template('home/index.html')
            #return HttpResponse(template.render(context, request))
            response = HttpResponse(template.render(context, request))
            #response.set_cookie('login_username', tuple_response[1])
            return response

        elif (tuple_response[0] == "0"):

            if "Duplicate entry" in str(tuple_response[1]):
                template = loader.get_template('home/login_register.html')
                context = {'account_error': "Account already register", "items" : items}
                return HttpResponse(template.render(context, request))

            elif (tuple_response[1] == "error"):
                template = loader.get_template('home/login_register.html')
                context = {'account_error': "Username and password not match", "items" : items}
                return HttpResponse(template.render(context, request))


    else :
        context = {"items" : items}
        return HttpResponse(template.render(context, request))

def hiSaajan(request):
    cur.execute("SELECT * FROM Items where Name = 'Apples' ")
    message = [];
    for row in cur.fetchall():
        message.append("Number: " + str(row[0]) + " Name: " + str(row[1]) + " Weight: " + str(row[2]) + " Cost: " + str(row[3]) + " Quantity: " + str(row[4]) + " Description: " + str(row[5]) + "\n")
    return HttpResponse(message)


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



# Login controller if request is login then

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


def tracking_home(request):

    # render simple static page


    if request.method == 'POST':

         if(request.POST['tracking_number'] != ""):
            if(tracking_controller(request)[0] == "1"): # if no error mean is 1 then return that result
                result_set = tracking_controller(request)[1];
                template = loader.get_template('home/tracking.html')
                context = {"destination":result_set[0],
                "current_lang":result_set[1],
                "current_lat":result_set[2],
                "status":result_set[5],
                "track_id":result_set[6],
                }
                #return HttpResponse("Not valid tracking number")
                return HttpResponse(template.render(context, request))
                return HttpResponse(tracking_controller(request)[1][0])
            else:
                template = loader.get_template('home/tracking.html')
                context = {"tracking_error":"Tracking Number Not valid "}
                #return HttpResponse("Not valid tracking number")
                return HttpResponse(template.render(context, request))
         else:
            template = loader.get_template('home/tracking_home.html')
            context = {"value":"empty"}
            return HttpResponse(template.render(context, request))


    elif request.method == 'GET':
        template = loader.get_template('home/tracking_home.html')
        context = {}
        return HttpResponse(template.render(context, request))
    else:
        template = loader.get_template('home/tracking_home.html')
        context = {}
        return HttpResponse(template.render(context, request))

# This is controller for tracking
#request will contain post request from tracking page
# check tracking number with database
#
def tracking_controller(request):
    tracking_number = request.POST['tracking_number']

        #first_person = Person.objects.raw("SELECT * FROM register_user where userid = 'username' ")[0]

    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd=dbpswd, db='grocery_store')
    cur = conn.cursor()

    query = 'SELECT destination,current_lat,current_long,start_lat,start_long,status,track_id  FROM tracking_update where track_id = "' + str(tracking_number) +  '" '
    #return HttpResponse(query)
    cur.execute(query)

    result = ""

    for r in cur:
        result = r

    cur.close()
    conn.close()

    if(result != ""):
        return ("1",result)
    else:
        return ("0","error")

def tracking(request):
	# render simple static page
    template = loader.get_template('home/tracking_home.html')
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

def navigation_bar(request):
    template = loader.get_template('home/nav.html')
    context = {}
    return HttpResponse(template.render(context, request))

# Payment handler from alvin

def creditcard(request):
    template = loader.get_template('home/creditcard.html')
    context = {}

    if request.method == 'POST':
        if request.POST['submit_payment'] != "":

            conn = pymysql.connect(host='localhost', port=3306, user='root', passwd=dbpswd, db='grocery_store')
            cur = conn.cursor()
            # Credit Card Submission form

            try:
                CreditCardNumber = request.POST['Credit_Card_Number']
                CreditCardNumber = "'" + CreditCardNumber + "'"
            except ValueError:
                pass  # it was a string, not an int.


            try:
                CSV = request.POST['CSV']
                #CSV = "'" + CSV + "'"
            except ValueError:
                pass  # it was a string, not an int.


            try:
                ExpirationDate = request.POST['ExpirationDate']
                ExpirationDate =  "'" + ExpirationDate + "'"
            except ValueError:
                pass  # it was a string, not an int.


            try:
                NameOnCard = request.POST['NameOnCard']
                NameOnCard = "'" + NameOnCard + "'"
            except ValueError:
                pass  # it was a string, not an int.


            try:
                CardZipcode = request.POST['Card_Zipcode']
                CardZipcode = "'" + CardZipcode + "'"
            except ValueError:
                pass  # it was a string, not an int.

# Address Information
            Street_Name = request.POST['Street_Name']
            try:
                destination = Street_Name
                StreetName = "'" + Street_Name + "'"
            except ValueError:
                pass  # it was a string, not an int.

            City = request.POST['City']
            try:
                destination =  destination + " , " + City
                City =  "'" + City + "'"
            except ValueError:
                pass  # it was a string, not an int.

            State = request.POST['State']
            try:
                destination = destination + " , " + State
                State = "'" + State + "'"
            except ValueError:
                pass  # it was a string, not an int.


            Zip_Code = request.POST['Zip_Code']
            try:
                destination = destination + " , " + Zip_Code
                Zip_Code = "'" + Zip_Code + "'"
            except ValueError:
                pass  # it was a string, not an int.


            try:
                StoreID = request.POST['store_id']
                #StoreID = "'" + StoreID + "'"
            except ValueError:
                pass  # it was a string, not an int.

            ran = (str(int(time.time())))
            try:
                ran = (str(int(time.time())))

                #ran = "'" + ran + "'"
            except ValueError:
                pass  # it was a string, not an int.

            try:
                user_id = request.POST['user_id']

                #ran = "'" + ran + "'"
            except ValueError:
                pass  # it was a string, not an int.


            #print ("STORE VALUE: " + StoreID)
            #return HttpResponse(ran + ", " + destination+ ", " + StoreID)
            destination = "'" + destination + "'"

            query = "INSERT INTO tracking (track_id, destination, store_id) VALUES (" + ran + ", " + destination+ ", " + StoreID + ")"
            try:
                cur.execute(query)
                conn.commit()
                response = ("1",UserID)
            except Exception as e:
                response = ("0",e)

            cur.close()
            conn.close()

            # query = "INSERT INTO User Info (Street_Name, State, City, Zip_Code) VALUES (" + StreetName + ", " + State+ ", " + City + ", " + Zip_Code + ")"
            # try:
            #     cur.execute(query)
            #     conn.commit()
            #     response = ("1",UserID)


            # except Exception as e:
            #     response = ("0",e)



            conn = pymysql.connect(host='localhost', port=3306, user='root', passwd=dbpswd, db='grocery_store')
            cur = conn.cursor()
#            query = "DROP Table if exists Payments;"
            query = "INSERT INTO Payments (UserID,Credit_Card_Number, CSV, Expiration_Date, Name_on_Card, Card_Zipcode) VALUES (" + user_id + ", "+ CreditCardNumber + ", " + CSV+ ", " + ExpirationDate + ", " + NameOnCard + ", " + CardZipcode + ")"
            try:
                cur.execute(query)
                conn.commit()
                response = ("1",UserID)
                cur.close()
                conn.close()


            except Exception as e:
                response = ("0",e)
                #raise

            # items = [];
            # i = 0
            # cur.execute("SELECT * FROM Payments")
            # for row in cur.fetchall():
            #     items.append(("name" + str(i), str(row[4])))
            #     i = i + 1
            #     #items.append(("name0", alvin)
            # context = dict(items)

            # return HttpResponse(template.render(context, request))
            template = loader.get_template('home/index.html')
            context = {"tracking_id" : 101}
            return HttpResponse(template.render(context, request))
    elif request.method == 'GET':
        return HttpResponse(template.render(context, request))
    return HttpResponse("hello just return")

def confirmation(request):
    template = loader.get_template('home/confirmation.html')
    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd=dbpswd, db='grocery_store')
    cur = conn.cursor()

    ran = (str(int(time.time())))
    query = "INSERT INTO tracking (track_id, ) VALUES (" + ran +  ")"
    try:
        cur.execute(query)
        conn.commit()
        response = ("1",UserID)

    except Exception as e:
        response = ("0",e)
        #raise
    items = [];
    i = 0
    cur.execute("SELECT * FROM tracking")
    for row in cur.fetchall():
        items.append(("name" + str(i), str(row[4])))
        i = i + 1

    context = dict(items)
    # return HttpResponse(template.render(context, request))
    return HttpResponse("Random Value: " + ran)





def shoppingcart(request):
    context = RequestContext(request)
    data = Cart.objects.all()
    #if request.method == 'POST':
    #do something
    return TemplateResponse(request, 'home/shoppingcart.html', {"data" : data})

def search(request):
    if request.method == 'GET':
        # password1234 HelloThisIsAnAI
        conn = pymysql.connect(host='localhost', port=3306, user='root', passwd= dbpswd, db='grocery_store')
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


        query = ''
        if user_filter_choice != "Categories" and user_search_input != "":  # Displays search result in category
            query = 'SELECT * FROM items WHERE categories = "' + user_filter_choice + '" AND name LIKE "' + user_search_input + '"'
        elif user_filter_choice != "Categories":  # Displays all items in this category, no input
            query = 'SELECT * FROM items WHERE categories = "' + user_filter_choice + '"'
        elif user_search_input == "" and user_filter_choice == "Categories":  # Displays all items
            query = 'SELECT * FROM items'
        else:  # Searches for items in all categories, no filter
            query = 'SELECT * FROM items WHERE name LIKE ' + '"%' + user_search_input + '%"'
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
