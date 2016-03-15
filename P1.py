#Mini-Project 1

import cx_Oracle
import sys
import getpass
import random
import datetime

def main():

    setup_oracle_connection()
    drop_views_and_tables()
    create_views_and_tables()
    
    while True:
        #Get user to pick an option
        print("--------------------------------------------")
        print("Enter '1' to register a vehicle")
        print("Enter '2' to make an auto transaction")
        print("Enter '3' for register a license")
        print("Enter '4' to record a violation ticket")
        print("Enter '5' to search")
        print("--------------------------------------------")
        option = input('Please pick an option: ')
        if 'q' in option.lower():
            exit()
        else:
            try:
                option = int(option)
            except ValueError as ve:
                pass

        if option == 1:
            #TO DO
            register_vehicle()
        elif option == 2:
            #TO DO
            auto_transaction()
        elif option == 3:
            #TO DO
            register_license()
        elif option == 4:
            #TO DO
            record_violation()
        elif option == 5:
            #TO DO
            search()
        else:
            print("--------------------------------------------")
            print("Enter '1' to register a vehicle")
            print("Enter '2' to make an auto transaction")
            print("Enter '3' for register a license")
            print("Enter '4' to record a violation ticket")
            print("Enter '5' to search")
            print("--------------------------------------------")
            print('Invalid option! Please pick again.')

    return

def create_views_and_tables():
    ''' create all the needed tables and views '''
    # Connect to database
    try:
        connection = cx_Oracle.connect(CONNECT_INFO)
        curs = connection.cursor()
    except cx_Oracle.DatabaseError as exc:
        error, = exc.args
        print(sys.stderr, "Oracle code:", error.code)
        print(sys.stderr, "Oracle message:", error.message)
        return
        
    try:
        curs.execute("""CREATE TABLE people (
                        sin          CHAR(15),  
                        name         VARCHAR(40),
                        height       number(5,2),
                        weight       number(5,2),
                        eyecolor     VARCHAR (10),
                        haircolor    VARCHAR(10),
                        addr         VARCHAR2(50),
                        gender       CHAR,
                        birthday     DATE,
                        PRIMARY KEY (sin),
                        CHECK ( gender IN ('m', 'f') )
                    )""")
        connection.commit()
        curs.execute("""CREATE TABLE drive_licence (
                        licence_no      CHAR(15),
                        sin             char(15),
                        class           VARCHAR(10),
                        photo           BLOB,
                        issuing_date    DATE,
                        expiring_date   DATE,
                        PRIMARY KEY (licence_no),
                        UNIQUE (sin),
                        FOREIGN KEY (sin) REFERENCES people
                        ON DELETE CASCADE
                    )""")
        connection.commit()
        curs.execute("""CREATE TABLE driving_condition (
                        c_id        INTEGER,
                        description VARCHAR(1024),
                        PRIMARY KEY (c_id)
                    )""")
        connection.commit()
        curs.execute("""CREATE TABLE restriction(
                        licence_no   CHAR(15),
                        r_id         INTEGER,
                        PRIMARY KEY (licence_no, r_id),
                        FOREIGN KEY (licence_no) REFERENCES drive_licence,
                        FOREIGN KEY (r_id) REFERENCES driving_condition
                     )""")
        connection.commit()
        curs.execute("""CREATE TABLE vehicle_type (
                        type_id       integer,
                        type          CHAR(10),
                        PRIMARY KEY (type_id)
                     )""")
        connection.commit()
        curs.execute("""CREATE TABLE vehicle (
                        serial_no    CHAR(15),
                        maker        VARCHAR(20),	
                        model        VARCHAR(20),
                        year         number(4,0),
                        color        VARCHAR(10),
                        type_id      integer,
                        PRIMARY KEY (serial_no),
                        FOREIGN KEY (type_id) REFERENCES vehicle_type
                     )""")
        connection.commit()
        curs.execute("""CREATE TABLE owner (
                        owner_id          CHAR(15),
                        vehicle_id        CHAR(15),
                        is_primary_owner  CHAR(1),
                        PRIMARY KEY (owner_id, vehicle_id),
                        FOREIGN KEY (owner_id) REFERENCES people,
                        FOREIGN KEY (vehicle_id) REFERENCES vehicle,
                        CHECK ( is_primary_owner IN ('y', 'n'))
                     )""")
        connection.commit()
        curs.execute("""CREATE TABLE auto_sale (
                        transaction_id  int,
                        seller_id   CHAR(15),
                        buyer_id    CHAR(15),
                        vehicle_id  CHAR(15),
                        s_date      date,
                        price       numeric(9,2),
                        PRIMARY KEY (transaction_id),
                        FOREIGN KEY (seller_id) REFERENCES people,
                        FOREIGN KEY (buyer_id) REFERENCES people,
                        FOREIGN KEY (vehicle_id) REFERENCES vehicle
                     )""")
        connection.commit()
        curs.execute("""CREATE TABLE ticket_type (
                        vtype     CHAR(10),
                        fine      number(5,2),
                        PRIMARY KEY (vtype)
                     )""")
        connection.commit()
        curs.execute("""CREATE TABLE ticket (
                        ticket_no     int,
                        violator_no   CHAR(15),  
                        vehicle_id    CHAR(15),
                        office_no     CHAR(15),
                        vtype        char(10),
                        vdate        date,
                        place        varchar(20),
                        descriptions varchar(1024),
                        PRIMARY KEY (ticket_no),
                        FOREIGN KEY (vtype) REFERENCES ticket_type,
                        FOREIGN KEY (violator_no) REFERENCES people ON DELETE CASCADE,
                        FOREIGN KEY (vehicle_id)  REFERENCES vehicle,
                        FOREIGN KEY (office_no) REFERENCES people ON DELETE CASCADE
                     )""")
        connection.commit()
        
        testfile = open("a2-data.txt","r")
        for line in testfile:
            curs.execute(line)
        connection.commit()
        
    except cx_Oracle.DatabaseError as exc:
        error, = exc.args
        print(sys.stderr, "Oracle code:", error.code)
        print(sys.stderr, "Oracle message:", error.message)
        
    # Close connection
    try:
        curs.close()
        connection.close()
    except cx_Oracle.DatabaseError as exc:
        error, = exc.args
        print(sys.stderr, "Oracle code:", error.code)
        print(sys.stderr, "Oracle message:", error.message)
        return
        
    return

def drop_views_and_tables():
    ''' drop all existing views and tables '''
    # Connect to database
    try:
        connection = cx_Oracle.connect(CONNECT_INFO)
        curs = connection.cursor()
    except cx_Oracle.DatabaseError as exc:
        error, = exc.args
        print(sys.stderr, "Oracle code:", error.code)
        print(sys.stderr, "Oracle message:", error.message)
        return

    try:
        curs.execute("DROP TABLE owner")
    except cx_Oracle.DatabaseError as exc:
        pass
    try:
        curs.execute("DROP TABLE auto_sale")
    except cx_Oracle.DatabaseError as exc:
        pass
    try:
        curs.execute("DROP TABLE restriction")
    except cx_Oracle.DatabaseError as exc:
        pass
    try:
        curs.execute("DROP TABLE driving_condition")
    except cx_Oracle.DatabaseError as exc:
        pass
    try:
        curs.execute("DROP TABLE ticket")
    except cx_Oracle.DatabaseError as exc:
        pass
    try:
        curs.execute("DROP TABLE ticket_type")
    except cx_Oracle.DatabaseError as exc:
        pass
    try:
        curs.execute("DROP TABLE vehicle")
    except cx_Oracle.DatabaseError as exc:
        pass
    try:
        curs.execute("DROP TABLE vehicle_type")
    except cx_Oracle.DatabaseError as exc:
        pass
    try:
        curs.execute("DROP TABLE drive_licence")
    except cx_Oracle.DatabaseError as exc:
        pass
    try:
        curs.execute("DROP TABLE people")
    except cx_Oracle.DatabaseError as exc:
        pass


    # Commit changes, close connection
    try:
        connection.commit()
        curs.close()
        connection.close()
    except cx_Oracle.DatabaseError as exc:
        error, = exc.args
        print(sys.stderr, "Oracle code:", error.code)
        print(sys.stderr, "Oracle message:", error.message)
        return
        
    return


def setup_oracle_connection():
    ''' Get oracle connection from user and try to connect to DB '''
    global ORACLE_USER
    global ORACLE_PSWD
    global CONNECT_INFO

    while True:
        # Get account info from user
        #ORACLE_USER = input('Enter oracle user name: ')
        #ORACLE_PSWD = getpass.getpass('Enter oracle password: ')
        ORACLE_USER = 'schraa'
        ORACLE_PSWD = 'Monkeybolt1'
        CONNECT_INFO = '{0}/{1}@gwynne.cs.ualberta.ca:1521/CRS'.format(ORACLE_USER, ORACLE_PSWD)
        
        # Connect to database
        try:
            connection = cx_Oracle.connect(CONNECT_INFO)
            curs = connection.cursor()
            break
        except cx_Oracle.DatabaseError as exc:
            error, = exc.args
            print(sys.stderr, "Oracle code:", error.code)
            print(sys.stderr, "Oracle message:", error.message)

    # Close connection
    try:
        curs.close()
        connection.close()
    except cx_Oracle.DatabaseError as exc:
        error, = exc.args
        print(sys.stderr, "Oracle code:", error.code)
        print(sys.stderr, "Oracle message:", error.message)
        return

    return


def auto_transaction():
    # Connect to database
    try:
        connection = cx_Oracle.connect(CONNECT_INFO)
        curs = connection.cursor()
    except cx_Oracle.DatabaseError as exception:
        error = exception.args
        print(sys.stderr, "Oracle code: ", error.code)
        print(sys.stderr, "Oracle message: ", error.message)
        return

    valid = False
    while not valid: 
        #get transaction id
        t_id = input ('Enter transaction ID: ')
        if t_id == 'q':
            exit()
        #check to see if transaction number already in the database
        try:
            curs.execute("SELECT transaction_id FROM auto_sale WHERE transaction_id = '{0}'".format(int(t_id)))
            result = curs.fetchall()
        except cx_Oracle.DatabaseError as exception:
            error = exception.args
            print(sys.stderr, "Oracle code: ", error.code)
            print(sys.stderr, "Oracle message: ", error.message)
            return    
        if result:
            print('Auto sale already registered, try again')
            
        else:
            #Have the user enter the sale information
            #Enter the seller information ------------------------------- SELLER
            s_answer = input('Is the seller in the system (y/n): ').strip().lower()
            skip = False
            if s_answer == 'y':
                seller_id = input('Please enter the seller SIN: ').strip()
                if seller_id == 'q':
                    exit()
                #check to make sure the seller is in the system
                try:
                    curs.execute("SELECT sin FROM people WHERE sin = '{0}'".format(seller_id))
                    seller_result = curs.fetchall()
                except cx_Oracle.DatabaseError as exception:
                    error = exception.args
                    print(sys.stderr, "Oracle code: ", error.code)
                    print(sys.stderr, "Oracle message: ", error.message)
                    return     
                if seller_result:
                    #seller in the system
                    print("seller in the system")
                    print('')
                    skip = True
                else:
                    #seller not in the system
                    print("seller NOT in the system, please enter them now")
            #enter seller into system
            if not skip:
                sin = input('Please enter the seller SIN: ')
                name = input('Please enter the seller name: ')
                height = input('Please enter the seller height: ')
                weight = input('Please enter the seller weight: ')
                eyecolor = input('Please enter the seller eyecolor: ')
                haircolor = input('Please enter the seller haircolor: ')
                addr = input('Please enter the seller address: ')
                gender = input('Please enter the seller gender (m/f): ')
                birthday = input('Please enter the seller birthday (YYYY-MM-DD): ')
                print('')
                
                try:
                    curs.execute("INSERT INTO people VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}', date '{8}')"
                                 .format(sin,name,int(height),int(weight),
                                         eyecolor,haircolor,addr,gender,birthday))
                    connection.commit()
                except cx_Oracle.DatabaseError as exception:
                    error = exception.args
                    print(sys.stderr, "Oracle code: ", error.code)
                    print(sys.stderr, "Oracle message: ", error.message)
                    return                    
            
            #enter buyer information ------------------------------------- BUYER
            s_answer = input('Is the buyer in the system (y/n): ').strip().lower()
            skip = False
            if s_answer == 'y':
                buyer_id = input('Please enter the buyer SIN: ').strip()
                if buyer_id == 'q':
                    exit()
                #check to make sure the buyer is in the system
                try:
                    curs.execute("SELECT sin FROM people WHERE sin = '{0}'".format(buyer_id))
                    buyer_result = curs.fetchall()
                except cx_Oracle.DatabaseError as exception:
                    error = exception.args
                    print(sys.stderr, "Oracle code: ", error.code)
                    print(sys.stderr, "Oracle message: ", error.message)
                    return     
                if buyer_result:
                    #buyer in the system
                    print("buyer in the system")
                    print('')
                    skip = True
                else:
                    #buyer not in the system
                    print("buyer NOT in the system, please enter them now")
            #enter buyer into system
            if not skip:
                sin = input('Please enter the buyer SIN: ')
                name = input('Please enter the buyer name: ')
                height = input('Please enter the buyer height: ')
                weight = input('Please enter the buyer weight: ')
                eyecolor = input('Please enter the buyer eyecolor: ')
                haircolor = input('Please enter the buyer haircolor: ')
                addr = input('Please enter the buyer address: ')
                gender = input('Please enter the buyer gender (m/f): ')
                birthday = input('Please enter the buyer birthday (YYYY-MM-DD): ')
                print('')
                
                try:
                    curs.execute("INSERT INTO people VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}', date '{8}')"
                                 .format(sin,name,int(height),int(weight),eyecolor,haircolor,addr,gender,birthday))
                    connection.commit()
                except cx_Oracle.DatabaseError as exception:
                    error = exception.args
                    print(sys.stderr, "Oracle code: ", error.code)
                    print(sys.stderr, "Oracle message: ", error.message)
                    return   
                
            #enter vehicle into system --------------------------------- VEHICLE           
            s_answer = input('Is the vehicle in the system (y/n): ').strip().lower()
            skip = False
            if s_answer == 'y':            
                vehicle_id = input('Please enter the serial number of the vehicle: ').strip()
                if vehicle_id == 'q':
                    exit()
                try:
                    curs.execute("SELECT serial_no FROM vehicle WHERE serial_no = '{0}'".format(vehicle_id))
                    vehicle_result = curs.fetchall()
                except cx_Oracle.DatabaseError as exception:
                    error = exception.args
                    print(sys.stderr, "Oracle code: ", error.code)
                    print(sys.stderr, "Oracle message: ", error.message)
                    return   
                if vehicle_result:
                    #vehicle in the system
                    print("vehicle in the system")
                    skip = True
                    print('')
                else:
                    #vehicle not in the system
                    print('Vehicle not in system, please enter it now')
            if not skip:
                try:
                    vehicle_id = input('Please enter the serial number of the vehicle: ').strip()
                    maker = input('Please enter the maker of the vehicle: ').strip()
                    model = input('Please enter the model of the vehicle: ').strip()
                    year = input('Please enter the year of the vehicle: ').strip()
                    color = input('Please enter the colour of the vehicle: ').strip()
                    type_id = input('Please enter the type ID of the vehicle: ').strip()
                    
                    curs.execute("INSERT INTO vehicle VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}')"
                                    .format(vehicle_id, maker, model, int(year), color, int(type_id)))
                    connection.commit()
                except cx_Oracle.DatabaseError as exception:
                    error = exception.args
                    print(sys.stderr, "Oracle code: ", error.code)
                    print(sys.stderr, "Oracle message: ", error.message)
                    return
            
            #enter date --------------------------------------------------- DATE 
            print('')
            s_date = input('Please enter the date of sale transaction (YYYY-MM-DD): ').strip()
            #enter price ------------------------------------------------- PRICE
            print('')
            price = input('Please enter the price: ').strip()
            
            valid = True
     
    #close connection        
    try:
        curs.close()
        connection.close()
    except cx_Oracle.DatabaseError as exception:
        error = exception.args
        print(sys.stderr, "Oracle code: ", error.code)
        print(sys.stderr, "Oracle message: ", error.message)
        return    
                
    return
                
                

def register_vehicle():
    # Connect to database
    try:
        connection = cx_Oracle.connect(CONNECT_INFO)
        curs = connection.cursor()
    except cx_Oracle.DatabaseError as exception:
        error = exception.args
        print(sys.stderr, "Oracle code: ", error.code)
        print(sys.stderr, "Oracle message: ", error.message)
        return

    valid = False
    while not valid:
        
        # Get serial_no of car from user
        while True:
            serial_no = input('Please enter the serial number of the vehicle: ').strip()
            if serial_no == 'q':
                exit()
            elif len(serial_no) == 15:
                
                # Look up serial number if it's already registered
                try:
                    curs.execute("SELECT serial_no FROM vehicle WHERE serial_no = int('{0}')".format(serial_no))
                    result.curs.fetchall()
                except cx_Oracle.DatabaseError as exception:
                    error = exception.args
                    print(sys.stderr, "Oracle code: ", error.code)
                    print(sys.stderr, "Oracle message: ", error.message)
                    return
                        
                if result:
                    print('Vehicle has already been registered. Please try again.')
                else:
                    # Register vehicle
                    try:
                        maker = input('Please enter the serial number of the vehicle: ').strip()
                        model = input('Please enter the serial number of the vehicle: ').strip()
                        year = input('Please enter the serial number of the vehicle: ').strip()
                        color = input('Please enter the serial number of the vehicle: ').strip()
                        type_id = input('Please enter the serial number of the vehicle: ').strip()
                        
                        #UNSURE ABOUT TYPE_ID BEING CONVERTED TO AN INT // do we even need type_id?
                        curs.execute("""INSERT INTO vehicle VALUES
                                        (int('{0}'), '{1}', '{2}', '{3}', '{4}', int('{5}'))"""
                                        .format(serial_no, maker, model, year, color, type_id))
                        connection.commit()
                    except cx_Oracle.DatabaseError as exception:
                        error = exception.args
                        print(sys.stderr, "Oracle code: ", error.code)
                        print(sys.stderr, "Oracle message: ", error.message)
                        return
                                     
                    # Register person
                    try:
                        maker = input('Please enter the serial number of the vehicle: ').strip()
                        model = input('Please enter the serial number of the vehicle: ').strip()
                        year = input('Please enter the serial number of the vehicle: ').strip()
                        color = input('Please enter the serial number of the vehicle: ').strip()
                        type_id = input('Please enter the serial number of the vehicle: ').strip()
                                     
                        curs.execute("""INSERT INTO vehicle VALUES
                            (int('{0}'), '{1}', '{2}', '{3}', '{4}', int('{5}'))"""
                            .format(serial_no, maker, model, year, color, type_id))
                        connection.commit()
                    except cx_Oracle.DatabaseError as exception:
                        error = exception.args
                        print(sys.stderr, "Oracle code: ", error.code)
                        print(sys.stderr, "Oracle message: ", error.message)
                        return
                                     
                    # Register owner
                    try:
                        maker = input('Please enter the serial number of the vehicle: ').strip()
                        model = input('Please enter the serial number of the vehicle: ').strip()
                        year = input('Please enter the serial number of the vehicle: ').strip()
                        color = input('Please enter the serial number of the vehicle: ').strip()
                        type_id = input('Please enter the serial number of the vehicle: ').strip()
                                    
                        curs.execute("""INSERT INTO vehicle VALUES
                            (int('{0}'), '{1}', '{2}', '{3}', '{4}', int('{5}'))"""
                            .format(serial_no, maker, model, year, color, type_id))
                        connnection.commit()
                    except cx_Oracle.DatabaseError as exception:
                        error = exception.args
                        print(sys.stderr, "Oracle code: ", error.code)
                        print(sys.stderr, "Oracle message: ", error.message)
                        return
                                
    valid = True

    try:
        curs.close()
        connection.close()
    except cx_Oracle.DatabaseError as exception:
        error = exception.args
        print(sys.stderr, "Oracle code: ", error.code)
        print(sys.stderr, "Oracle message: ", error.message)
        return

    #return something




def transaction():
    #TO DO
    # Connect to database
    try:
        con = cx_Oracle.connect(CONNECT_INFO)
        curs = con.cursor()
    except cx_Oracle.DatabaseError as exception:
        error = exception.args
        print(sys.stderr, "Oracle code: ", error.code)
        print(sys.stderr, "Oracle message: ", error.message)
        return
    #-----------------
    #TO DO
    #-----------------
    try:
        curs.close()
        con.close()
    except cx_Oracle.DatabaseError as exception:
        error = exception.args
        print(sys.stderr, "Oracle code: ", error.code)
        print(sys.stderr, "Oracle message: ", error.message)
        return

    #return something




def register_license():
    #TO DO
    # Connect to database
    try:
        con = cx_Oracle.connect(CONNECT_INFO)
        curs = con.cursor()
    except cx_Oracle.DatabaseError as exception:
        error = exception.args
        print(sys.stderr, "Oracle code: ", error.code)
        print(sys.stderr, "Oracle message: ", error.message)
        return
    #-----------------
    #TO DO
    #-----------------
    try:
        curs.close()
        con.close()
    except cx_Oracle.DatabaseError as exception:
        error = exception.args
        print(sys.stderr, "Oracle code: ", error.code)
        print(sys.stderr, "Oracle message: ", error.message)
        return

    #return something




def record_violation():
    #TO DO
    # Connect to database
    try:
        con = cx_Oracle.connect(CONNECT_INFO)
        curs = con.cursor()
    except cx_Oracle.DatabaseError as exception:
        error = exception.args
        print(sys.stderr, "Oracle code: ", error.code)
        print(sys.stderr, "Oracle message: ", error.message)
        return
    #-----------------
    #TO DO
    #-----------------
    try:
        curs.close()
        con.close()
    except cx_Oracle.DatabaseError as exception:
        error = exception.args
        print(sys.stderr, "Oracle code: ", error.code)
        print(sys.stderr, "Oracle message: ", error.message)
        return

    #return something




def search():
    # Connect to database
    try:
        con = cx_Oracle.connect(CONNECT_INFO)
        curs = con.cursor()
    except cx_Oracle.DatabaseError as exception:
        error = exception.args
        print(sys.stderr, "Oracle code: ", error.code)
        print(sys.stderr, "Oracle message: ", error.message)
        return
    #-----------------
    #TO DO
    #-----------------
    try:
        curs.close()
        con.close()
    except cx_Oracle.DatabaseError as exception:
        error = exception.args
        print(sys.stderr, "Oracle code: ", error.code)
        print(sys.stderr, "Oracle message: ", error.message)
        return

    #return something

if __name__ == "__main__":
    main()


