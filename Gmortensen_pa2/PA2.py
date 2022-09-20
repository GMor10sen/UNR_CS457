#!/usr/bin/env python3
import os
import shutil

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#Gabriel Mortensen
#3/29/2022
#CS 457
#
#Project 2: Basic Data Manipulation 
#
#This assignment was created to task students to 
#create a basic database system that can modify tables such that   
#depending on certain requirements tuples can be: 
#deleted, modified, outputted to the User 
#
#Various functions have been used to complete this task
#with the idea that directories are databases and files are tables. 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Define Global Variables
home_directory = os.getcwd() # Used to remember the "home" directory

#Custom Exceptions 
class ElementNotFoundError (Exception): #this makes a new exception avaliable 
    pass
class WrongSingleQuotes (Exception): #this makes a new exception avaliable 
    pass    
class IncorrectFormat (Exception): #this makes a new exception avaliable 
    pass

#~~~~~~~~~~~~~
# Uses the equation provided in parameters to determine if equation is true or false
# returns a true or false depending on legitmacy of equation
#~~~~~~~~~~~~~
def ListToEquation(equation): 
   
    #Add double == if = sign detected 
    if (equation[1] == '='):
        equation[1] = equation[1] + equation[1]
    
    #Do different operations depending on datatypes 
    if(equation[2].isnumeric()): #numerical datatypes
        if (eval(ListToString(equation))): #default eval function that tests numerical scenarios 
            return True
        else:
            return False
    else:    #string datatypes 
        equation = ListToString(equation).replace("'", "")        #Remove all single quotes 
        equation = equation.split() #remove whitespace 
        if (equation[1] == '=='): #if both are equal test 
            if (str(equation[0]) == str(equation[2])):
                return True
            else:
                return False
        if (equation[1] == '!='): #if strings are different
            if (str(equation[0]) != str(equation[2])):
                return True
            else:
                return False
        elif (equation[1] == '>'): #if one string is "greater" than other test 
            if (str(equation[0]) > str(equation[2])):
                return True
            else:
                return False
        else: #if one string is "less" than another test
            if (str(equation[0]) < str(equation[2])):
                return True
            else:
                return False
#~~~~~~~~~~~~~
# Find the index of the identifer listed in the header 
# and modify it to work with contents of table 
#~~~~~~~~~~~~~
def FindIndex(table, element):
    header = OBTAIN_HEADER(table) #obtain header of table 
    
    sub_list = header.split() #Break header of table up into segments 
    
    index = sub_list.index(element) #Obtain index of equation datatype in header
    return int(index/3) #Divide value by 3 due to extra '|' and datatype

#~~~~~~~~~~~~~~~~~~~~~~~~`
# This function removes extra white space from the table to ensure it is in proper format 
#~~~~~~~~~~~~~~~~~~~~~~~
def CLEAN_FILE(table):
    file = open(table, "r")  
    data = file.read().rstrip('\n') #Remove white space created 
    file.close()
 
    file = open(table, "w") 
    file.write(data) #put information back in file without whitespace 
    file.close()

#~~~~~~~~~~~~~~~~~~~~~~
# This function obtains the tuples of the table 
#~~~~~~~~~~~~~~~~~~~~~~
def OBTAIN_TUPLES(table):
    file = open(table, "r") #read file 
    header = file.readline() #read header to skip header of table 
    lines = file.readlines() #obtain rest of the tuples 
    file.close() #close the file 
    return lines #return tuples 
   
#~~~~~~~~~~~~~~~~~~~~~~
# This function obtains the header of the table 
#~~~~~~~~~~~~~~~~~~~~~~
def OBTAIN_HEADER(table):
    file = open(table, "r") #read file 
    header = file.readline() #obtain headerof table 
    file.close() #close the file 
    return header #return tuples 

#~~~~~~~~~~~~
# This function delets tuples in the table 
# that match specific requirements specified by the user   
#~~~~~~~~~~~~
def DELETE_TUPLE(table, equation):

    try:  #If the file does not exist raise an error, otherwise open the file and append the new element      
        if not os.path.exists(table):
            raise FileNotFoundError

        #Declare Variables     
        delete_counter = 0 #counter used for final result 
        ElementCheck (table, equation[0]) #check if element exists, if does not exist an exception is raised 
        where_datatype_index = FindIndex(table, equation[0])  #obtain index of where type in table 
        header = OBTAIN_HEADER(table) #obtain header of table 
        lines = OBTAIN_TUPLES(table) #obtain tuples of table 
        
       

        file = open(table, "w")  #clear the entire table 
        file.write(header) #write the saved header in the file's first line 

        for tuples in lines: #run a for loop for all other tuples 
            if (WHERE_TEST (where_datatype_index, tuples, ListToString(equation[1:]))): #check equation
                delete_counter = delete_counter + 1 #do not write in tuple if true and increment counter
            else:
                file.write(tuples) #if equation false write tuple and continued 
                delete_counter = delete_counter #counter remains the same if equation false 
        file.close()

        CLEAN_FILE(table) #remove unecessary white space with function 

        if (delete_counter == 1):  #notify user of how many items have been deleted
            print('{0} record deleted.'.format(delete_counter))
        else:
            print('{0} records deleted.'.format(delete_counter))

    except FileNotFoundError:   #Error message for file not existing 
        print("!Failed to alter table {0} because it does not exist.".format(table))
    except ElementNotFoundError:
        print("!Failed to query because {0} does not exist in table {1}.".format(equation[0] ,table))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# This function replaces certain elements of tuples
# elements in tuples are replaced if they meet if_EQ requirements 
# element identifer and assignment determined by then_EQ
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def UPDATE_TABLE(table, then_EQ, if_EQ):
   
    try:  #If the file does not exist raise an error, otherwise open the file and append the new element      
        if not os.path.exists(table):
            raise FileNotFoundError
        
        #Declare variables 
        modified_counter = 0 #counter for number of tuples updated 
        temp_list = ' ' #create empty string 
        temp_list = temp_list.split() #turn empty string to list 
        header = OBTAIN_HEADER(table) #obtain header of table 
        lines = OBTAIN_TUPLES(table) #obtain tuples of table 
        
        element = if_EQ[0] #assign element 
        ElementCheck (table, element) #check if element exists, if does not exist an exception is raised 
        element = then_EQ[0] #assign element 
        ElementCheck (table, element) #check if element exists, if does not exist an exception is raised 
        
        where_datatype_index = FindIndex(table, if_EQ[0])  #obtain index of where type in table 
        set_index = FindIndex(table, then_EQ[0]) #obtain index of set type in table
      
        file = open(table, "w")  #clear the entire table 
        file.write(header) #write the saved header in the file's first line 

        for tuples in lines: #run a for loop for all other tuples 
            tuples = tuples.split() #turn tuple to list object for indexing 
            if (WHERE_TEST (where_datatype_index, ListToString(tuples), ListToString(if_EQ[1:]))): #check equation
                modified_counter = modified_counter + 1 #increment number modified 
                tuples[set_index * 2] = then_EQ[2] #change set variable to user input
            file.write(ListToString(tuples)) #write either modfied or unmodfied tuple
            file.write('\n') 

        file.close()

        CLEAN_FILE(table) #remove unecessary white space with function 

        if (modified_counter == 1):  #notify user of how many items have been modified
            print('{0} record modified.'.format(modified_counter))
        else:
            print('{0} records modified.'.format(modified_counter))

    except FileNotFoundError:   #Error message for file not existing 
        print("!Failed to alter table {0} because it does not exist.".format(table))
    except ElementNotFoundError:
        print("!Failed to query because {0} does not exist in table {1}.".format(element, table))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#This function adds tuples into the table.  
#More specifically it runs over the user input and seperates elements with a '|' by checking the ','
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def INSERT_TABLE(table, arguments):
    try:  #If the file does not exist raise an error, otherwise open the file and append the new element      
        if not os.path.exists(table):
            raise FileNotFoundError

        arguments = arguments[arguments.find('(')+1:arguments.rfind(')')]   #obtain information in parenthesis then remove parethesis 
    
        file = open(table, "a")
        file.write('\n') #Need to write on a new line 
        for i in arguments:   #Use for loop to run through arguments and replace , with | for the new file. 
            if(i == ','):
                file.write(' | ')
            else:
                file.write(i)
        file.close()
        print('1 new record inserted.')
   
    except FileNotFoundError:   #Error message for file not existing 
        print("!Failed to alter table {0} because it does not exist.".format(table))

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
def ALTER_TABLE(table, new_element):
  
    try:  #If the file does not exist raise an error, otherwise open the file and append the new element      
        if not os.path.exists(table):
            raise FileNotFoundError
        file = open(table, "a+") #open the file for appending
        file.write(' | ' + new_element) #Adding | to match format of file 
        file.close()
        print('Table {0} modified.'.format(table))
   
    except FileNotFoundError:   #Error message for file not existing 
        print("!Failed to alter table {0} because it does not exist.".format(table))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# This function obtains the determines if a element in a tuple matches speicific requirements 
# If so, it returns true 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def WHERE_TEST (element_where_index, tuples, EQ): 
    tuples = tuples.split() #split the tuple up into words 
    tuple_check = tuples[element_where_index * 2] + ' ' + EQ  #append the desired identifer information with equation
    tuple_check = tuple_check.split() # remove whitespace
     
    if (ListToEquation(tuple_check)): #check equation
        return True 
    else:
        return False

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# This function prints out tuples with specific elements specified by the user 
# To see how tuples are inputted please look at the SELECT_TABLE function 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def SPECIFICS(tuples, output_elements, table):

    iterator = 0 #counter used to determine ending element in for loop
 
    for search in output_elements: 
        search_index = FindIndex(table, search) * 2 #get the index, account for |       
        print(tuples.split()[search_index], end='')   #use index and print 
                            
        if(iterator < len(output_elements) -1 ): #if for loop is not on last element add a | after                     
            print('|' , end='') 
        else:
            print()  #otherwise do nothing an increment the iterator for later 

        iterator = iterator + 1 #increse incrementor 

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# This function outputs contents user specified table.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def SELECT_TABLE(command):

    try: 
        
        #Declare Variables  
        index_of_from = command.index('from') #index of from 
        table = command[index_of_from + 1] #current table pulled from index of list  
        header = OBTAIN_HEADER(table) #obtain header of table 
        lines = OBTAIN_TUPLES(table) #obtain tuples of table 
        wrong_element = '' # blank string 
       
        if not os.path.exists(table): #If file does not exist raise an error
            raise FileNotFoundError
  
        if('where' in command): #if user specified 
           command_where_index = command.index('where') #index of where in user command 
           element = command[command_where_index+1] # assign element
           ElementCheck(table, element) #check element than raise element 
           where_datatype_index = FindIndex(table, command[command_where_index+1]) #obtain datatype location in table tuples
           right_half_of_EQ = ListToString(command[command_where_index+2:command_where_index+4]) #obtain right half of EQ 
           

        if (command[1] == '*' and len(command) == 4): #all tuples are outputted
            file = open(table, "r") #open file 
            print(file.read()) #output file to user  
            file.close() #close 
        
        elif (command[1] == '*' and 'where' in command): #all elements of tuples outputted with restriction 
            print(header, end='')
            for tuples in lines: #go through all the tuples in the table 
                if (WHERE_TEST (where_datatype_index, tuples, right_half_of_EQ)): #if where is found call where function
                    print(tuples, end='') #output tuple

        else: #table outputted with some type of restriction 
           
            #Declare Variables  
            outputs = command[1:index_of_from] #get user input between Select and From
            outputs = ListToString(outputs).replace(',', '') #remove all commas in the desired output lists
            outputs = outputs.strip() # remove whitespace            
            outputs = outputs.split() # convert back to string 
            
            try:
              
                for search in outputs: #check if every element specified by user esists   
                    if (search not in header): 
                        wrong_element = search 
                        raise ElementNotFoundError #if the element does not exist raise a custom exception            
                
                #declare variable 
                iterator = 0    #counter used later in for loops to determine end of | usage while printing 
                
                header_list = header.split() #make list a header 
                for search in outputs: #obtain the index of each search element 
                    head_search_index = FindIndex(table, search) * 3 #get index, account for | and extra variable                   
                    print(header_list[head_search_index], end=' ') # print header variable obtained from index
                    print(header_list[head_search_index + 1], end='') # print the datatype along with desired variable   
                    
                    if(iterator < len(outputs) -1 ): #if for loop is not on last element add a | after                                
                        print(' | ' , end='')
                    else:
                        print() #otherwise do nothing an increment the iterator for later 
                    iterator = iterator + 1 

                for tuples in lines: #go through all the tuples in the table 
                     if ('where' in command and WHERE_TEST (where_datatype_index, tuples, right_half_of_EQ)): #if where is found call where function
                        SPECIFICS(tuples, outputs, table) #Call the specifics function 
                     if ('where' not in command): #if where is not used then do not run extra check  
                        SPECIFICS(tuples, outputs, table) #Call the specifics function 
            except ElementNotFoundError:
                print("!Failed to query because {0} does not exist in table {1}.".format(wrong_element ,table))

    except FileNotFoundError:     #Error message for no file 
         print("!Failed to query table {0} because it does not exist.".format(table))       
    except ElementNotFoundError:
         print("!Failed to query because {0} does not exist in table {1}.".format(element, table))
    
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
def ListToString(list_element): 
  
    parameter_string = " " #Declare an empty string
    return (parameter_string.join(list_element))  #Return result   

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Function checks to see if single quotes used and if so keeps string in quotes case sensitive 
# Everything else is lowercased
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def lower_and_consider_quotes (sentence):
     quote_count = 0 # set the quote count to 0 
     new_sentence = '' # make empty string 
  
     for word in sentence: #run loop through all characters 
        if(word == "'"): #if quote detected increase the count 
           quote_count = quote_count + 1
        if(quote_count % 2 == 0): #anything outside the quotes are lowercased 
            new_sentence = new_sentence + word.lower()       
        else: #everything inside quotes are added without modification 
            new_sentence = new_sentence + word
            
        new_sentence = new_sentence.replace("'", '')  #remove all the single quotes
     if (quote_count % 2 != 0):
        raise WrongSingleQuotes
     return new_sentence #return the new string
 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Check to see if element requested by user even exists in the table 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    
def ElementCheck (table, element):
    header = OBTAIN_HEADER(table) #obtain header of table 
    if(element not in header): #see if element in table 
        wrong_element = element #if not, raise error 
        raise ElementNotFoundError 
           
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~   
# This function ensures that the equation is in the proper format 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def StringEquationToList(Equation_String): 
   #Declare variables     
    LEQ = '' #new list equation
    prev_letter = ''  #storing the previous letter if necessary 
        
    for letter in Equation_String:    
           
        if((letter == '=' and prev_letter == '') or letter == '>' or letter == '<'):  #check to see if char is equation 
            LEQ = LEQ + ' ' + letter + ' ' #if so, add space 
        elif(letter == '!'):  #if char is ! then it is likely the != symbol 
            prev_letter = letter #store the previous char (!)
            LEQ = LEQ + ' ' + letter  #add space to the front only  
        elif(prev_letter == '!' and letter == '='): #if != detected then add space after = sign 
            LEQ = LEQ + letter + ' '
        else: 
            LEQ = LEQ + letter #otherwise append string as usual 

    LEQ = LEQ.strip() #remove uncessary whitespace to result 
    LEQ = LEQ.split() #turn to list 
        
    if (len(LEQ) > 3): 
        raise IncorrectFormat

    return LEQ #return list of the string 

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# If equations by user are in proper format (i.e., left = right)
# but not spaced properly (e.g., left= right or left=right or left =right)
# then this function usese the StringEquationToList function to fix it and updates user_input
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def FixEQFormat(user_input):
    #Checking if equation is in proper fomat (i.e., spaces between each, if not add spaces) 
    if ('where' in user_input): 
        where_input_index = user_input.index('where') #index of where in user command 
        #where_datatype_index = FindIndex(table, command[where_input_index+1]) #obtain datatype location in table tuple         
        if (len(user_input) != where_input_index + 4): #check if the format is right for equation
            if(len(user_input) == where_input_index + 2): #index case if equation has no space 
                 Fixed_EQ = StringEquationToList(ListToString(user_input[where_input_index+1 : where_input_index + 2])) #fix format 
                 old_EQ = ListToString(user_input[where_input_index+1 : where_input_index + 2])  #obtain old equation (always on last)
                 user_input.remove(old_EQ) #remove old equation (always on last)
                 user_input = user_input + Fixed_EQ #append fixed EQ
            elif(len(user_input) == where_input_index + 3): #index case if equation has only one space 
                 Fixed_EQ = StringEquationToList(ListToString(user_input[where_input_index+1 : where_input_index + 3])) #fix format 
                 old_EQ_Left = user_input[where_input_index+1] #obtain old equation llft side (always one away from last)
                 old_EQ_Right = user_input[where_input_index+2] #obtain old equation llft side (always last)
                 user_input.remove(old_EQ_Left)  #remove left EQ
                 user_input.remove(old_EQ_Right) #remove right EQ
                 user_input = user_input + Fixed_EQ  #add fixed EQ
            else:
                 raise IncorrectFormat
    if ('set' in user_input):
        set_input_index = user_input.index('set') #index of where in user command
        if(len(user_input) !=  set_input_index + 8): #if the index is off then equation for set is off 
            if(len(user_input) == set_input_index + 6):  #index case if equation has no space 
                 Fixed_EQ = StringEquationToList(ListToString(user_input[set_input_index+1 : set_input_index + 2])) #fix format 
                 start_of_command = user_input[0 : set_input_index+1] #get everything before the left side of EQ 
                 rest_of_command = user_input[set_input_index+2 : ]  #get everything after the right side of EQ
                 user_input = start_of_command + Fixed_EQ + rest_of_command #combine with new equation in middle 
            elif(len(user_input) == set_input_index + 7): #index case if equation has only one space 
                 Fixed_EQ = StringEquationToList(ListToString(user_input[set_input_index+1 : set_input_index + 3])) #fix format 
                 start_of_command = user_input[0 : set_input_index+1] #get everything before the left side of EQ 
                 rest_of_command = user_input[set_input_index+3: ]  #get everything after the right side of EQ
                 user_input = start_of_command + Fixed_EQ + rest_of_command #combine with new equation in middle 
            else:
                 raise IncorrectFormat
    return user_input
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main function handles parsing user input  
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def Main():
    
    while (True):  #Run endless loop until user desires to exit
        user_input = '' #User input is empty string 
        user_input =  user_input.strip() #make user_input an empty list 
        user_input = user_input.split() #remove any whitespace in this list 
        
        try:
            #repeat obtaning input until user enters a ;
            while (not ListToString(user_input).endswith(';')): 
                new_input = input('') #get input from user 
                if ('--' in new_input or len(new_input) == 0):
                    new_input = '' #reset if comments detected 
                else:
                    new_input = lower_and_consider_quotes(new_input) #removes single quotes and lowers non quoted material
                    new_input.strip() #remove whitespace 
                    
                    user_input = user_input + new_input.split() #add string to list
                    if(len(user_input) == 1 and user_input[0] == '.exit'): #if user inputs .exit then end program
                        print('All done.') 
                        exit()

            user_input = ListToString(user_input).replace(';',' ') #Store all of input in a list after removing ';'
            user_input = user_input.split() #remove whitespace
            
            user_input = FixEQFormat(user_input) #fix format of user equations if needed 
        
               
            #Series of if statements act as parser 
            if (ListToString(user_input) == '.exit'):  
                print('All done.') 
                exit() 
            elif (len(user_input) == 2 and user_input[0] == 'use'):     #triggers use database function
                USE(user_input[1])
            elif (len(user_input) == 3 and user_input[0] == 'create' and user_input[1] == 'database'): #triggers create database function 
                CREATE_DATABASE(user_input[2])
            elif (len(user_input) == 3 and user_input[0] == 'drop' and user_input[1] == 'database'): #triggers drop database function  
                DROP_DATABASE(user_input[2])
            elif (len(user_input) == 3 and user_input[0] == 'drop' and user_input[1] == 'table'): #triggers drop table function
                DROP_TABLE(user_input[2])
            elif (len(user_input) > 3 and user_input[0] == 'alter' and user_input[1] == 'table' and user_input[3] == 'add'):  #triggers alter table  function
                ALTER_TABLE(user_input[2], ListToString(user_input[4:]))
            elif (len(user_input) > 3 and user_input[0] == 'create' and user_input[1] == 'table'): #triggers create table function
                CREATE_TABLE(user_input[2], ListToString(user_input[3:]))
            elif (user_input[0] == 'select' and 'from' in user_input): #triggers select table function
                SELECT_TABLE(user_input) 
            elif (len(user_input) > 3 and user_input[0] == 'insert' and user_input[1] == 'into' and ( user_input[3].startswith("values(") or user_input[3].startswith("values") ) ): #triggers insert table function
                INSERT_TABLE(user_input[2], ListToString(user_input[3:]))
            elif (len(user_input) == 10 and user_input[0] == 'update' and user_input[2] == 'set' and user_input[6] == 'where'): 
                UPDATE_TABLE(user_input[1], user_input[3:6], user_input[7:])
            elif (len(user_input) == 7 and user_input[0] == 'delete' and user_input[1] == 'from' and user_input[3] == 'where'): 
                DELETE_TUPLE(user_input[2], user_input[4:])
            elif (len(user_input) == 0 ): #If file has empty lines they are removed when being read in 
                print (" ")
            else:
                print ("!Failed, please review documentation concerning acceptable commands")
        except WrongSingleQuotes:  
            print("!Failed because of unbalanced quotations")
        except IncorrectFormat:
            print("!Failed to query because equation (or element near equation) is in wrong format.") 
        except ElementNotFoundError:
            print("!Failed to query because {0} does not exist in table {1}.".format(wrong_element ,table))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# This guarentees that the main funciton is called first
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == "__main__":      
    Main()

    
