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
        print("------------Type 'quit' to quit ------------")
        print("----Type 'menu' to go back to main menu-----")
        print("--------------------------------------------")
        print("Enter '1' to register a vehicle")
        print("Enter '2' to make an auto transaction")
        print("Enter '3' for register a license")
        print("Enter '4' to record a violation ticket")
        print("Enter '5' to search")
        print("--------------------------------------------")
        option = input('Please pick an option: ')
        if 'quit' in option.lower():
            exit()
        else:
            try:
                option = int(option)
            except ValueError as ve:
                pass

        if option == 1:
            register_vehicle()
        elif option == 2:
            auto_transaction()
        elif option == 3:
            register_licence()
        elif option == 4:
            record_violation()
        elif option == 5:
            search()
        else:
            print("--------------------------------------------")
            print("Enter [1] to register a vehicle")
            print("Enter [2] to make an auto transaction")
            print("Enter [3] to register a licence")
            print("Enter [4] to record a violation ticket")
            print("Enter [5] to search")
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
    ''' Completes an auto transaction '''
    # Connect to database
    try:
        connection = cx_Oracle.connect(CONNECT_INFO)
        curs = connection.cursor()
    except cx_Oracle.DatabaseError as exception:
        error = exception.args
        print(sys.stderr, "Oracle code: ", error.code)
        print(sys.stderr, "Oracle message: ", error.message)
        return
    
    #-------------------------------------------------------------TRANSACTION ID
    transaction_correct=False
    while not transaction_correct:
        t_id = input("Enter transaction ID: ")
        choice(t_id)
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
            transaction_correct = True
            
    #---------------------------------------------------------------------SELLER
    answer_correct = False
    while not answer_correct:
        answer = input("Is the seller in the system (y/n): ").lower()
        choice(answer)
        if answer == 'y':
            seller_id = input('Please enter the seller SIN: ').strip()
            choice(seller_id)
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
                answer_correct = True
            else:
                #seller not in the system
                print("seller NOT in the system, please try again") 
        elif answer == 'n':
            answer_correct = True
            seller_id = add_person()
        else:
            print("Please enter 'y' or 'n'")
            print('')
            
    #----------------------------------------------------------------------BUYER
    answer_correct = False
    while not answer_correct:
        answer = input("Is the buyer in the system (y/n): ").lower()
        choice(answer)
        if answer == 'y':
            buyer_id = input('Please enter the buyer SIN: ').strip()
            choice(buyer_id)
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
                answer_correct = True
            else:
                #buyer not in the system
                print("buyer NOT in the system, please try again") 
        elif answer == 'n':
            answer_correct = True
            buyer_id = add_person()
        else:
            print("Please enter 'y' or 'n'")
            print('')    
            
    #--------------------------------------------------------------------VEHICLE
    answer = False
    while not answer:
        answer = input("Is the vehicle in the system (y/n): ").lower()
        choice(answer)
        #vehicle in database
        if answer == 'y':
            answer = False
            vehicle_id = input('Please enter the serial number of the vehicle: ').strip()
            choice(vehicle_id)
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
                print('')
                
                #check that the vehicle is owned by the seller
                try:
                    curs.execute("SELECT * FROM owner WHERE owner_id = '{0}' AND vehicle_id = '{1}' AND is_primary_owner = 'y'".format(seller_id, vehicle_id))
                    not_owner = curs.fetchall()
                except cx_Oracle.DatabaseError as exception:
                    error = exception.args
                    print(sys.stderr, "Oracle code: ", error.code)
                    print(sys.stderr, "Oracle message: ", error.message)
                    return
                if not_owner:
                    print("Vehicle is owned by the seller")
                    answer = True
                    new_vehicle = False
                else:
                    print("Vehicle is not owned by seller, please try again")
                    answer = False
            else:
                #vehicle not in the system
                print('Vehicle not in system, please try again') 
        #add vehicle to system
        elif answer == 'n':
            try:
                vehicle_id = input('Please enter the serial number of the vehicle: ').strip()
                choice(vehicle_id)
                maker = input('Please enter the maker of the vehicle: ').strip()
                model = input('Please enter the model of the vehicle: ').strip()
                year = input('Please enter the year of the vehicle: ').strip()
                color = input('Please enter the colour of the vehicle: ').strip()
                type_id = input('Please enter the type ID of the vehicle: ').strip()

                curs.execute("INSERT INTO vehicle VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}')"
                                .format(vehicle_id, maker, model, int(year), color, int(type_id)))
                connection.commit()
                new_vehicle = True
            except:
                print('One or more inputs not formated correctly, please try again')  
            print("--- VEHICLE ADDED TO DATABASE ---")
            answer = True
        else:
            print("Please enter 'y' or 'n'")
            print('')  
            
    #--------------------------------------------------------------------- PRICE                
    price = input('Please enter the price: ').strip()
    choice(price) 
    
    #-----------------------------------------------------------------------DATE 
    date_correct = False
    while not date_correct:
        s_date = input('Please enter the date of sale transaction (YYYY-MM-DD): ').strip()
        choice(price)
    
        try:
            curs.execute("INSERT INTO auto_sale VALUES ('{0}','{1}','{2}','{3}', date '{4}', '{5}')"
                        .format(int(t_id),seller_id,buyer_id,vehicle_id,s_date,int(price)))
            connection.commit()
            date_correct = True
        except cx_Oracle.DatabaseError as exception:
            error = exception.args
            print(sys.stderr, "Oracle code: ", error.code)
            print(sys.stderr, "Oracle message: ", error.message)                        
            print('Date not formatted correctly please try again') 
    
    #delete previous ownership        
    try:
        curs.execute("INSERT INTO owner VALUES ('{0}','{1}','y')".format(buyer_id,vehicle_id))
        connection.commit()
        #delete the previous owner from ownership
        if not new_vehicle:
            curs.execute("DELETE FROM owner WHERE owner_id = '{0}' AND vehicle_id = '{1}'".format(seller_id,vehicle_id))
            connection.commit()
    except cx_Oracle.DatabaseError as exception:
        error = exception.args
        print(sys.stderr, "Oracle code: ", error.code)
        print(sys.stderr, "Oracle message: ", error.message)                 
        
    print('--- AUTO SALE RECORDED ---')   

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
    ''' Registers a vehicle '''
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
    while valid == False:
        
        # Get car info
        found = False
        while found == False:
            serial_no = input("Please enter the serial number of the vehicle: ").strip()
            if serial_no == 'quit':
                exit()
            elif serial_no = 'menu':
                main()
            else:
                # Look up serial number if it's already registered
                try:
                    curs.execute("SELECT serial_no FROM vehicle WHERE serial_no = '{0}'".format(serial_no))
                    result = curs.fetchall()
                except cx_Oracle.DatabaseError as exception:
                    error = exception.args
                    print(sys.stderr, "Oracle code: ", error.code)
                    print(sys.stderr, "Oracle message: ", error.message)
                    return
                
                if result:
                    print('Vehicle has already been registered.')
                    found = True
                else:
                # Register vehicle
                    try:
                        maker = input('Please enter the maker of the vehicle: ').strip()
                        model = input('Please enter the model of the vehicle: ').strip()
                        year = input('Please enter the year of the vehicle: ').strip()
                        color = input('Please enter the serial number of the vehicle: ').strip()
                        # FORMATTING MAY BE WEIRD
                        type_id = input('TYPES \n 1 - sedan \n 2 - SUV \n 3 - van \n Please enter the type of the vehicle: ').strip()
                        curs.execute("INSERT INTO vehicle VALUES('{0}', '{1}', '{2}', '{3}', '{4}', '{5}')".format(serial_no, maker, model, year, color, int(type_id)))
                        connection.commit()
                        found = True
                    except cx_Oracle.DatabaseError as exception:
                        error = exception.args
                        print(sys.stderr, "Oracle code: ", error.code)
                        print(sys.stderr, "Oracle message: ", error.message)
                        return
                             
        # Get person info
        found = False
        while found == False:
            sin = input('Please enter the sin number of the person: ').strip()
            if sin == 'quit':
                exit()
            elif sin == 'menu':
                main()
            else:
                # Look up serial number if it's already registered
                try:
                    curs.execute("SELECT sin FROM people WHERE sin = '{0}'".format(sin))
                    result = curs.fetchall()
                except cx_Oracle.DatabaseError as exception:
                    error = exception.args
                    print(sys.stderr, "Oracle code: ", error.code)
                    print(sys.stderr, "Oracle message: ", error.message)
                    return
                         
                if result:
                    print('Person has already been registered.')
                    found = True
                else:
                    # Register person
                    try:
                        name = input('Please enter the name of the person: ').strip()
                        height = input('Please enter the height of the person: ').strip()
                        weight = input('Please enter the weight of the person: ').strip()
                        eyecolor = input('Please enter the eye colour of the person: ').strip()
                        haircolor = input('Please enter the hair colour of the person: ').strip()
                        addr = input('Please enter the address of the person: ').strip()
                        gender = input('Please enter the gender of the person (m/f): ').strip().lower()
                        birthday = input('Please enter the birthday of the person (YYYY-MM-DD): ').strip()
                         
                        curs.execute("INSERT INTO people VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', date'{8}')".format(sin, name, int(height), int(weight), eyecolor, haircolor, addr, gender, birthday))
                        connection.commit()
                        found = True
                    except cx_Oracle.DatabaseError as exception:
                        error = exception.args
                        print(sys.stderr, "Oracle code: ", error.code)
                        print(sys.stderr, "Oracle message: ", error.message)
                        return
                                     
        # Get owner info
        set = False
        while set == False:
            # Register owner
            try:
                # Primary owner
                sin = input('Please enter the sin number of the primary owner of the vehicle: ').strip()
                if sin == 'quit':
                    exit()
                elif sin = 'menu':
                    main()
                else:                
                    curs.execute("SELECT name FROM people WHERE sin = '{0}'".format(sin))
                    result = curs.fetchall()
                    primary_owner = input('Is %s the primary owner of this vehicle? (y/n) ' %result).lower()
                    
                    # Checks if recorded already
                    curs.execute("SELECT * FROM owner WHERE owner_id = '{0}' AND vehicle_id = '{1}' AND is_primary_owner = '{2}'".format(sin, serial_no, primary_owner))
                    result = curs.fetchall()
                    if not result:
                        curs.execute("INSERT INTO owner VALUES ('{0}', '{1}', '{2}')".format(sin, serial_no, primary_owner))
                    
                    # Secondary owner
                    answer = input('Is there a secondary owner for this vehicle? (y/n) ')
                    if answer.lower() == 'y':
                        sin = input('Please enter the sin number of the secondary owner of the vehicle: ').strip()
                        if sin == 'quit':
                            exit()
                        elif sin = 'menu':
                            main()
                        else:
                            curs.execute("SELECT name FROM people WHERE sin = '{0}'".format(sin))
                            result = curs.fetchall()
                            secondary_owner = input('Is %s the secondary owner of this vehicle? (y/n) ' %result).lower()
                            if secondary_owner == 'y':
                                secondary_owner = 'n'
                                curs.execute("INSERT INTO owner VALUES ('{0}', '{1}', '{2}')".format(sin, serial_no, secondary_owner))
                                
                    connection.commit()
                    set = True
        
            except cx_Oracle.DatabaseError as exception:
                error = exception.args
                print(sys.stderr, "Oracle code: ", error.code)
                print(sys.stderr, "Oracle message: ", error.message)
                return
        
        # Close connection
        try:
            curs.close()
            connection.close()
            valid = True
        except cx_Oracle.DatabaseError as exception:
            error = exception.args
            print(sys.stderr, "Oracle code: ", error.code)
            print(sys.stderr, "Oracle message: ", error.message)
            return
    return

def add_person():
    #TO DO
    # Connect to database
    try:
        connection = cx_Oracle.connect(CONNECT_INFO)
        curs = connection.cursor()
    except cx_Oracle.DatabaseError as exception:
        error = exception.args
        print(sys.stderr, "Oracle code: ", error.code)
        print(sys.stderr, "Oracle message: ", error.message)
        return   
    
    #------------------------------------------------------------------------SIN
    person_correct = False
    while not person_correct:
        
        sin_correct = False
        while not sin_correct:
            sin = input("Enter the person's SIN number: ")
            choice(sin)
            try:
                curs.execute("SELECT sin FROM people WHERE sin = '{0}'".format(sin))
                sin_result1 = curs.fetchall()
            except cx_Oracle.DatabaseError as exception:
                error = exception.args
                print(sys.stderr, "Oracle code: ", error.code)
                print(sys.stderr, "Oracle message: ", error.message)
                return          
            if sin_result1:
                print('Person already in the system, try again')
                print("")
            else:
                sin_correct = True
        #-------------------------------------------------------------------NAME
        name = input("Enter the person's name: ")
        choice(name)
        
        #-----------------------------------------------------------------HEIGHT
        height = input("Enter the person's height: ")
        choice(height)
        
        #-----------------------------------------------------------------WEIGHT
        weight = input("Enter the person's weight: ")
        choice(weight)
        
        #---------------------------------------------------------------EYECOLOR
        eyecolor = input("Enter the person's eyecolor: ")
        choice(eyecolor)
        
        #--------------------------------------------------------------HAIRCOLOR
        haircolor = input("Enter the person's haircolor: ")
        choice(haircolor)
        
        #----------------------------------------------------------------ADDRESS
        addr = input("Enter the person's address: ")
        choice(addr)
        
        #-----------------------------------------------------------------GENDER
        gender_correct = False
        while not gender_correct:
            gender = input("Enter the person's gender(m/f): ").lower()
            choice(gender)
            if gender == 'm' or gender == 'f':
                gender_correct = True
            else:
                print("Gender must be 'm' or 'f'")
                print('')
        
        #---------------------------------------------------------------BIRTHDAY
        birthday = input("Enter the person's birthday (YYYY-MM-DD): ")
        choice(birthday)
        
        try:
            curs.execute("INSERT INTO people VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}', date '{8}')"
                         .format(sin,name,float(height),float(weight),
                                 eyecolor,haircolor,addr,gender,birthday))
            connection.commit()
            person_correct = True
            print("---- PERSON ADDED TO DATABASE ----")
        except:
            print("Error with format of input try again")
            
    #close connection
    try:
        curs.close()
        connection.close()
    except cx_Oracle.DatabaseError as exception:
        error = exception.args
        print(sys.stderr, "Oracle code: ", error.code)
        print(sys.stderr, "Oracle message: ", error.message) 
        
    return sin

def register_licence():
    #TO DO
    # Connect to database
    try:
        connection = cx_Oracle.connect(CONNECT_INFO)
        curs = connection.cursor()
    except cx_Oracle.DatabaseError as exception:
        error = exception.args
        print(sys.stderr, "Oracle code: ", error.code)
        print(sys.stderr, "Oracle message: ", error.message)
        return
    
    
    #-----------------------------------------------------------------PERSON SIN
    answer_correct = False
    while not answer_correct:
        answer = input("Is the person in the system (y/n): ").lower()
        choice(answer)
        if answer == 'y':
            #get the person's sin
            sin = input("Enter the person's SIN: ")
            choice(sin)
            try:
                curs.execute("SELECT sin FROM people WHERE sin = '{0}'".format(sin))
                sin_result = curs.fetchall()
            except cx_Oracle.DatabaseError as exception:
                error = exception.args
                print(sys.stderr, "Oracle code: ", error.code)
                print(sys.stderr, "Oracle message: ", error.message)
                return  
            if sin_result:
                #check to see if person already has a licence
                try:
                    curs.execute("SELECT sin FROM drive_licence WHERE sin = '{0}'".format(sin))
                    already_has = curs.fetchall()
                except cx_Oracle.DatabaseError as exception:
                    error = exception.args
                    print(sys.stderr, "Oracle code: ", error.code)
                    print(sys.stderr, "Oracle message: ", error.message)
                    return
                if already_has:
                    print('Person already has licence try again')
                    print('')
                else:
                    answer_correct = True 
                    sin_correct = True
            else:
                print('Person not in the system try again')
                print('')
        elif answer == 'n':
            #add a new person
            sin = add_person()
            answer_correct = True  
        else:
            print("Please enter 'y' or 'n'")
            print('')
            
    #-------------------------------------------------------------LICENCE NUMBER
    licence_correct = False
    while not licence_correct:
        licence_no = input("Enter the licence number: ")
        choice(licence_no)
        try:
            curs.execute("SELECT licence_no FROM drive_licence WHERE licence_no = '{0}'".format(licence_no))
            licence_result = curs.fetchall()
        except cx_Oracle.DatabaseError as exception:
            error = exception.args
            print(sys.stderr, "Oracle code: ", error.code)
            print(sys.stderr, "Oracle message: ", error.message)
            return  
        if licence_result:
            print("Licence already in the system try again")
            print('')
        else:
            licence_correct = True
    
    #----------------------------------------------------------------------CLASS
    class_no = input("Enter the driving class: ")
    choice(class_no)
    
    #----------------------------------------------------------------------PHOTO
    photo_name = input("Enter the photo name: ")
    choice(photo_name)
    f_image = open('test.jpg','rb')
    photo = 'NULL'
    #curs.setinputsizes(photo=cx_Oracle.BLOB)
    
    #---------------------------------------------------------------ISSUING DATE
    issuing_date = input("Enter the issuing date (YYYY-MM-DD): ")
    choice(issuing_date)
    
    #--------------------------------------------------------------EXPIRING DATE
    expiring_date = input("Enter the expiring date (YYYY-MM-DD): ")
    choice(expiring_date)
    
    try:                   
        curs.execute("INSERT INTO drive_licence VALUES ('{0}','{1}','{2}',{3}, date '{4}', date '{5}')".format(licence_no,sin,class_no,photo,issuing_date,expiring_date))
        connection.commit()
    except cx_Oracle.DatabaseError as exception:
        error = exception.args
        print(sys.stderr, "Oracle code: ", error.code)
        print(sys.stderr, "Oracle message: ", error.message)
        return      

    f_image.close()
    print("---- LICENCE ADDED TO DATABASE ----")
    try:
        curs.close()
        connection.close()
    except cx_Oracle.DatabaseError as exception:
        error = exception.args
        print(sys.stderr, "Oracle code: ", error.code)
        print(sys.stderr, "Oracle message: ", error.message)
        return

    return




def record_violation():
    #TO DO
    # Connect to database
    try:
        connection = cx_Oracle.connect(CONNECT_INFO)
        curs = connection.cursor()
    except cx_Oracle.DatabaseError as exception:
        error = exception.args
        print(sys.stderr, "Oracle code: ", error.code)
        print(sys.stderr, "Oracle message: ", error.message)
        return
    
    #-------------------------------------------------------------OFFICER NUMBER
    office_correct = False
    while not office_correct:
        office_no = input ("Enter the officer number: ").strip()
        choice(office_no)
        #make sure the officer is in the system
        try:
            curs.execute("SELECT sin FROM people WHERE sin = '{0}'".format(office_no))
            officer_result = curs.fetchall()
        except cx_Oracle.DatabaseError as exception:
            error = exception.args
            print(sys.stderr, "Oracle code: ", error.code)
            print(sys.stderr, "Oracle message: ", error.message)
            return
        if officer_result:
            office_correct = True
        else:
            print('Officer not in system try again')
            print('')
            
    #-----------------------------------------------------------------VEHICLE ID
    vehicle_correct = False
    while not vehicle_correct:
        vehicle_id = input("Enter the vehicle serial number: ").strip()
        choice(vehicle_id)
        #check to see if vehicle is in the system
        try:
            curs.execute("SELECT serial_no FROM vehicle WHERE serial_no = '{0}'".format(vehicle_id))
            vehicle_result = curs.fetchall()
        except cx_Oracle.DatabaseError as exception:
            error = exception.args
            print(sys.stderr, "Oracle code: ", error.code)
            print(sys.stderr, "Oracle message: ", error.message)
            return
        if vehicle_result:
            vehicle_correct = True
        else: 
            print('Vehicle not in system try again')
            print('')
    
    #----------------------------------------------------------------VIOLATOR ID
    input_correct = False
    while not input_correct:
        offender_is_primary = input("Is violator primary owner of the vehicle (y/n): ").strip()
        choice(offender_is_primary)
        if offender_is_primary == 'y':
            input_correct = True
            #get primary owner of vehicle
            try:
                curs.execute("SELECT owner_id FROM owner WHERE vehicle_id = '{0}' AND is_primary_owner = 'y'".format(vehicle_id))
                violator_no = str(curs.fetchall())
                violator_no = violator_no[3:-4]
            except cx_Oracle.DatabaseError as exception:
                error = exception.args
                print(sys.stderr, "Oracle code: ", error.code)
                print(sys.stderr, "Oracle message: ", error.message)
                return
        #if the violator is not the primary owner have them enter the violator number
        elif offender_is_primary == 'n':
            input_correct = True
            violator_correct = False
            while not violator_correct:
                violator_no = input("Enter the violator number: ")
                choice(violator_no)
                try:
                    curs.execute("SELECT sin FROM people WHERE sin = '{0}'".format(violator_no))
                    violator_result = curs.fetchall()
                except cx_Oracle.DatabaseError as exception:
                    error = exception.args
                    print(sys.stderr, "Oracle code: ", error.code)
                    print(sys.stderr, "Oracle message: ", error.message)
                    return   
                if violator_result:
                    violator_correct = True
                else:
                    print('Violator not in system try again')
                    print('')        
        else:
            print("Please enter 'y' or 'n'")
            print('')
            
    #--------------------------------------------------------------TICKET NUMBER
    ticket_correct = False
    while not ticket_correct:
        ticket_num = False
        while not ticket_num:
            ticket_no = input("Enter ticket number: ").strip()
            choice(ticket_no)
            try:
                ticket_no = int(ticket_no)
                ticket_num = True
            except:
                print("Ticket number must be a number")
                print('')            
        #check that ticket number hasn't already been used
        try:
            curs.execute("SELECT * FROM ticket WHERE ticket_no = '{0}'".format(ticket_no))
            ticket_result = curs.fetchall()
        except cx_Oracle.DatabaseError as exception:
            error = exception.args
            print(sys.stderr, "Oracle code: ", error.code)
            print(sys.stderr, "Oracle message: ", error.message)
            return  
        if ticket_result:
            print("Ticket number already in system try again")
            print('')
        else:
            ticket_correct = True

            
    #----------------------------------------------------------------------VTYPE
    type_correct = False
    while not type_correct:
        vtype = ''
        while len(vtype) == 0:
            vtype = input("Enter violation type: ").strip()
            choice(vtype)
        try:
            curs.execute("SELECT vtype FROM ticket_type")
            ticket_result = curs.fetchall()
        except cx_Oracle.DatabaseError as exception:
            error = exception.args
            print(sys.stderr, "Oracle code: ", error.code)
            print(sys.stderr, "Oracle message: ", error.message)
            return
        if vtype in str(ticket_result):
            type_correct = True
        else:
            print("That type of ticket is not in the system try a different type")
            print('')
        
    #----------------------------------------------------------------------PLACE
    place = input("Enter place of violation: ").strip()
    choice(place)
            
    #----------------------------------------------------------------DESCRIPTION
    descriptions = input("Enter ticket description: ").strip()
    choice(descriptions)
    
    #----------------------------------------------------------------------VDATE
    vdate_correct = False
    while not vdate_correct:
        vdate = input("Enter violation date (YYYY-MM-DD): ").strip()
        choice(vdate)
        try:
            curs.execute("INSERT INTO ticket VALUES ('{0}','{1}','{2}','{3}','{4}', date '{5}','{6}','{7}')".format(ticket_no,violator_no,vehicle_id,office_no,vtype,vdate,place,descriptions))
            connection.commit()
            vdate_correct = True
        except:
            print("Date not formatted correctly (YYYY-MM-DD) try again")
            print('')

    print('')
    print("---- TICKET ADDED TO DATABASE ----")
    try:
        curs.close()
        connection.close()
    except cx_Oracle.DatabaseError as exception:
        error = exception.args
        print(sys.stderr, "Oracle code: ", error.code)
        print(sys.stderr, "Oracle message: ", error.message)
        return

    return

    
def choice(selection):
    if selection == 'quit':
        exit()
    elif selection == 'menu':
        main()
    return

def search():

    while True:
        #Get user to pick an option
        print("-----------------------------------------------------")
        print("Enter [1] to look up a person's information")
        print("Enter [2] to look up a person's violation records")
        print("Enter [3] to look up a vehicle's history")
        print("-----------------------------------------------------")
        option = input('Please pick an option: ')
        if 'quit' in option.lower():
            exit()
        elif option = 'menu':
            main()
        else:
            try:
                option = int(option)
            except ValueError as ve:
                pass

        if option == 1:
            people_info()
        elif option == 2:
            people_vrecord()
        elif option == 3:
            vehicle_history()
        else:
            print('Invalid option! Please pick again.')

    return
    
def people_info():
    # Connect to database
    try:
        connection = cx_Oracle.connect(CONNECT_INFO)
        curs = connection.cursor()
    except cx_Oracle.DatabaseError as exception:
        error = exception.args
        print(sys.stderr, "Oracle code: ", error.code)
        print(sys.stderr, "Oracle message: ", error.message)
        return
    
    while True:
        # Asks user to input a license number or name
        info = input("Please enter a licence # or name: ").strip()
            if info == 'quit':
                exit()
            elif info = 'menu':
                main()
            elif info.isalpha():
                # Checks if it's made up of the alphabet (name)
                # Looks up a name
                try:
                    # Looks up if name is in database
                    curs.execute("SELECT name FROM people WHERE name = '{0}'".format(info))
                    result = curs.fetchall()
                except cx_Oracle.DatabaseError as exception:
                    error = exception.args
                    print(sys.stderr, "Oracle code: ", error.code)
                    print(sys.stderr, "Oracle message: ", error.message)
                    return

                if result:
                    # Makes a view
                    curs.execute("CREATE VIEW OR REPLACE VIEW person_info AS
                                 SELECT name, dl.licence_no, addr, birthday,
                                 class, dc.description, expiring_date
                                 FROM people p, drive_licence dl, driving_condition dc, restriction r
                                 WHERE p.sin = dl.sin AND dc.c_id = r.r_id AND r.licence_no = drive_licence")
                    connection.commit()
                else:
                    print('Person not found')
                    
            # If not a name, then it might be a licence number        
            else 
                try:
                    info = int(info)
                except ValueError as ve:
                    pass 
                
                # Checks if it's a numeric number (licence_no)
                if info.isnumeric():    
                    try:
                        # Looks up a name
                        info = str(info)
                        curs.execute("SELECT licence_no FROM drive_licence WHERE licence_no = '{0}'".format(info))
                        result = curs.fetchall()
                    except cx_Oracle.DatabaseError as exception:
                        error = exception.args
                        print(sys.stderr, "Oracle code: ", error.code)
                        print(sys.stderr, "Oracle message: ", error.message)
                        return

                    if result:
                        # Makes a view
                        curs.execute("CREATE VIEW OR REPLACE VIEW person_info AS
                                 SELECT name, dl.licence_no, addr, birthday,
                                 class, dc.description, expiring_date
                                 FROM people p, drive_licence dl, driving_condition dc, restriction r
                                 WHERE p.sin = dl.sin AND dc.c_id = r.r_id AND r.licence_no = drive_licence")
                        connection.commit()
                    else:
                        print('Licence number not found')
                                     
    # Close connection        
    try:
        curs.close()
        connection.close()
    except cx_Oracle.DatabaseError as exception:
        error = exception.args
        print(sys.stderr, "Oracle code: ", error.code)
        print(sys.stderr, "Oracle message: ", error.message)
        return

    return
    
def people_vrecord():
    # Connect to database
    try:
        connection = cx_Oracle.connect(CONNECT_INFO)
        curs = connection.cursor()
    except cx_Oracle.DatabaseError as exception:
        error = exception.args
        print(sys.stderr, "Oracle code: ", error.code)
        print(sys.stderr, "Oracle message: ", error.message)
        return
    
    while True:
        info = input("Please enter a licence # or sin #: ").strip()
            if info == 'quit':
                exit()
            elif info = 'menu':
                main()
            else:
                # Checks if it's a licence 
                try:
                    # Looks up a licence number
                    curs.execute("SELECT licence_no FROM drive_licence WHERE licence_no = '{0}'".format(info))
                    result = curs.fetchall()
                except cx_Oracle.DatabaseError as exception:
                    error = exception.args
                    print(sys.stderr, "Oracle code: ", error.code)
                    print(sys.stderr, "Oracle message: ", error.message)
                    return

                if result:
                    # Makes a view
                    curs.execute("CREATE VIEW OR REPLACE VIEW people_violation_record AS
                                 SELECT name, ticket_no, tt.vtype, t.vdate, place t.description,
                                 FROM people p, ticket t, ticket_type tt, vehicle v, drive_licence dl
                                 WHERE p.sin = t.violator_no AND v.serial_no = t.vehicle_id AND tt.vtype = t.vtype dl.sin = p.sin AND t.violator_no = dl.sin AND '{0}' = dl.licence_no".format(info))
                    connection.commit()
                else:
                    try:
                        # Looks up a sin number
                        curs.execute("SELECT sin FROM people WHERE sin = '{0}'".format(info))
                        result = curs.fetchall()
                    except cx_Oracle.DatabaseError as exception:
                        error = exception.args
                        print(sys.stderr, "Oracle code: ", error.code)
                        print(sys.stderr, "Oracle message: ", error.message)
                        return

                    if result:
                        # Makes a view
                        curs.execute("CREATE VIEW OR REPLACE VIEW people_violation_record AS
                                 SELECT name, ticket_no, tt.vtype, t.vdate, place t.description,
                                 FROM people p, ticket t, ticket_type tt, vehicle v
                                 WHERE p.sin = t.violator_no AND v.serial_no = t.vehicle_id AND tt.vtype = t.vtype AND '{0}' = p.sin AND '{0}' = t.violator_no".format(info))
                        connection.commit()
                    else:
                        print('Licence number and sin not found')
        
    # Close connection        
    try:
        curs.close()
        connection.close()
    except cx_Oracle.DatabaseError as exception:
        error = exception.args
        print(sys.stderr, "Oracle code: ", error.code)
        print(sys.stderr, "Oracle message: ", error.message)
        return

    return
    
def vehicle_history():
    # Connect to database
    try:
        connection = cx_Oracle.connect(CONNECT_INFO)
        curs = connection.cursor()
    except cx_Oracle.DatabaseError as exception:
        error = exception.args
        print(sys.stderr, "Oracle code: ", error.code)
        print(sys.stderr, "Oracle message: ", error.message)
        return
    
    while True:
        info = input("Please enter a vehicle serial #: ").strip()
            if info == 'quit':
                exit()
            elif info = 'menu':
                main()
            else:
                # Checks if it's a valid serial number 
                try:
                    curs.execute("SELECT serial_no FROM vehicle WHERE serial_no = '{0}'".format(info))
                    result = curs.fetchall()
                except cx_Oracle.DatabaseError as exception:
                    error = exception.args
                    print(sys.stderr, "Oracle code: ", error.code)
                    print(sys.stderr, "Oracle message: ", error.message)
                    return

                # If there is a valid serial number
                if result:
                    # Makes a view
                    curs.execute("CREATE VIEW OR REPLACE VIEW vehicle_history AS
                                 SELECT serial_no, COUNT(a.vehicle_id), AVG(a.price), COUNT() AS VehicleTransfer, AveragePrice, Violations
                                 FROM vehicle v, autosale a, ticket t
                                 WHERE v.serial_no = a.vehicle_id AND v.serial_no = t.vehicle_id AND a.vehicle_id = t.vehicle_id AND '{0}' = v.serial_no AND '{0}' = a.vehicle_id AND '{0}' = t.vehicle_id".format(info))
                    connection.commit()
                else:
                    print('Vehicle is not found')
        

        
    # Close connection        
    try:
        curs.close()
        connection.close()
    except cx_Oracle.DatabaseError as exception:
        error = exception.args
        print(sys.stderr, "Oracle code: ", error.code)
        print(sys.stderr, "Oracle message: ", error.message)
        return

    return

if __name__ == "__main__":
    main()


