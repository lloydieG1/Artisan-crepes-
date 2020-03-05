#import MySQLdb
import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    ''' create a database connection to a SQLite database and check for errors
    :param db_file: database file
    :return: Connection object or None
    '''
    #Conn starts as 'None' so that if connection fails, 'None' is returned
    conn = None
    
    try:
        #attempts to connect to given database
        conn = sqlite3.connect(db_file)
        #prints version is connection is successful
        print("Connection Successful\nSQL Version =", sqlite3.version)
    
    except Error as e:
        #prints the error if one occurs
        print("Error1 = " + str(e))

    return conn

def create_table(conn, create_table_sql):
    ''' create a table in the database given with an SQL statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE sql statement
    :return:
    '''
    
    try:
        #create sql cursor
        c = conn.cursor()
        #executes the command passed by parameter create_table_sql
        c.execute(create_table_sql)
        
    except Error as e:
        #prints the error if one occurs
        print("Error2 = " + str(e))

def get_field_names(conn, table_name):
    ''' get field names for a specific table
    :param conn: Connection object
    :param table_name: the table that the function will get field names of
    :return: list of field names
    '''
    #Creates cursor
    c = conn.cursor()
    #Gets all information of table, use .format as field names cannot be passed to SQL using '?'
    table_info = c.execute('''PRAGMA table_info({})'''.format(table_name))
    fields = []

    #Adds each field name to list fields, table names are in index 1 of each record in table_info
    for l in table_info:
        fields.append(l[1])
        
    return fields

def menu(conn):
    ''' gives choice of add, view, select, update, delete or exit program
    :param conn: Connection object
    :return:
    '''
    #Outputs all options in a format assigning numbers to each option
    choice = str(input("1 - Add Data\n2 - View Data\n3 - Select Data\n4 - Update Data\n5 - Delete Data\n6 - Exit\n>>> "))

    if choice == '1':
        #Navigates to add_data function
        add_data(conn)
        
    elif choice == '2':
        #Navigates to view_data function
        view_data(conn)
        
    elif choice == '3':
        #Navigates to select_data function
        select_data(conn)
        
    elif choice == '4':
        #Navigates to update_data function
        update_data(conn)
        
    elif choice == '5':
        #Navigates to delete_data function
        delete_data(conn)
        
    elif choice == '6':
        #Exits program
        print("Goodbye")

    #Restarts if invalid input is given for choice
    else:
        print("Invalid Input")
        menu()

def add_data(conn):
    ''' allows user to select the table to add to and asks for input for new record
    :param conn: Connection object
    :return:
    '''
    #Choice for table to add to
    which_table = str(input("Would you like to add data to:\n1 - membership_types\n2 - users\n>>> "))

    if which_table == '1':
        #All user input entries
        name = input("Enter membership name\n>>> ")
        length_months = input("Enter length of membership in months\n>>> ")
        price = input("Enter price of membership per month\n>>> ")
        gym_access = input("Does this allow access to the Gym? (yes/no)\n>>> ").lower()
        studio_access = input("Does this allow access to the Studio? (yes/no)\n>>> ").lower()

        #Creates a list of all user input
        membership_type = (name, length_months, price, gym_access, studio_access)
        #Navigates to create_membership_type function
        create = create_membership_type(conn, membership_type)

        #Executes if create has a value - if the function was successful
        if create is not None:
            print(f"Membership ID = {create}")
            
        else:
            print("Unsuccessful")

        #Commits the changes
        conn.commit()
        menu(conn)
        
    elif which_table == '2':
        #All user input entries
        first_name = input("Enter first name\n>>> ")
        last_name = input("Enter last name\n>>> ")
        age = input("Enter age\n>>> ")
        membership_type = input("Choose membership type (Bronze/Silver/Gold)\n>>> ")

        #Creates a list of all user input
        user = (first_name, last_name, age, membership_type)
        #Navigates to create_user function
        create = create_user(conn, user)

        #Executes if create has a value - if the function was successful
        if create is not None:
            print(f"User ID = {create}")
            
        else:
            print("Unsuccessful")

        #Commits the changes
        conn.commit()
        menu(conn)

    #Restarts if invalid input is given for table choice    
    else:
        print("Invalid input")
        add_data(conn)

def create_membership_type(conn, membership_type):
    ''' create a new type of membership
    :param conn: Connection object
    :param membership_type: list of each item in membership_type record given as user input
    :return: membership id
    '''
    #SQL command to insert data
    sql = '''INSERT INTO membership_types(name, length_months, price, gym_access, studio_access)VALUES(?,?,?,?,?) '''
    #Creates cursor
    c = conn.cursor()
    #Executes SQL command using user input
    c.execute(sql, membership_type)

    #Returns ID of added data
    return c.lastrowid
    
def create_user(conn, user):
    ''' create a new user
    :param conn: Connection object
    :param user: list of each item in user record given as user input
    :return: user id
    '''
    #SQL command to insert data
    sql = '''INSERT INTO users(first_name, last_name, age, membership_type)VALUES(?,?,?,?)'''
    #Creates cursor
    c = conn.cursor()
    #Executes SQL command using list of user input
    c.execute(sql, user)

    #Returns ID of added data
    return c.lastrowid

def view_data(conn):
    ''' allows the user to select which table to view
        prints data record by record
    :param conn: Connecion object
    :return:
    '''
    #Choice for table to view
    which_table = str(input("Would you like to view:\n1 - membership_types\n2 - users\n>>> "))
    #Creates cursor
    c = conn.cursor()
    
    if which_table == '1':
        #SQL command to select all from table
        c.execute('SELECT * FROM membership_types')
        #Stores in a variable
        records = c.fetchall()

        #Outputs record by record
        for row in records:
            print(row)

        menu(conn)
            
    elif which_table == '2':
        #SQL command to select all data
        c.execute('SELECT * FROM users')
        #Stores in a variable
        records = c.fetchall()

        #Outputs record by record
        for row in records:
            print(row)

        menu(conn)

    #Restarts if invalid input is given for table choice        
    else:
        print("Invalid Input")
        view_data(conn)
        
def select_data(conn):
    ''' allows user to select which table to select data from
        allows user to decide which search category to use
        allows user to enter search term
        prints all records matching criteria
    :param conn: Connecion object
    :return:
    '''
    #Choice for table to select from
    which_table = str(input("Would you like to select data from:\n1 - membership_types\n2 - users\n>>> "))
    #Creates cursor
    c = conn.cursor()
    
    if which_table == '1':
        #Uses get_field_names function to get field names
        fields = get_field_names(conn, 'membership_types')
        #User input to select search category
        which_field = input("Which field would you like to search in?\n1 - ID\n2 - Name\n3 - Length (in months)\n4 - Price\n5 - Gym Access?\n6 - Studio Access?\n>>> ")
        #User input for term to search for
        search_term = input("Enter term to search for\n>>> ")
        
        #Loops through field names
        for i in range(1, len(fields)+1):

            #Assigns search category based on user input and index of list
            if int(which_field) == i:
                which_field = fields[i-1]
                break

        #SQL command to select using the search category and search terms from user input
        results = c.execute('''SELECT * FROM membership_types WHERE {}=?'''.format(which_field), (search_term,)).fetchall()
        
        #Outputs results if there are any
        if len(results) != 0:
            print("Results:")
            
            for row in results:
                print(row)
                
        else:
            print("No results found")

        menu(conn)
            
    elif which_table == '2':
        #Uses get_field_names function to get field names
        fields = get_field_names(conn, 'users')
        #User input to select search category
        which_field = input("Which field would you like to search in?\n1 - ID\n2 - First Name\n3 - Surname\n4 - Age\n5 - Membership Type\n>>> ")
        #User input for term to search for
        search_term = input("Enter term to search for\n>>> ")

        #Loops through field names
        for i in range(1, len(fields)+1):

            #Assigns search category based on user input and index of list
            if int(which_field) == i:
                which_field = fields[i-1]
                break
            
        #SQL command to select using the search category and search terms from user input
        results = c.execute('''SELECT * FROM users WHERE {}=?'''.format(which_field), (search_term,)).fetchall()

        #Outputs results if there are any
        if len(results) != 0:
            print("Results:")
            
            for row in results:
                print(row)
                
        else:
            print("No results found")

        menu(conn)

    #Restarts if invalid input is given for table choice
    else:
        print("Invalid Input")
        select_data(conn)

def update_data(conn):
    ''' allows user to select which table to update data in
        allows user to select record to update by record id
        allows user to enter new data for record
        prints updated data of table record by record
    :param conn: Connecion object
    :return:
    '''
    #Choice for table to update data in
    which_table = str(input("Would you like to update data from:\n1 - membership_types\n2 - users\n>>> "))
    #Creates cursor
    c = conn.cursor()
    
    if which_table == '1':
        #All user input entries
        ID = input("Enter ID of membership you wish to update\n>>> ")
        name = input("Enter membership name\n>>> ")
        length_months = input("Enter length of membership in months\n>>> ")
        price = input("Enter price of membership per month\n>>> ")
        gym_access = input("Does this allow access to the Gym? (yes/no)\n>>> ").lower()
        studio_access = input("Does this allow access to the Studio? (yes/no)\n>>> ").lower()

        #Creates a list of all user input
        membership_type = (name, length_months, price, gym_access, studio_access, ID)
        #SQL command to update record based on id
        sql = '''UPDATE membership_types SET name = ?, len_months = ?, price = ?, gym_access = ?, studio_access = ? WHERE id = ?'''

        #Execute command using user input
        c.execute(sql, membership_type)
        #Commits the changes
        conn.commit()

        #Outputs all data in table to show updates - see view_data() for more info
        c.execute('SELECT * FROM membership_types')
        records = c.fetchall()
        
        for row in records:
            print(row)

        menu(conn)
        
    elif which_table == '2':
        #All user input entries
        ID = input("Enter ID of user you wish to update\n>>> ")
        first_name = input("Enter first name\n>>> ")
        last_name = input("Enter last name\n>>> ")
        age = input("Enter age\n>>> ")
        membership_type = input("Choose membership type (Bronze/Silver/Gold)\n>>> ")

        #Creates a list of all user input
        user = (first_name, last_name, age, membership_type, ID)
        #SQL command to update record based on id
        sql = '''UPDATE users SET first_name = ?, last_name = ?, age = ?, membership_type = ? WHERE id = ?'''

        #Execute command using user input
        c.execute(sql, user)
        #Commits the changes
        conn.commit()

        #Outputs all data in table to show updates - see view_data() for more info
        c.execute('SELECT * FROM users')
        records = c.fetchall()
        
        for row in records:
            print(row)

        menu(conn)

    #Restarts if invalid input is given for table choice
    else:
        print("Invalid Input")
        update_data(conn)

def delete_data(conn):
    ''' allows user to select which table to delete data from
        allows user to delete record based on record id
    :param conn: Connecion object
    :return:
    '''
    #Choice for table to delete from
    which_table = str(input("Would you like to delete data from:\n1 - membership_types\n2 - users\n>>> "))
    #Creates cursor
    c = conn.cursor()
    
    if which_table == '1':
        #Takes user input of ID
        ID = input("Enter ID of membership you wish to delete\n>>> ")
        #SQL command to delete data based on ID
        sql = '''DELETE FROM membership_types WHERE id=?'''
        #Executes command using user input
        c.execute(sql, (ID,))
        #Commits the changes
        conn.commit()
        
        menu(conn)
        
    elif which_table == '2':
        #Takes user input of ID
        ID = input("Enter ID of user you wish to delete\n>>> ")
        #SQL command to delete data based on ID
        sql = '''DELETE FROM users WHERE id=?'''
        #Executes command using user input
        c.execute(sql, (ID,))
        #Commits the changes
        conn.commit()

        menu(conn)

    #Restarts if invalid input is given for table choice  
    else:
        print("Invalid Input")
        delete_data(conn)

def main():
    ''' runs at runtime of program
        definitions of SQL commands for creating tables
        establish connection
        creates tables
        opens menu for system
        closes connection
    '''
    #Name of database file
    #'r' shows that it is passing plain text incase '\' are used in file address
    db = r"test.db"

    #SQL command creating a table called membership_types with 6 columns
    sql_create_membership_types_table = ''' CREATE TABLE IF NOT EXISTS membership_types (
                                                id integer PRIMARY KEY,
                                                name text NOT NULL,
                                                length_months integer NOT NULL,
                                                price text NOT NULL,
                                                gym_access text,
                                                studio_access text
                                            ); '''
    
    #SQL command creating a table called users with 5 columns
    sql_create_users_table = '''CREATE TABLE IF NOT EXISTS users (
                                    id integer PRIMARY KEY,
                                    first_name text NOT NULL,
                                    last_name text NOT NULL,
                                    age integer NOT NULL,
                                    membership_type text NOT NULL,
                                    FOREIGN KEY (membership_type) REFERENCES membership_types (id)
                                ); '''

    #create a database connection
    conn = create_connection(db)
    
    #executes if connection has been made
    if conn is not None:
        #create membership_types table if it doesn't exist
        create_table(conn, sql_create_membership_types_table)
        #create users table if it doesn't exist
        create_table(conn, sql_create_users_table)

        menu(conn)

    else:
        print("Error! Cannot establish the database connection so cannot add mamberships.")
    
    #Closes connection
    conn.close()

#Calls main() if not imported as a module
if __name__ == "__main__":
    main()


