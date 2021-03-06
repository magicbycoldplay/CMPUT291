import time
import datetime
import os
import random
import sys
import getopt
import shutil
import bsddb3 as bsddb

def main():
    global db
    global db2
    global bteedb
    global hashdb
    global indexdb
    global indexdb2 
    global answerFile
    
    try:
        os.stat("/tmp/schraa")
    except:
        os.mkdir("/tmp/schraa")
    
    try:
        answerFile = open("answers", "w")
    except:
        print("Error")
        
    while(setup(sys.argv[1]) == False):
        print("Not a correct DB type Try Again")
        exit()
    
    menu()
    while(True):
        userIn = input("Choose an option: ")
        if(userIn == '1'):
            #Creating and populating the database.
            fill(sys.argv[1])
            menu()
        elif(userIn == '2'):
            #Retrieving records with a given key.
            key_search()
            menu()
        elif(userIn == '3'):
            #Retrieving records with given data.
            data_search()
            menu()
        elif(userIn == '4'):
            #Retrieving data in a range of keys
            if (sys.argv[1] == "hash"):
                rangeHash()
            else:
                rangeBtree()
            menu()
        elif(userIn == '5'):
            #Destroying the database.
            destroyDB(False)
            menu()
        elif(userIn == '6'):
            destroyDB(True)
            exit()
        else:
            print("I'm sorry, I did not understand your command.")    
    
    print("DONE")
    
def rangeHash():
    print("HELLLLLLO")
    global answerFile
    lower = input("Enter the lower bound: ")
    uppper = input("Enter the uppper bound: ")
    elower = lower.encode(encoding = "UTF-8")
    eupper = uppper.encode(encoding = "UTF-8")
    records = 1
    if elower > eupper:
        print("Lower greater than upper try again")
        return 
    else:
        searchResults = list()
        begin = datetime.datetime.now()
        #sequential hash search
        for ekey, evalue in db.iteritems():
            if (ekey > elower and ekey < eupper):
                searchResults.append(ekey)
                records += 1
        finish = datetime.datetime.now()
        exectime = finish.microsecond-begin.microsecond
        print("Number of records retrieved: ", records)
        print("It took " + str(exectime) + " microseconds to finish.")  
        
        #write data to a file
        answerFile.write("RANGE RESULTS")
        answerFile.write("\n")
        for data in searchResults:  
            answerFile.write(db[data].decode() + "\n")
            answerFile.write(data.decode() + "\n")
            answerFile.write("-----------------------" + "\n")
            answerFile.flush()
        return        

    
def rangeBtree():
    global answerFile
    lower = input("Enter the lower bound: ")
    uppper = input("Enter the uppper bound: ")
    elower = lower.encode(encoding = "UTF-8")
    eupper = uppper.encode(encoding = "UTF-8")
    if elower > eupper:
        print("Lower greater than upper try again")
        return
    else:
        #start at the bottom and append all data till you get to the top
        begin = datetime.datetime.now()
        lowKey = db.set_location(elower)[0]
        searchResults = list()
        searchResults.append(lowKey)
        records = 1
        while(db.next()[0] <= eupper):
            searchResults.append(db.next()[0])
            records += 1
        finish = datetime.datetime.now()
        exectime = finish.microsecond-begin.microsecond
        print("Number of records retrieved: ", records)
        print("It took " + str(exectime) + " microseconds to finish.")
        
        #write data to a file
        answerFile.write("RANGE RESULTS")
        answerFile.write("\n")
        for data in searchResults:  
            answerFile.write(db[data].decode() + "\n")
            answerFile.write(data.decode() + "\n")
            answerFile.write("-----------------------" + "\n")
            answerFile.flush()
        return
    
    
def destroyDB(quit):
    global db
    global db2
    global bteedb
    global hashdb
    global indexdb
    global indexdb2     
    try:
        os.remove(btreedb)
    except:
        pass
    
    try:
        os.remove(hashdb)
    except:
        pass
    
    try:
        os.remove(indexdb)
        os.remove(indexdb2)
    except:
        pass
    
    if (quit == True):
        try: 
            shutil.rmtree("/tmp/schraa")
        except:
            pass
        print("DONE")
        exit()
    else:
        print("DESTROYED")
    
        
def setup(dbtype):
    global db
    global db2
    global bteedb
    global hashdb
    global indexdb
    global indexdb2    
    
    btreedb = "/tmp/schraa/btree.db"
    hashdb = "/tmp/schraa/hashdb.db"
    indexdb = "/tmp/schraa/indexdb1.db"
    indexdb2 = "/tmp/schraa/index2.db"   
    print('')
    if (dbtype == "btree"):
        try:
            db = bsddb.btopen(btreedb, 'w')
        except:
            db = bssdb.btopen(btreedb, 'c')
        return True
    elif (dbtype == "hash"):
        try:
            db = bsddb.btopen(hashdb, 'w')
        except:
            db = bsddb.btopen(hashdb, 'c')
        return True
    elif (dbtype == "indexfile"):
        try:
            db = bsddb.btopen(indexdb, 'w')
            db2 = bsddb.db.DB()
            db2.open(indexdb2, None, bsddb.db.DB_BTREE, bsddb.db.DB_CREATE)
        except:
            db = bsddb.btopen(indexdb, 'c')
            db2 = bsddb.db.DB()
            db2.open(indexdb2, None, bsddb.db.DB_BTREE, bsddb.db.DB_CREATE)
        return True
    else:
        return False
       
def fill(dbtype):

    DB_SIZE = 100000
    SEED = 10000000 
    random.seed(SEED)
    #code taken from example python3 on eclass
    for index in range(DB_SIZE):
        krng = 64 + get_random()
        key = ""
        while True:
            for i in range(krng):
                key += str(get_random_char())
            if(db.has_key(key.encode()) == False):
                break
            else:
                key = ""
        vrng = 64 + get_random()
        value = ""
        for i in range(vrng):
            value += str(get_random_char())
        key = key.encode(encoding="UTF-8")
        value = value.encode(encoding="UTF-8")
        db[key] = value
        if (dbtype == "indexfile"):
            db2[value] = key
    print("Database Full") 
    return

def menu():
    print("*********************************************************")
    print("Enter [1] to create and populate the database")
    print("Enter [2] to retrieve records with a given key")
    print("Enter [3] to retrieve records with given data")
    print("Enter [4] to retrieve records in a given range of keys")
    print("Enter [5] to destroy the database")
    print("Enter [6] to quit")
    
def key_search():
    global db
    global answerFile
    data = list()
    key = input("Enter a key: ")
    ekey = key.encode(encoding = "UTF-8")
    begin = datetime.datetime.now()
    try:
        data.append(db[ekey])
        records = 1
    except:
        records = 0
    finish = datetime.datetime.now()
    exectime = finish.microsecond-begin.microsecond
    print("Number of records retrieved: ", records)
    print("It took " + str(exectime) + " microseconds to finish.")
    for pair in data:
        answerFile.write(key + "\n")
        answerFile.write(pair.decode() + "\n" + "\n")
        answerFile.flush()
    return

def data_search():
    global db
    global db2
    global answerFile
    records = 0
    searchInput = input("Enter data to search for: ")
    search = searchInput.encode(encoding = "UTF-8")
    if sys.argv[1] == "indexfile":
        data = ""
        begin = datetime.datetime.now()
        data = db2[searchInput.encode(encoding = "UTF-8")]
        data = data.decode(encoding = "UTF-8")
        finish = datetime.datetime.now()
        exectime = finish.microsecond-begin.microsecond
        if data != "":
            records = records + 1
            print("Number of records retrieved: ", records)
            print("It took " + str(exectime) + " microseconds to finish.")            
            answerFile.write(data + "\n")
            answerFile.write(searchInput + "\n" + "\n")
            answerFile.flush()
        else:
            print("Number of records retrieved: ", records)
            print("It took " + str(exectime) + " microseconds to finish.")            
    elif sys.argv[1] != "indexfile":
        data = list()
        begin = datetime.datetime.now()
        for key, value in db.iteritems():
            if value == search:
                data.append(key)
                records = records + 1
        finish = datetime.datetime.now()
        exectime = finish.microsecond-begin.microsecond
        print("Number of records retrieved: ", records)
        print("It took " + str(exectime) + " microseconds to finish.")
        for pair in data:
            answerFile.write(pair.decode() + "\n")
            answerFile.write(searchInput + "\n" + "\n")
            answerFile.flush()        
    return

def get_random():
    return random.randint(0, 63)
def get_random_char():
    return chr(97 + random.randint(0, 25))

if __name__ == "__main__":
        main()    
