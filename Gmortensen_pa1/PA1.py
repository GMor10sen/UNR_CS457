#!/usr/bin/env python3
import os
import shutil

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#Gabriel Mortensen
#2/14/2022
#CS 457
#
#Project 1: Basic Database system 
#
#This assignment was created to task students to 
#create a basic database system that can
#create and delete databases that can store tables which can be  
#created, deleted, outputted, and modified. 
#
#Various functions have been used to complete this task
#with the idea that directories are databases and files are tables. 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Define Global Variables
home_directory = os.getcwd() # Used to remember the "home" directory

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# This function Creates a table 
# in the current directory with a user input.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def CREATE_TABLE(new_table, arguments):
    
    try:       #Check to see if the table already exists, if it does bring up an error, Otherwise create a new file with table name.
        if os.path.exists(new_table):
            raise FileExistsError
        file = open(new_table, "w+")
        info = arguments[arguments.find('(')+1:arguments.rfind(')')]   #obtain information in parenthesis then remove parethesis 
        for i in info:   #Use for loop to run through arguments and replace , with | for the new file. 
            if(i == ','):
                file.write(' |')
            else:
                file.write(i)
        print('Table {0} created.'.format(new_table))  #Update User on sucess 
        file.close()
    
    except FileExistsError:  #Error message if the file already exists 
        print("!Failed to create table {0} because it already exists.".format(new_table))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# This function appends a user inputted argument/string
# to the file/table they call.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def ALTER_TABLE(old_table, new_element):
  
    try:  #If the file does not exist raise an error, otherwise open the file and append the new element      
        if not os.path.exists(old_table):
            raise FileNotFoundError
        file = open(old_table, "a+")
        file.write(' | ' + new_element) #Adding | to match format of file 
        file.close()
        print('Table {0} modified.'.format(old_table))
   
    except FileNotFoundError:   #Error message for file not existing 
        print("!Failed to alter table {0} because it does not exist.".format(old_table))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# This function outputs contents user specified table.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def SELECT_TABLE(current_table):
    
    try:   #If file does not exist raise an error, otherwise output everything the file contains (done only for project1)  
        if not os.path.exists(current_table):
            raise FileNotFoundError
        file = open(current_table, "r")
        print(file.read())
        file.close()

    except FileNotFoundError:     #Error message for no file 
        print("!Failed to query table {0} because it does not exist.".format(current_table))


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# This function deletes a table upon user input
# as long as the file is in the current database/directory.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def DROP_TABLE(user_file):
    
    try:  #try to remove the file, then notify user  
        os.remove('{0}/{1}'.format(os.getcwd(), user_file))
        print('Table {0} deleted.'.format(user_file))
   
    except FileNotFoundError:   #file not found error detected automatically 
        print("!Failed to delete {0} because it does not exist.".format(user_file))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Creates directory of user input,
# directory always in home.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def CREATE_DATABASE(new_database):
   
    try:   #Set current directory to the home directory as databases cannot be in one another (according to professsor).
        os.chdir(home_directory)
        os.mkdir(new_database)  #Make hte directory specified by user if it does not already exist 
        print('Database {0} created.'.format(new_database))
    
    except FileExistsError:  #Error message for database already existing is detected automatically
        print("!Failed to create database {0} because it already exists.".format(new_database))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Deletes an existing directory that user inputs.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def DROP_DATABASE(user_directory):

    try:  #Use home directory and user input to delete the directory specified by user. This function also deletes all files speciffied by user. 
        shutil.rmtree('{0}/{1}'.format(home_directory, user_directory))
        print('Database {0} deleted.'.format(user_directory))

    except FileNotFoundError:  #Error of file not found detected automatically and will notify user 
        print("!Failed to delete {0} because it does not exist.".format(user_directory))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Switches directory to desired oen,
# always starts at "home" directory.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def USE(user_directory):

    try:  #Use homedirectory along with user input to switch the directory then output to user   
        os.chdir('{0}/{1}'.format(home_directory, user_directory))
        print("Using database {0}.".format(user_directory))
   
    except FileNotFoundError:  #Error of file not found detected automatically and will notify user 
        print("!Failed because database {0} does not exist.".format(user_directory))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Function to convert parameters in list to a single string
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def listToString(list_element): 
  
    parameter_string = " " #Declare an empty string
    return (parameter_string.join(list_element))  #Return result   

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main function handles parsing user input  
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def Main():

    #Declare an empty string
    user_input=' '

    #Run endless loop until user desires to exit
    while (True):
        
        #Turn user input into all lowercase letters
        user_input= input('--> ').lower() 

        
        if (user_input.strip().endswith(';')):  #If statment to ensure command must end with a ';' to work

                      
            user_input = user_input.replace(';',' ') #Store all of input in a list after removing ';'
            resulting_list = user_input.split()
            
            #Series of if statements act as parser 
            if (len(resulting_list) == 2 and resulting_list[0] == 'use'): #triggers use database function
                USE(resulting_list[1])
            if (len(resulting_list) == 3 and resulting_list[0] == 'create' and resulting_list[1] == 'database'): #triggers create database function 
                CREATE_DATABASE(resulting_list[2])
            if (len(resulting_list) == 3 and resulting_list[0] == 'drop' and resulting_list[1] == 'database'): #triggers drop database function  
                DROP_DATABASE(resulting_list[2])
            if (len(resulting_list) == 3 and resulting_list[0] == 'drop' and resulting_list[1] == 'table'): #triggers drop table function
                DROP_TABLE(resulting_list[2])
            if (len(resulting_list) > 3 and resulting_list[0] == 'alter' and resulting_list[1] == 'table' and resulting_list[3] == 'add'):  #triggers alter table  function
                ALTER_TABLE(resulting_list[2], listToString(resulting_list[4:]))
            if (len(resulting_list) > 3 and resulting_list[0] == 'create' and resulting_list[1] == 'table'): #triggers create table function
                CREATE_TABLE(resulting_list[2], listToString(resulting_list[3:]))
            if (len(resulting_list) > 3 and resulting_list[0] == 'select' and resulting_list[2] == 'from' and resulting_list[1] == '*'): #triggers select table function
                SELECT_TABLE(resulting_list[3]) 
        if (user_input.strip() == '.exit'):  #When user desires an exit the program must exit  
            print('All done.') 
            exit() 
        if (len(user_input.strip()) == 0 ): #If file has empty lines they are removed when being read in 
            print (" ")
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# This guarentees that the main funciton is called first
if __name__ == "__main__":
    Main()

    
