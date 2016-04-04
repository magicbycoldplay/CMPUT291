import sys
import bsddb3 as bsddb

def main():
    
    btreedb = "tmp/schraa/project2.db"
    hashdb = "tmp/schraa/hash.db"
    indexdb = "tmp/schraa/index.db"
    indexdb2 = "tmp/schraa/index2.db"
    DB_SIZE = 1000
    SEED = 10000000
    
    while(setup(sys.argv[1]) == False):
        print("Not a correct DB type Try Again")
        exit()
    populate(sys.argv[1])
    print("Finshed")
    return

def get_random():
    return random.randint(0, 63)
def get_random_char():
    return chr(97 + random.randint(0, 25))
    
def setup(DBtype):
    if DBtype == "btree":
        print("BTREE")
        try:
            db = bsddb.btopen(btreedb, 'w')
        except:
            db = bsddb.btopen(btreede, 'c')
        return True
    elif DBtype == "hash":
        print("HASH")
        try:
            db = bsddb.hashopen(hashdb, 'w')
        except:
            db = bsddb.hashopen(hashdb, 'c')
        return True
    elif DBtype == "indexfile":
        print("INDEXFILE")
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
      
    return

def populate(DBtype):
    #code from the sample python3 program on eclass
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
        key = key.encode(encoding = "UTF-8")
        value = value.encode(encoding="UTF-8")
        db[key] = value
        if DBtype == 'indexfile':
            db2[value] = key
    return

def get():
    cur = db.cursor()
    iter = cur.first()
    while iter:
        print(iter[0].decode("utf-8"))
        print(iter[1].decode("utf-8"))
        iter = cur.next()
    print("------------------------")
    try:
        db.close()
    except Exception as e:
        print (e)    
    
    
if __name__ == "__main__":
        main()    
