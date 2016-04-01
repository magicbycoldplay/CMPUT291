import bsddb3 as bsddb
import os
import random
import datetime
import time
import sys
import getopt
import shutil

DA_FILE = "/tmp/lnreyes/projectdatabase"
DB_SIZE = 1000
SEED = 10000000

def get_random():
    return random.randint(0, 63)
def get_random_char():
    return chr(97 + random.randint(0, 25))

def main():
    file_setup()
    
    
    #Get user to pick an option
    print("----Type 'menu' to go back to main menu-----")
    print("--------------------------------------------")
    print("Enter [1] to create and populate a database")
    print("Enter [2] to retrieve records with a given key")
    print("Enter [3] to retrieve records with a given data")
    print("Enter [4] to retrieve records with a given range of key values")
    print("Enter [5] to destroy the database")
    print("Enter [6] to quit")
    print("--------------------------------------------")
    option = input('Please pick an option: ')
    try:
        option = int(option)
    except ValueError as ve:
        pass
    
    if option == 1:
        populate_database()
    elif option == 2:
        key_search()
    elif option == 3:
        data_search()
    elif option == 4:
        range_search()
    elif option == 5:
        destroy_database()
    elif option == 6:
        exit()
    else:
        #Get user to pick an option
        print("----Type 'menu' to go back to main menu-----")
        print("--------------------------------------------")
        print("Enter [1] to create and populate a database")
        print("Enter [2] to retrieve records with a given key")
        print("Enter [3] to retrieve records with a given data")
        print("Enter [4] to retrieve records with a given range of key values")
        print("Enter [5] to destroy the database")
        print("Enter [6] to quit")
        print("--------------------------------------------")
        option = input('Invalid input. Please pick an option: ')
    return

def file_setup():
    global answerFile
    try:
        os.stat("/tmp/lnreyes_db")
    except:
        os.mkdir("/tmp/lnreyes_db")
        print("Folder was created")
    
    try:
        answerFile = open("answers", "w")
    except:
        print("Error in opening file")
    return
    

def populate_database():
    return

def key_search():
    return

def data_search():
    return

def range_search():
    return

def destroy_database():
    return
        
if __name__ == "__main__":
        main()