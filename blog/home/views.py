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

from six.moves import input

# f = open('../blog/SQLSetup.txt', "r")
# usernameLine = f.readline()
# usernameArray = usernameLine.split(":")
# SQL_username = str(usernameArray[1]).strip()
# if SQL_username.startswith("\"") and SQL_username.endswith("\""):
#     SQL_username = SQL_username[1:len(SQL_username) - 1]
SQL_username = str(input("What is your MySQL username: "))
SQL_username = SQL_username.strip();
# passwordLine = f.readline()
# passwordArray = passwordLine.split(":")
# # SQL_password = str(passwordArray[1]).strip()
# if SQL_password.startswith("\"") and SQL_password.endswith("\""):
#     SQL_password = SQL_password[1:len(SQL_password) - 1]
SQL_password = str(input("What is your MySQL password: "))
SQL_password = SQL_password.strip()
f = open('../blog/SQLSetup.txt', "w")
f.write(SQL_username + "\n")
f.write(SQL_password)

f.close()

dbuser = SQL_username
dbpswd = SQL_password
tracking_number=[]
tracking_number_string=""



def get_item():
    items = []
    db = MySQLdb.connect(host="localhost", user=dbuser, passwd= dbpswd, db="grocery_store")   # name of the database

    cur = db.cursor() # creates a cursor to execute queries

    cur.execute("SELECT * FROM Items")
    for row in cur.fetchall():
        if (row[4] > 0):
            item = {"itemID": str(row[0]),"name": str(row[1]), "weight": str(row[2]), "cost": str(row[3]), "quantity": str(row[4]), "tags": str(row[5]), "image": str(row[6]), "description": str(row[7])}
            items.append(item)
    
    db.close()
    cur.close()

    return items

@api_view(['GET', 'POST'])
def index(request):
    template = loader.get_template('home/index.html')
 
    items = get_item()

    if request.method == 'POST':
        if(request.POST['req_type'] == "Log-in"):
            tuple_response = login_controller(request)
        elif(request.POST['req_type'] == "sign-up"):
            tuple_response = sign_up_controller(request)


        if(tuple_response[0] == "1"):
            context = {
            'username': tuple_response[1][0],
            'u_id':tuple_response[1][1],
            'email': tuple_response[1][2],
            'u_token':'none',
            'address':'none',
            'payment':'none',
            "items" : items
            }
            template = loader.get_template('home/index.html')
            #return HttpResponse(template.render(context, request))
            response = HttpResponse(template.render(context, request))
            #response.set_cookie('login_username', tuple_response[1])
            return response

            #return sign_up_controller(request)
            #return HttpResponse(name)
        # if (usernameCookie == None):
        #     print("Goes into statement")
        #     usernameCookie = tuple_response[1]
        

        elif(tuple_response[0] == "2"):
            card = tuple_response[1][5]+","+tuple_response[1][6] +","+tuple_response[1][7]+","+tuple_response[1][8]+","+tuple_response[1][9]
            print("string - >"+tracking_number_string)
            delete = "yes"
            context = {
                'username': tuple_response[1][0],
                'u_id':tuple_response[1][1],
                'email': tuple_response[1][2],
                'u_token':tuple_response[1][3],
                'address':tuple_response[1][4],
                'payment':card,
                'tracking_number':tracking_number_string,
                'deleteCookies' : delete,
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

            elif (tuple_response[1] == "error_l"):
                template = loader.get_template('home/login_register.html')
                context = {'account_error': "Username and password not match", "items" : items}
                return HttpResponse(template.render(context, request))
            elif (tuple_response[1] == "error_s"):
                template = loader.get_template('home/login_register.html')
                context = {'account_error': "Account already register", "items" : items}
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

def handle404(request, somethingElse):
    template = loader.get_template('home/404.html')
    context = {}
    return HttpResponse(template.render(context, request))





def get_user_info_from_db(username,password):
    conn = pymysql.connect(host='localhost', port=3306, user=dbuser, passwd=dbpswd, db='grocery_store')
    cur = conn.cursor()
    #query = 'SELECT name,userid,email  FROM register_user where email = "' + str(username) +  '" AND password = "' + str(password) + '"'
    #query = 'select u.name,u.userid,u.email,u.token,t.destination from tracking t left join register_user u on t.user_id = u.userid where email = "' + str(username) +  '" AND password = "' + str(password) + '"'
    query = 'select distinct d.* from (select r.*,p.Name_on_Card,p.Card_Zipcode,p.Credit_Card_Number,p.CSV,p.Expiration_Date from Payments p,(select u.name,u.userid,u.email,u.token,t.destination from tracking t left join register_user u on t.user_id = u.userid where email = "'  + str(username) +  '" AND password = "'+ str(password) +'" ) as r where r.userid = p.UserID) as d '
   
    #return HttpResponse(query)
    cur.execute(query)
    result = ""
    for r in cur:
        result = (r[0],r[1],r[2],r[3],r[4],r[5],str(r[6]),r[7],str(r[8]),r[9])
    cur.close()
    conn.close()

    return result

def get_user_login_result_from_db(username,password):
    conn = pymysql.connect(host='localhost', port=3306, user=dbuser, passwd=dbpswd, db='grocery_store')
    cur = conn.cursor()
    query = 'SELECT name,userid,email  FROM register_user where email = "' + str(username) +  '" AND password = "' + str(password) + '"'
    #query = 'select u.name,u.userid,u.email,u.token,t.destination from tracking t left join register_user u on t.user_id = u.userid where email = "' + str(username) +  '" AND password = "' + str(password) + '"'
   # query = 'select distinct d.* from (select r.*,p.Name_on_Card,p.Card_Zipcode,p.Credit_Card_Number,p.CSV,p.Expiration_Date from Payments p,(select u.name,u.userid,u.email,u.token,t.destination from tracking t left join register_user u on t.user_id = u.userid where email = "'  + str(username) +  '" AND password = "'+ str(password) +'" ) as r where r.userid = p.UserID) as d '
   
    #return HttpResponse(query)
    cur.execute(query)
    name = ""
    for r in cur:
        name = (r[0],r[1],r[2])
   
    cur.close()
    conn.close()

    return name

def login_controller(request):
    username = request.POST['Username']
    password = request.POST['Password']
    global tracking_number_string
        #first_person = Person.objects.raw("SELECT * FROM register_user where userid = 'username' ")[0]
    result_from_1st = ""
    result_from_1st = get_user_info_from_db(username,password)
    result = ""
    if(result_from_1st == ""):
        result = get_user_login_result_from_db(username,password)
        if(result == ""):

            return ("0","error_l")
        else:
            return ("1",result)
    else:
        track_id = result_from_1st[1]
        query = 'select track_id from tracking where user_id= "' + str(track_id) + '"'
        print(query)
        result = select_track_query(query)
        if(result[0] == "1"):
            tracking_number = result[1]
            tracking_number_string = ','.join(map(str, tracking_number)) 
            print(tracking_number)
            print("-----------------------------")
            print(tracking_number_string)
        return ("2",result_from_1st)
    

# Login controller if request is login then

def sign_up_controller(request):
    email = request.POST['email']
    t_email = email
    email = "'"+str(email)+"'"

    name = request.POST['name']
    token = name
    realname = name
    name = "'"+str(name)+"'"
    password = request.POST['password']
    t_pass = password
    token = token + password
    token = "'"+token+"'"
    password = "'"+str(password)+"'"
    repeat_password = request.POST['repeat_password']
    repeat_password = "'"+str(repeat_password)+"'"

        #first_person = Person.objects.raw("SELECT * FROM register_user where userid = 'username' ")[0]

    conn = pymysql.connect(host='localhost', port=3306, user=dbuser, passwd=dbpswd, db='grocery_store')
    cur = conn.cursor()

    #query = 'SELECT name  FROM register_user where email = "' + str(username) +  '" AND password = "' + str(password) + '"'
    query = "INSERT INTO register_user (name,email,password,token) VALUES ( " + name +","+ email +","+ password+","+ token + ")"
    #return HttpResponse(query)

    try:
        cur.execute(query)
        conn.commit()
        response = 1


    except Exception as e:
        response = 0
        #raise
    else:
        pass
    finally:
        cur.close()
        conn.close()

    if(response == 1):
        response = ("1",get_user_login_result_from_db(t_email,t_pass))
    else:
        response = ("0","error_s")

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

                update_tracking_record(str(result_set[6]))
                #return HttpResponse("Not valid tracking number")
                return HttpResponse(template.render(context, request))
               
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

    conn = pymysql.connect(host='localhost', port=3306, user=dbuser, passwd=dbpswd, db='grocery_store')
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
        #if(result[5] == 0):
           # update_tracking_record(tracking_number)

        return ("1",result)

    else:
        return ("0","error")

#update tracking table 
# take tracking number as argument
def update_tracking_record(tracking_num):
    conn = pymysql.connect(host='localhost', port=3306, user=dbuser, passwd=dbpswd, db='grocery_store')
    cur = conn.cursor()   
    query = 'UPDATE `grocery_store`.`tracking_update` SET `status`=1 WHERE `track_id`='+tracking_num+';'
    #return HttpResponse(query)


    try:
        cur.execute(query)
        conn.commit()
        response = 1


    except Exception as e:
        response = 0
        #raise
   
    finally:
        cur.close()
        conn.close()

    return response


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
#for run insert,update statment
def update_tracking_database(query):
    conn = pymysql.connect(host='localhost', port=3306, user=dbuser, passwd=dbpswd, db='grocery_store')
    cur = conn.cursor()
    try:
        cur.execute(query)
        conn.commit()
        response = ("1","success")      
    except Exception as e:
        response = ("0",e)
    finally:
        cur.close()
        conn.close()
    return response

# Payment handler from alvin

def creditcard(request):
    template = loader.get_template('home/creditcard.html')
    context = {}
    #REMOVE THIS AFTER FIX
    
    if request.method == 'POST':
        if request.POST['submit_payment'] != "":

            try:
                CreditCardNumber = request.POST['Credit_Card_Number']
               # CreditCardNumber = "'" + CreditCardNumber + "'"
                CSV = request.POST['CSV']
                #CSV = "'" + CSV + "'"
                NameOnCard = request.POST['NameOnCard']
                #NameOnCard = "'" + NameOnCard + "'"
                CardZipcode = request.POST['Card_Zipcode']
               # CardZipcode = "'" + CardZipcode + "'"
                Street_Name = request.POST['Street_Name']
                destination = Street_Name
                StreetName = "'" + Street_Name + "'"
                City = request.POST['City']
                destination =  destination + " , " + City
                City =  "'" + City + "'"
                State = request.POST['State']
                destination = destination + " , " + State
                State = "'" + State + "'"
                Zip_Code = request.POST['Zip_Code']
                destination = destination + " , " + Zip_Code
                Zip_Code = "'" + Zip_Code + "'"
                StoreID = request.POST['user_id']
                ExpirationDate = request.POST['exp_date']

                ran = (str(int(time.time())))

                #ran = "'" + ran + "'"
                user_id = request.POST['user_id']

                #ran = "'" + ran + "'"
            except ValueError:
                pass  # it was a string, not an int.


            #print ("STORE VALUE: " + StoreID)
            #return HttpResponse(ran + ", " + destination+ ", " + StoreID)
            
            query = 'INSERT INTO Payments (UserID,Credit_Card_Number, CSV, Expiration_Date, Name_on_Card, Card_Zipcode) VALUES ("' + user_id + '", "'+ CreditCardNumber + '", "' + CSV+ '", "' + ExpirationDate + '", "' + NameOnCard + '", "' + CardZipcode + '")'
            result1 = update_tracking_database(query)
            print(result1)

            query = 'INSERT INTO tracking (track_id, destination, user_id) VALUES ("' + ran + '", "' + destination+ '", "' + user_id + '")'
            result2 = update_tracking_database(query)
            print(result2)

            if(result2[0] == "1"):
                query_temp = ", '37.324240', '37.324240', '-121.882652', '-121.882652', '0' )"
                query = 'INSERT INTO `grocery_store`.`tracking_update` (`track_id`, `user_id`, `destination`, `current_lat`, `start_lat`, `current_long`, `start_long`, `status`) VALUES ("' + ran + '", "' + user_id+ '", "' + destination + '" ' + query_temp
                result3 = update_tracking_database(query)
                if(result3[0]  == 0):
                    return HttpResponse(query)
                print(result3)
                print(query)
            else:
                print("error at inserting in tracking,tracking_update")
           

            template = loader.get_template('home/index.html')
            context = {"tracking_id" : ran, "deleteCookies" : "yes"}
            return HttpResponse(template.render(context, request))
    elif request.method == 'GET':
        return HttpResponse(template.render(context, request))
    return HttpResponse("hello just return")




def confirmation(request):
    template = loader.get_template('home/confirmation.html')
    conn = pymysql.connect(host='localhost', port=3306, user=dbuser, passwd=dbpswd, db='grocery_store')
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
        conn = pymysql.connect(host='localhost', port=3306, user=dbuser, passwd= dbpswd, db='grocery_store')
        cur = conn.cursor()

        # user_filter_choice = request.POST['drop_down_filter']
        # user_search_input = request.POST['search_bar']
        user_filter_choice = request.GET.get('drop_down_filter', "Categories")
        user_search_input = request.GET.get('search_bar', "")
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
            if(row[4] > 0):
                item = {"itemID": str(row[0]),"name": str(row[1]), "weight": str(row[2]), "cost": str(row[3]), "quantity": str(row[4]), "tags": str(row[5]), "image": str(row[6]), "description": str(row[7])}
                items.append(item)

        if(actual_input == ""):
            context = {"items" : items}
        else:
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

#<QueryDict: {' 'name-addr': ['Brian Tan'], 'street-addr': ['4834 Mowry Ave'], 'city-addr': ['Fremont'], 'zip-addr': ['94538'], 'state-addr': ['CA'], 'name-cc': ['Brian Tan'], 'zip-cc': ['94538'], 'number-cc': ['as'], 'ccv-cc': ['asd'], 'update_type': ['update']}>
#

def run_db_query(query):
    conn = pymysql.connect(host='localhost', port=3306, user=dbuser, passwd=dbpswd, db='grocery_store')
    cur = conn.cursor()
    try:
        cur.execute(query)
        conn.commit()
        ret = (1,"success")
        cur.close()
        conn.close()

    except Exception as e:
        ret = (0,e)
    return ret

def select_track_query(query):
    conn = pymysql.connect(host='localhost', port=3306, user=dbuser, passwd=dbpswd, db='grocery_store')
    cur = conn.cursor()
    try:
        cur.execute(query)
        
        ret = (1,"success")
        result = []

        for r in cur:
            print(r[0])
            result.append(r[0])
        ret = ("1",result)
        cur.close()
        conn.close()

    except Exception as e:
        ret = (0,e)
    return ret

def select_db_query(query):
    conn = pymysql.connect(host='localhost', port=3306, user=dbuser, passwd=dbpswd, db='grocery_store')
    cur = conn.cursor()
    try:
        cur.execute(query)
        
        ret = (1,"success")
        result = ""

        for r in cur:
            result = r
        ret = ("1",result)
        cur.close()
        conn.close()

    except Exception as e:
        ret = (0,e)
    return ret



def profile(request):
    if request.method == 'POST':
        if (request.POST['update_type'] == "update"):
            name = request.POST['name-addr']
            street = request.POST['street-addr']
            city = request.POST['city-addr']
            zipcode = request.POST['zip-addr']
            state = request.POST['state-addr']
            c_name = request.POST['name-cc']
            c_name = "'" + c_name+ "'"
            c_zipcode = request.POST['zip-cc']
            c_zipcode = "'" + c_zipcode+ "'"
            
            c_cardnumber = request.POST['number-cc']
            c_cardnumber = "'" + c_cardnumber+ "'"

            c_csv = request.POST['ccv-cc']
            user_id = request.POST['user_id']
            Expiration_Date = request.POST['exp-cc']

            string = name +" , "+ street +" , "+ city +" , "+ zipcode +" , "+ state +" , "+ c_name +" , "+ c_zipcode +" , "+ c_cardnumber +" , "+ c_csv +" , "+ user_id
            address = street +" , "+ city +" , "+ zipcode +" , "+ state
            
            query = 'select * from user_profile where user_id = "' + user_id + '"'

            select_result = select_db_query(query)

            if(select_result[0] == "1" and select_result[1] != "" ):

                query = 'UPDATE `grocery_store`.`user_profile` SET `address`="' + address + '" WHERE `user_id`="' + user_id + '"'
                result = run_db_query(query) 
                
            else:
                query = 'INSERT INTO `grocery_store`.`UserAddress` (`UserID`,`Address`) VALUES ("' + user_id + '","' + address + '")'
                result = run_db_query(query) 
                if(result[0] == 1):
                    print(query)
                    pass
                else:
                    return HttpResponse(result[1])

            query = 'select * from Payments where UserID = "' + user_id + '"'

            select_result = select_db_query(query)

            if(select_result[0] == "1" and select_result[1] != "" ):

                query = 'UPDATE `grocery_store`.`Payments` SET `Credit_Card_Number`="' + c_cardnumber + '", `CSV`="' + c_csv + '",`Expiration_Date`="' + Expiration_Date + '",`Name_on_Card`="' + c_name + '",`Card_Zipcode`="' + c_zipcode + '"  WHERE `UserID`="' + user_id + '"'
            
                result = run_db_query(query)
                print(query) 
                
            else:
                query = "INSERT INTO Payments (PaymentID,UserID,Credit_Card_Number, CSV, Expiration_Date, Name_on_Card, Card_Zipcode) VALUES (" + user_id + ", " + user_id + ", "+ c_cardnumber + ", " + c_csv+ ", " + Expiration_Date + ", " + c_name + ", " + c_zipcode + ")"
                
                result = run_db_query(query) 
                if(result[0] == 1):
                    print(query)
                    pass
                else:
                    print(query)
                    return HttpResponse(result[1])

           



    template = loader.get_template('home/profile.html')
    context = {}
    return HttpResponse(template.render(context, request))



# Create your views here.
