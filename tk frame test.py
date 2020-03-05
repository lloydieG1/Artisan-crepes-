

#imported modules

from tkinter import *
from tkinter import ttk
import datetime
import sqlite3
from sqlite3 import Error


#SQL FUNTIONS

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


def GetFieldNames(conn, table_name):
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


def Menu(conn):
    ''' gives choice of add, view, select, update, delete or exit program
    :param conn: Connection object
    :return:
    '''
    #Outputs all options in a format assigning numbers to each option
    choice = str(input("1 - Add Data\n2 - View Data\n3 - Select Data\n4 - Update Data\n5 - Delete Data\n6 - Exit\n>>> "))

    if choice == '1':
        #Navigates to add_data function
        AddData(conn)
        
    elif choice == '2':
        #Navigates to ViewData function
        ViewData(conn)
        
    elif choice == '3':
        #Navigates to SelectData function
        SelectData(conn)
        
    elif choice == '4':
        #Navigates to Updatedata function
        Updatedata(conn)
        
    elif choice == '5':
        #Navigates to DeleteData function
        DeleteData(conn)
        
    elif choice == '6':
        #Exits program
        print("Goodbye")

    #Restarts if invalid input is given for choice
    else:
        print("Invalid Input")
##        menu()


def AddData(conn, FN, SN, LC, DT, HC, MT):
    ''' allows user to select the table to add to and asks for input for new record
    :param conn: Connection object
    :return:
    '''


    #Creates a list of all user input
    bookingdata = (FN, SN, LC, DT, HC, MT)
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
    :param membership_type: list of each item in membership_type record given as user input
    :return: booking id
    '''
    #SQL command to insert data
    sql = '''INSERT INTO bookings_table(firstname, secondname, location, eventdate, headcount, menutype)VALUES(?,?,?,?,?,?) '''
    #Creates cursor
    c = conn.cursor()
    #Executes SQL command using user input
    c.execute(sql, bookingdata)

    #Returns ID of added data
    return c.lastrowid


def CreateUser(conn, user):
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


def ViewData(conn):
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
        ViewData(conn)
        

def SelectData(conn):
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
        fields = GetFieldNames(conn, 'membership_types')
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
        fields = GetFieldNames(conn, 'users')
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

        Menu(conn)

    #Restarts if invalid input is given for table choice
    else:
        print("Invalid Input")
        SelectData(conn)

def UpdateData(conn):
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

        #Outputs all data in table to show updates - see ViewData() for more info
        c.execute('SELECT * FROM membership_types')
        records = c.fetchall()
        
        for row in records:
            print(row)

        Menu(conn)
        
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

        #Outputs all data in table to show updates - see ViewData() for more info
        c.execute('SELECT * FROM users')
        records = c.fetchall()
        
        for row in records:
            print(row)

        Menu(conn)

    #Restarts if invalid input is given for table choice
    else:
        print("Invalid Input")
        Updatedata(conn)

def DeleteData(conn):
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
        
        Menu(conn)
        
    elif which_table == '2':
        #Takes user input of ID
        ID = input("Enter ID of user you wish to delete\n>>> ")
        #SQL command to delete data based on ID
        sql = '''DELETE FROM users WHERE id=?'''
        #Executes command using user input
        c.execute(sql, (ID,))
        #Commits the changes
        conn.commit()

##        Menu(conn)

    #Restarts if invalid input is given for table choice  
    else:
        print("Invalid Input")
        DeleteData(conn)

def InitialiseTables(conn, db_file):
    ''' runs at runtime of program
        definitions of SQL commands for creating tables
        establish connection
        creates tables
        opens menu for system
        returns the database
    '''

    #SQL command creating a table called bookings_table with 3 columns
    sql_create_bookings_table = ''' CREATE TABLE IF NOT EXISTS bookings_table (
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
                                                presentationoffood text
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

#OTHER FUNCTIONS

#initializes the root window which acts as a main menu with buttons for the customer and staff menus. Arguement is previous frame so that the previous frame can be wiped.
def RootWindow(previousframe):
    #makes a list of everything on the previousframe and destroys them one by one!
    list = previousframe.pack_slaves()
    for l in list:
        l.destroy()

    frame = Frame(root)
    frame.pack()

    menuframe = Frame(root)
    menuframe.pack(side = BOTTOM)

    #when one of these buttons is pressed, the cuntion in the command parameter is called
    customerbutton = Button(frame, text='Open Customer Menu', command = lambda:OpenCustomerMenu(root))
    customerbutton.configure(bg="black")
    customerbutton.pack()

    staffbutton = Button(frame, text='Open Staff Menu', command = lambda:OpenStaffMenu(root))
    staffbutton.pack()

def destroyTuple(previousframe):	
    for frames in previousframe:       
        #makes a list of everything on the previousframe and destroys them one by one!
        print(type(frames))
        list = frames.pack_slaves()
        for l in list:    
	    l.destroy()
	
#function to instantiate customer menu
def OpenCustomerMenu(previousframe):
    #the booking frames withing frame, so this loop deals with that circumstance
    print(type(previousframe))
    if type(previousframe) == tuple:
        destroyTuple(previousframe)
    else:
        list = previousframe.pack_slaves()
        for l in list:
            l.destroy()
        
    customermenu = Frame(previousframe)
    customermenu.pack()
    title = Label(customermenu, text='Welcome to the customer menu! Please choose a service.').pack()

    returnbutton = Button(customermenu, text='Return to main menu', command = lambda:RootWindow(customermenu))
    returnbutton.pack()

    bookingform = Button(customermenu, text='Make a Booking', command = lambda:OpenBookingForm(customermenu))
    bookingform.pack()


#function to instantiate booking form frame
def OpenBookingForm(previousframe):
    #makes a list of everything on the previousframe and destroys them one by one!
    list = previousframe.pack_slaves()
    for l in list:
        l.destroy()

    #long list of all the entry fields for the make booking screen
    bookingframe = Frame(previousframe)
    bookingframe.pack()

    firstnamelabel = Label(bookingframe, text = 'Please enter your first name:')
    firstnamelabel.grid(row = 1, column = 1)
    
    firstnamefield = Entry(bookingframe)
    firstnamefield.grid(row = 1, column = 3)

    secondnamelabel = Label(bookingframe, text = 'Please enter your second name:')
    secondnamelabel.grid(row = 2, column = 1)

    secondnamefield = Entry(bookingframe)
    secondnamefield.grid(row = 2, column = 3)


    locationlabel = Label(bookingframe, text = 'Please enter the location of your booking:')
    locationlabel.grid(row = 3, column = 1)

    locationfield = Entry(bookingframe)
    locationfield.grid(row = 3, column = 3) 

    #dayframe,monthframe,yearframe are seperate frames for the month day and year, these each are packed toghether with grid in bookingframe
    dayframe = Frame(bookingframe)
    monthframe = Frame(bookingframe)
    yearframe = Frame(bookingframe)

    daylabel = Label(dayframe, text = 'day:')
    daylabel.pack( side = LEFT)


    daycombo = ttk.Combobox(dayframe, values = [
        '00', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16',
        '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31'
        ], width = 20)
    daycombo.pack()

    monthlabel = Label(monthframe, text = 'Month:')
    monthlabel.pack( side = LEFT)

    monthcombo = ttk.Combobox(monthframe, values = [
        '01','02','03','04','05','06','07','08','09','10','11','12'
        ], width = 20)
    monthcombo.pack()

    yearlabel = Label(yearframe, text = 'year:')
    yearlabel.pack( side = LEFT)

    yearcombo = ttk.Combobox(yearframe, values = [
        '2020','2021','2023','2024','2025'
        ], width = 20)
    yearcombo.pack()

    #places the 3 frames for month date and year in the grid
    dayframe.grid(row = 4, column = 1)
    monthframe.grid(row = 4, column = 2)   
    yearframe.grid(row = 4, column = 3)

    headcountlabel = Label(bookingframe, text = 'Please enter the headcount for your event:')
    headcountlabel.grid(row = 5, column = 1)
    
    headcountfield = Entry(bookingframe)
    headcountfield.grid(row = 5, column = 3)

    menutypelabel = Label(bookingframe, text = 'Please choose a menu:')
    menutypelabel.grid(row = 6, column = 1)

    menutypecombo = ttk.Combobox(bookingframe, values = [
        'Sweet Basic','Sweet and Savoury Basic', 'Sweet luxury', 'Sweet and Savoury Luxury'
        ], width = 15)
    menutypecombo.grid(row = 6, column = 3)


    getbutton = Button(bookingframe, text='Make booking',
                       command = lambda:ConfirmBookingToDatabase(firstnamefield, secondnamefield, locationfield,
                                                                 daycombo, monthcombo, yearcombo, headcountfield
                                                                 , menutypecombo))
    getbutton.grid(row = 10, column = 2)

    removalframes = (bookingframe, dayframe, monthframe, yearframe)

    returnbutton = Button(bookingframe, text='Return to customer menu', command = lambda:OpenCustomerMenu(removalframes))
    returnbutton.grid(row = 10, column = 1)

    

#this function is called by a button at the end of a  form
def ConfirmBookingToDatabase(firstnamefield, secondnamefield, locationfield, daycombo, monthcombo, yearcombo,
                             headcountfield, menutypecombo):
    FN = firstnamefield.get()
    SN = secondnamefield.get()
    LC = locationfield.get()
    HC = headcountfield.get()
    MT = menutypecombo.get()

    #getting and compiling date from combo boxes
    DAY = daycombo.get()
    MON = monthcombo.get()
    YEAR = yearcombo.get()

    DT = str(DAY + '-' + MON + '-' + YEAR)

    #Name of database file
    #'r' shows that it is passing plain text incase '\' are used in file address
    db = r"test.db"

    #create a database connection
    conn = CreateConnection(db)
    if conn == None:
        print('Connection failed')

    InitialiseTables(conn, db)
    
    AddData(conn, FN, SN, LC, DT, HC, MT)
	


    

    
    
#funtion to instantiate staff menu
def OpenStaffMenu(previousframe):
    list = previousframe.pack_slaves()
    for l in list:
        l.destroy()
    
    staffmenu = Frame(previousframe)
    staffmenu.pack()
    title = Label(staffmenu, text='Welcome to the staff menu! Please choose a service.').pack()

    calendar = Button(staffmenu, text='View Calendar', command = lambda:OpenCalendarFrame(staffmenu))
    calendar.pack()

    returnbutton = Button(staffmenu, text='Return to main menu', command = lambda:RootWindow(staffmenu))
    returnbutton.pack()



def OpenCalendarFrame(previousframe):
    #makes a list of everything on the previousframe and destroys them one by one!
    list = previousframe.pack_slaves()
    for l in list:
        l.destroy()	

    calendarframe = Frame(previousframe)
    calendarframe.pack()

    title = Label(calendarframe, text='Welcome to the calendar! See what is coming up!').pack()


    db = "test.db"

    conn = CreateConnection(db)
    if conn == None:
        print('Connection failed')

    InitialiseTables(conn, db)
    #SQL command to insert data
    sql = '''SELECT * FROM bookings_table;'''
    #Creates cursor
    c = conn.cursor()
    #Executes SQL command using user input
    results = c.execute(sql).fetchall()

    if len(results) != 0:
        tree = ttk.Treeview()
        i=0 
        for row in results:
            print(row)
            tree.insert('', 'end', i, text=row)
            i+=1
                
    else:
        print("No results found")





#Main program
    
root = Tk()
root.minsize(width = '300', height = '400')

RootWindow(root)
root.mainloop()


