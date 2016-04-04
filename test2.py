import time
import datetime
import os
import bsddb3 as bsddb
import random
import sys
import getopt
import shutil

DA_FILE = "/tmp/hpabst_db/projdatabase.db"
DB_SIZE = 100000
SEED = 10000000
typeOption = ""    #This will be gotten from command line and determine if we're making
                   #a hash db, a B+tree db, or a indexfile db.

db = ""            #This will be the database object.
db2 = ""           #Used for IndexFile.
dbPopFlag = False  #Flag variable so we don't overpopulate the database.
answerFile = ""

def get_random():
    return random.randint(0, 63)
def get_random_char():
    return chr(97 + random.randint(0, 25))

def main():
    typeOptionCheck()
    fileSetup()
    print("Welcome to our database application.")
    menuMessage()
    while(True):
        userIn = input("> ")
        if(userIn == '1'):
            #Creating and populating the database.
            populateDatabase()
            menuMessage()
        elif(userIn == '2'):
            #Retrieving records with a given key.
            keySearch()
            menuMessage()
        elif(userIn == '3'):
            #Retrieving records with given data.
            dataSearch()
            menuMessage()
        elif(userIn == '4'):
            #Retrieving data in a range of keys.
            rangeSearch()
            menuMessage()
        elif(userIn == '5'):
            #Destroying the database.
            destroyDatabase()
            menuMessage()
        elif(userIn == '6'):
            quit()
            menuMessage()
        else:
            print("I'm sorry, I did not understand your command.")

def menuMessage():
    print("----------------------------------------")
    print("Enter '1' to create and populate the database.")
    print("Enter '2' to retrieve records with a given key.")
    print("Enter '3' to retrieve records with given data.")
    print("Enter '4' to retrieve records in a given range of keys.")
    print("Enter '5' to destroy the database.")
    print("Enter '6' to quit.")

# Retrieve records with a given key
def keySearch():
    global db
    data = list()
    key = input("Please enter the key to retrieve data for: ")
    keyencode = key.encode(encoding="UTF-8")
    start = datetime.datetime.now()
    try:
        data.append(db[keyencode])
        records = 1
    except:
        records = 0
    end = datetime.datetime.now()
    msdelta = end.microsecond-start.microsecond
    print("Number of records:", records)
    print("Execution time: " + str(msdelta) + " microseconds.")
    for datum in data:
        answerFile.write(key+"\n")
        answerFile.write(datum.decode()+"\n")
        answerFile.write("\n")
        answerFile.flush()
    return

# Retrieve records with a given data
def dataSearch():
    global db
    global db2
    global typeOption
    global answerFile
    data = list()
    searchIn = input("Please enter the data to search for: ")
    search = searchIn.encode(encoding="UTF-8")
    if(typeOption != "indexfile"):
        start = datetime.datetime.now()
        for key, value in db.iteritems():
            if value == search:
                data.append(key)
        end = datetime.datetime.now()
        msdelta = end.microsecond-start.microsecond
        print("Number of records: ", str(len(data)))
        print("Execution time: " + str(msdelta) + " microseconds.")
        for datum in data:
            answerFile.write(datum.decode()+"\n")
            answerFile.write(searchIn+"\n")
            answerFile.write("\n")
            answerFile.flush()
    elif(typeOption == "indexfile"):
        start = datetime.datetime.now()
        cursor = db2.cursor()
        nextValue = cursor.set(search)[0] 
        data.append(nextValue)
        while nextValue:
            nextValue = cursor.next_dup()
            if nextValue:
                data.append(nextValue[0])
        end = datetime.datetime.now()
        msdelta = end.microsecond-start.microsecond
        print("Number of records:", str(len(data)))
        print("Execution time: " + str(msdelta) + " microseconds.")
        for datum in data:
            answerFile.write(db2[datum].decode()+"\n")
            answerFile.write(searchIn+"\n")
            answerFile.write("\n")
            answerFile.flush()
    return

# Retrieve records with a given range of key values
def rangeSearch():
    global db
    global typeOption
    data = list()
    lowerIn = input("Please enter the lower bound of the range: ")
    lower = lowerIn.encode(encoding="UTF-8")
    upperIn = input("Please enter the upper bound of the range: ")
    upper = upperIn.encode(encoding="UTF-8")
    if lower <= upper:
        if typeOption != "hash":
            # Fast Btree Range Search
            start = datetime.datetime.now()
            try:
                lowestKey = db.set_location(lower)[0]
                data.append(lowestKey)
                while True:
                    key = db.next()[0]
                    if key <= upper:
                        data.append(key)
                    else:
                        break
                end = datetime.datetime.now()
                msdelta = end.microsecond-start.microsecond
                print("Number of records: ", str(len(data)))
                print("Execution time: " + str(msdelta) + " microseconds.")
            except:
                end = datetime.datetime.now()
                msdelta = end.microsecond-start.microsecond
                print("Number of records: 0")
                print("Execution time: " + str(msdelta) + " microseconds.")
        else:
            # Sequential Range Search
            start = datetime.datetime.now()
            for key, value in db.iteritems():
                if key >= lower and key <= upper:
                    data.append(key)
            end = datetime.datetime.now()
            msdelta = end.microsecond-start.microsecond
            print("Number of records: ", str(len(data)))
            print("Execution time: " + str(msdelta) + " microseconds.")

        for datum in data:
            answerFile.write(datum.decode()+"\n")
            answerFile.write(db[datum].decode()+"\n")
            answerFile.write("\n")
            answerFile.flush()
    else:
        print("Number of records: 0")
        print("Lower Bound is higher than the Upper Bound")
    return

# Store command line argument in typeOption
def typeOptionCheck():
    global typeOption
    try:
        option = getopt.getopt(sys.argv[1], "")[1]
        print("Database type you specified:", option)
        if option == "btree" or option == "hash" or option == "indexfile":
            typeOption = option
        else:
            print("Error: Invalid Database Type")
            sys.exit()
    except:
            print("Error: No Database Type specified")
            sys.exit()

# Create and populate the database
def populateDatabase():
    global typeOption
    global db
    global db2
    global dbPopFlag
    if(dbPopFlag == True):
        print("Error: database already populated, returning to menu.")
        return
    if(typeOption == "btree"):
        try:
            db = bsddb.btopen(DA_FILE, 'w')
        except:
            print("Error: Database does not exist, creating one.")
            db = bsddb.btopen(DA_FILE, 'c')
    elif(typeOption == "hash"):
        try:
            db = bsddb.hashopen("/tmp/hpabst_db/hashdb.db", "w")           
        except:
            print("Error: Database does not exist, creating one.")
            db = bsddb.hashopen("/tmp/hpabst_db/hashdb.db", "c")
    elif(typeOption == "indexfile"):
        try:
            db = bsddb.btopen("/tmp/hpabst_db/indexdb1.db", "w")
            db2 = bsddb.db.DB()
            db2.open("/tmp/hpabst_db/indexdb2.db", None, bsddb.db.DB_BTREE, bsddb.db.DB_CREATE)
        except:
            print("Error: Database does not exist, creating one.")
            db = bsddb.btopen("/tmp/hpabst_db/indexdb1.db", "c")
            db2 = bsddb.db.DB()
            db2.open("/tmp/hpabst_db/indexdb2.db", None, bsddb.db.DB_BTREE, bsddb.db.DB_CREATE)
    random.seed(SEED)

    print("Populating the database...")
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
        if typeOption == "indexfile":
            db2[value] = key
        # Tracking Database Population Progress
        print('\b\b\b'+str(int((index/DB_SIZE)*100))+"%",end="")
    dbPopFlag = True
    print('\b\b\b\b', end="")
    print("100%\nDatabase population complete.")

def indexFunc(primarykey, primarydata):
    return primarydata


def destroyDatabase2():
    global DA_FILE
    global db
    global typeOption
    global dbPopFlag
    if dbPopFlag:
        db.close()
        if db2 != "":
            db2.close()
        try:
            os.remove(DA_FILE)
        except Exception as e:
            pass
        try:
            os.remove("/tmp/hpabst_db/hashdb.db")
        except Exception as e:
            pass
        try:
            os.remove("/tmp/hpabst_db/recorddb.db")
        except Exception as e:
            pass
        try:
            os.remove("/tmp/hpabst_db/indexdb.db")
            os.remove("/tmp/hpabst_db/indexdb2.db")
        except Exception as e:
            pass
        print("Database was successfully destroyed")
        dbPopFlag = False
    else:
        print("There are no databases to destroy")


def quit():
    global db
    global db2
    if dbPopFlag:
        db.close()
        if db2 != "":
            db2.close()
         
    answerFile.close()
    try:
        os.remove(DA_FILE)
    except Exception as e:
        pass
    try:
        os.remove("/tmp/hpabst_db/hashdb.db")
    except Exception as e:
        pass
    try:
        os.remove("/tmp/hpabst_db/recorddb.db")
    except Exception as e:
        pass
    try:
        os.remove("/tmp/hpabst_db/indexdb.db")
        os.remove("/tmp/hpabst_db/indexdb2.db")
    except Exception as e:
        pass
    try:
        shutil.rmtree("/tmp/hpabst_db")
    except OSError as oserr:
        print("Folder '/tmp/hpabst_db' was already removed")
    print("Goodbye.")
    sys.exit()
    
def fileSetup():
    global answerFile
    try:
        os.stat("/tmp/hpabst_db")
    except:
        os.mkdir("/tmp/hpabst_db")
        print("Folder '/tmp/hpabst_db' was created") 
    try:
        answerFile = open("answers", "w")
    except:
        print("Error in opening answer file.")

if __name__ == "__main__":
    main()
