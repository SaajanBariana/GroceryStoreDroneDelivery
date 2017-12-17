query = "UPDATE grocery_store.items " + \
                    "SET name = '" + 'Apple' + "' , weight = " + "3" + \
                    " , cost = "+ "3" + \
                    " , quantity = " + "4" + \
                    " , categories = '" + "hello" + \
                    "' , image = '" + "aURL" + \
                    "' , description = '" + "hi" + \
                    "' WHERE itemID = " + '1' + ";"
print(query)