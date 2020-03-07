import sqlite3
from sqlite3 import Error

def CreateConnection(db_file):
    ''' create a database connection to a SQLite database and check for errors
    :param db_file: database file
    :return: Connection object or None
    '''
    #Conn starts as 'None' so that if connection fails, 'None' is returned
    conn = None
    
    try:
        #attempts to connect to given database
        conn = sqlite3.connect(db_file)
        #prints version if connection is successful
        print("Connection Successful\nSQL Version =", sqlite3.version)
    
    except Error as e:
        #prints the error if one occurs
        print("Error1 = " + str(e))

    return conn


def CreateTable(conn, create_table_sql):
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


def AddData(conn, FN, SN, LC, DT, HC, MT, userid, username):
    ''' allows user to select the table to add to and asks for input for new record
    :param conn: Connection object
    :return:
    '''


    #Creates a lst of all user input
    bookingdata = (FN, SN, LC, DT, HC, MT, userid, username, 0, 0)
    #Navigates to create_membership_type function
    create = ConfirmBookingToTable(conn, bookingdata)

    #Executes if create has a value - if the function was successful
    if create is not None:
        print("Booking ID = {create}")
        
    else:
        print("Unsuccessful")

    #Commits the changes
    conn.commit()
##    menu(conn)
        

def ConfirmBookingToTable(conn, bookingdata):
    ''' create a new booking
    :param conn: Connection object
    :param membership_type: lst of each item in membership_type record given as user input
    :return: booking id
    '''
    #SQL command to insert data
    sql = '''INSERT INTO bookings_table(firstname, secondname, location, eventdate, headcount, menutype, userid, username, quote, quote_accepted)VALUES(?, ?,?,?,?,?,?,?,?,?) '''
    #Creates cursor
    c = conn.cursor()
    #Executes SQL command using user input
    c.execute(sql, bookingdata)

    #Returns ID of added data
    return c.lastrowid


def CreateUser(conn, user):
    ''' create a new user
    :param conn: Connection object
    :param user: lst of each item in user record given as user input
    :return: user id
    '''
    #SQL command to insert data
    sql = '''INSERT INTO users(first_name, last_name, age, membership_type)VALUES(?,?,?,?)'''
    #Creates cursor
    c = conn.cursor()
    #Executes SQL command using lst of user input
    c.execute(sql, user)

    #Returns ID of added data
    return c.lastrowid


def ViewData(conn):
    return 1
def SelectData(conn):
    return 0
def UpdateData(conn):
    return 0
def DeleteData(conn):
    return 0

def InitialiseTables(conn, db_file):
    ''' runs at runtime of program
        definitions of SQL commands for creating tables
        establish connection
        creates tables
        opens menu for system
        returns the database
    '''

    users_table = ''' CREATE TABLE IF NOT EXISTS users_table(
                                                userid integer PRIMARY KEY,
                                                password text,
                                                logged_in int)'''



    #SQL command creating a table called bookings_table with 3 columns
    sql_create_bookings_table = ''' CREATE TABLE IF NOT EXISTS bookings_table (
                                                userid integer NOT NULL,
                                                username text NOT NULL,
                                                firstname text NOT NULL,
                                                secondname text NOT NULL,
                                                eventdate text,
                                                location text,
                                                headcount int,
                                                menutype text,
                                                choiceofmenu text,
                                                indoororoutdoor text,
                                                utilityaccess text,
                                                deliverytocustomers text,
                                                presentationoffood text,
                                                quote INT,
                                                quote_accepted 
                                            ); '''


##    #create a database connection
##    conn = CreateConnection(db_file)
##    
    #executes if connection has been made
    if conn is not None:
        #create bookings_talbe table if it doesn't exist
        print('success')
        CreateTable(conn, sql_create_bookings_table)

    else:
        print("Error! Cannot establish the database connection so cannot add bookings.")

    #Closes connection
    conn.commit()
