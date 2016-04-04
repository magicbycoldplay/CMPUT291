import time
import datetime
import os
import random
import sys
import getopt
import shutil
import bsddb3 as bsddb



def main():
      
    
    try:
        os.stat("/tmp/schraa")
        print("Folder there")
    except:
        os.mkdir("/tmp/schraa")
        print("Folder created")
        
    while(setup(sys.argv[1]) == False):
        print("Not a correct DB type Try Again")
        exit()
        
    fill(sys.argv[1])
    
    print("DONE")
        
def setup(dbtype):
    global db
    global db2
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
    print("Populating the database...")
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
        # Tracking Database Population Progress
        print('\b\b\b'+str(int((index/DB_SIZE)*100))+"%",end="")
    dbPopFlag = True
    print('\b\b\b\b', end="")
    print("100%\nDatabase population complete.") 
    return

def get_random():
    return random.randint(0, 63)
def get_random_char():
    return chr(97 + random.randint(0, 25))

if __name__ == "__main__":
        main()    
