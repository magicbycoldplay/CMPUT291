import time
import datetime
import os
import bsddb3 as bsddb
import random
import sys
import getopt
import shutil

def main():
    try:
        os.mkdir("/tmp/schraa")
        print("Folder")
    except:
        pass   
    
    while(setup(sys.argv[1]) == False):
        print("Not a correct DB type Try Again")
        exit()
    populate(sys.argv[1])
    get()
    print("Finshed")
    return

def get_random():
    return random.randint(0, 63)
def get_random_char():
    return chr(97 + random.randint(0, 25))
    
def setup(DBtype):
    data = bsddb.db.DB()
    btreedb = "/tmp/schraa/btree.db"
    hashdb = "/tmp/schraa/hash.db"
    indexdb = "/tmp/schraa/index.db"
    indexdb2 = "/tmp/schraa/index2.db" 
    
    if DBtype == "btree":
        print("BTREE")
        try:
            data.open(btreedb ,None, db.DB_BTREE, db.DB_CREATE)
            print("PASS")
        except:
            print("FAIL")
        return True
    elif DBtype == "hash":
        print("HASH")
        try:
            data = bsddb.hashopen(hashdb, 'w')
        except:
            data = bsddb.hashopen(hashdb, 'c')
        return True
    elif DBtype == "indexfile":
        print("INDEXFILE")
        try:
            data = bsddb.btopen(indexdb, 'w')
            data2 = bsddb.db.DB()
            data2.open(indexdb2, None, bsddb.db.DB_BTREE, bsddb.db.DB_CREATE)
        except:
            data = bsddb.btopen(indexdb, 'c')
            data2 = bsddb.db.DB()
            data2.open(indexdb2, None, bsddb.db.DB_BTREE, bsddb.db.DB_CREATE)            
        return True
    else:
        return False
      
    return

def populate(DBtype):
    DB_SIZE = 1000
    SEED = 10000000 
    random.seed(SEED)
    #code from the sample python3 program on eclass
    for index in range(DB_SIZE):
        krng = 64 + get_random()
        key = ""
        while True:
            for i in range(krng):
                key += str(get_random_char())
            if(data.has_key(key.encode()) == False):
                break
            else:
                key = ""
        vrng = 64 + get_random()
        value = ""
        for i in range(vrng):
            value += str(get_random_char())
        key = key.encode(encoding = "UTF-8")
        value = value.encode(encoding="UTF-8")
        data[key] = value
        if DBtype == 'indexfile':
            data2[value] = key
    return

def get():
    cur = data.cursor()
    iter = cur.first()
    while iter:
        print(iter[0].decode("utf-8"))
        print(iter[1].decode("utf-8"))
        iter = cur.next()
    print("------------------------")
    try:
        data.close()
    except Exception as e:
        print (e)    
    
    
if __name__ == "__main__":
        main()    
