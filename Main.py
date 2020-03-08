#imported modules

from tkinter import *
from tkinter import ttk
import tkinter.simpledialog
import datetime
from datetime import datetime as dt
# import sqlite3
# from sqlite3 import Error
from db_functions import *


#OTHER FUNCTIONS


def ClearFrame(previousframe):
    '''
    ClearFrame is used to clear everything from the frame that is passed into it/

    param 1 previousframe: Tkinter frame
    return: none
    '''
    #goes through each object that is a child of the frame and destorys them
    for obj in previousframe.winfo_children():
        obj.destroy()

#initializes the  root window which acts as a main menu with buttons for the customer and staff menus.
def RootWindow(previousframe):
    '''
    RootWindow is the first function that is called to initialize the first frame
    in the root Tk window. It +is called again to return to the menu. It also
    contains an image that is stored in the same directory as the script.

    param 1: Tk frame
    return: none
    '''
    #clearframe takes all objects from previous frame and destroys them
    ClearFrame(previousframe)

    #initializes frame
    frame = Frame(root)
    frame.pack()

    #stores the image as a label and packs that label
    canvas = Canvas(previousframe)   
    photo = PhotoImage(file="logo.gif")
    label = Label(image=photo)
    label.image = photo
    label.pack( side = TOP )


    #these are the two buttons on the menu, once one of the buttons are pressed a lambda (self-executing single line function)
    #calls the function that opens the customer frame or the staff frame
    customerbutton = Button(frame, text='Open Customer Menu', highlightbackground= 'blue', command = lambda:OpenCustomerMenu(root))
    customerbutton.pack( side = BOTTOM )

    staffbutton = Button(frame, text='Open Staff Menu', highlightbackground= 'blue', command = lambda:OpenStaffMenu(root))
    staffbutton.pack( side = BOTTOM )
	

def OpenCustomerMenu(previousframe):
    '''
    OpenCustomerMenu is called when the customer menu button is clicked in the root
    menu frame. It clears the previous frame and provides the customer with various
    button options.
    

    param 1 previousframe: Tk frame
    return: none
    '''

    ClearFrame(previousframe)
        
    customermenu = Frame(previousframe)
    customermenu.pack()

    #label that appears at the top of the frame
    title = Label(customermenu, text='Welcome to the customer menu! Please choose a service.').pack( side = TOP )

    bookingform = Button(customermenu, text='Make a Booking', highlightbackground= 'blue', command = lambda:OpenBookingForm(customermenu))
    bookingform.pack()

    viewquote = Button(customermenu, text='View Quotes', highlightbackground= 'blue', command = lambda:OpenCustomerQuote(customermenu))
    viewquote.pack()

    opencalendar = Button(customermenu, text='View Calendar', highlightbackground= 'blue', command = lambda:OpenCustomerCalendar(customermenu))
    opencalendar.pack()

    returnbutton = Button(customermenu, text='Return to main menu', highlightbackground= 'blue', command = lambda:RootWindow(customermenu))
    returnbutton.pack()

def OpenCustomerQuote(previousframe):
    ClearFrame(previousframe)
        
    customerquoteframe = Frame(previousframe)
    customerquoteframe.pack()
    
    db = "test.db"
    conn = CreateConnection(db)
    if conn == None:
        print('Connection failed')

    #SQL command to select data
    sql = '''SELECT eventdate, secondname FROM bookings_table;'''
    c = conn.cursor()
    results = c.execute(sql).fetchall()
    conn.close()


    #Sort results in chronological order
    date = lambda r: dt.strptime(r[0], '%d-%m-%Y')
    results.sort(key=date)
    
    tree = ttk.Treeview(customerquoteframe)
    tree["columns"]=("one","two")
    tree.column("#0", width=200, minwidth=200)
    tree.column("one", width=150, minwidth=150)
    tree.heading("#0",text="Date")
    tree.heading("one", text="Surname")


    if len(results) != 0:    
        i=0 
        for row in results:
            # print(row)
            tree.insert('', 'end', i,text=row[0], values=row[1:])
            i+=1
        tree.pack()        
    else:
        print("No results found")

    returnbutton = Button(customerquoteframe, text='Return to customer menu', highlightbackground= 'blue', command = lambda:OpenStaffMenu(reviewframe))
    returnbutton.pack( side = BOTTOM )

    userinstructions = Label(customerquoteframe, text='Select your booking and press enter to recieve a calculated quote')
    userinstructions.pack( side = BOTTOM )

    #### Magic code
    #### param 1: key press that calls lambda, param 2: lambda function that is passing event and tree, param3: function that lambda calls
    tree.bind("<Return>", lambda event, passedtree=tree: CalculateQuote(event, passedtree, customerquoteframe))

def CalculateQuote(event, passedtree, previousframe):
    calculatequoteframe = Frame(previousframe)
    calculatequoteframe.pack()
    
    db = "test.db"
    conn = CreateConnection(db)
    c = conn.cursor()

    #items itsnt actually each item in the row but a complex treeview index thingy, so these indexes need to be iterated to a list
    items = passedtree.selection()
    print(items)
    treedata = []
    for i in items:
        treedata.append(passedtree.item(i)['values'])
    print(treedata)

    #TODO - make this so it calculates the quote from headcount and menutype rather than just returning row
    selectsurname = treedata[0]
    print(selectsurname)
    #selects everything from the row selected in tree and stores in results
    selectheadcountsql = '''SELECT headcount FROM bookings_table WHERE secondname = ? ;'''
    headcountresult = c.execute(selectheadcountsql, selectsurname).fetchall()
    if len(headcountresult) != 0:
        print('Result: ',headcountresult)

    else:
        print('No results found')
    selectmenutypesql = '''SELECT menutype FROM bookings_table WHERE secondname = ? ;'''
    menutyperesult = c.execute(selectmenutypesql, selectsurname).fetchall()
    if len(menutyperesult) != 0:
        print('Result: ',menutyperesult)

    else:
        print('No results found')

    conn.commit()
    conn.close()

    #editable variables for quote calculation
    menutypecost = 0
    flatbookingfee = 20
    costpercrepe = 2
    if menutyperesult == 'Sweet Basic':
        menutypecost = 0
    elif menutyperesult == 'Sweet and Savoury Basic':
        menutypecost = 50
    elif menutyperesult == 'Sweet Luxury':
        menutypecost = 100
    elif menutyperesult == 'Sweet and Savoury Luxury':
        menutypecost = 150
    #convert from list to int
    intheadcountresult = 0
    for i in headcountresult:
        for z in i:
            intheadcountresult = z 

    

    #the calculation that decides the magnitude of the quote
    quotecalc = flatbookingfee + menutypecost + (intheadcountresult * costpercrepe)

    #label that displays quotecalc to user
    quotecalclabel = Label(calculatequoteframe, text='Your booking has been quoted for: £' + str(quotecalc))
    quotecalclabel.pack()

    

def OpenCustomerCalendar(previousframe):
    ClearFrame(previousframe)
    customercalendarframe = Frame(previousframe)
    customercalendarframe.pack()

    #connection is made to bookings_table
    db = "test.db"
    conn = CreateConnection(db)
    if conn == None:
        print('Connection failed')

    #SQL command to select data
    sql = '''SELECT eventdate FROM bookings_table;'''
    c = conn.cursor()
    results = c.execute(sql).fetchall()
    conn.close()


    #Sort results in chronological order
    date = lambda r: dt.strptime(r[0], '%d-%m-%Y')
    results.sort(key=date)
    
    tree = ttk.Treeview(customercalendarframe)
    tree["columns"]=("one")
    tree.column("#0", width=200, minwidth=200)  
    tree.heading("#0",text="Date")


    if len(results) != 0:    
        i=0 
        for row in results:
            # print(row)
            tree.insert('', 'end', i,text=row[0], values=row[1:])
            i+=1
        tree.pack()        
    else:
        print("No results found")

    returnbutton = Button(customercalendarframe, text='Return to customer menu', highlightbackground= 'blue', command = lambda:OpenCustomerMenu(customercalendarframe))
    returnbutton.pack()


def OpenBookingForm(previousframe):
    '''
    OpenBookingForm provides the user with a long form for inputting booking details
    as well as button that once pressed confirms a booking to bookings_table from
    the sql database. It is also of note that OpenBookingForm uses a grid system
    for arranging widgets rather than pack.

    param 1 previousframe: Tk frame
    return: none
    '''
    
    ClearFrame(previousframe)

    #long list of all the entry fields and combo boxes that are presented to user
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

    #everything in values will be selectable on drop-down menu
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

    #TODO - find a better way for assigning userid
    userid = 1
    username = "admin"


    getbutton = Button(bookingframe, text='Make booking', highlightbackground= 'blue',
                       command = lambda:ConfirmBookingToDatabase(bookingframe, firstnamefield, secondnamefield, locationfield,
                                                                 daycombo, monthcombo, yearcombo, headcountfield
                                                                 , menutypecombo, userid, username))
    getbutton.grid(row = 10, column = 2)


    returnbutton = Button(bookingframe, text='Return to customer menu', highlightbackground= 'blue', command = lambda:OpenCustomerMenu(bookingframe))
    returnbutton.grid(row = 10, column = 1)


def OpenQuote(previousframe):
    '''
    OpenQuote opens the quote management frame

    param 1 previousframe: Tk frame
    return: none
    '''
    ClearFrame(previousframe)


def ConfirmBookingToDatabase(previousframe, firstnamefield, secondnamefield, locationfield, daycombo, monthcombo, yearcombo,
                             headcountfield, menutypecombo, userid, username):
    '''
    ConfirmBookingToDatabase is called by a button on frames with a form.
    Once this function is called all the data from entry fields, combo boxes,
    etc are retrieved into variables and saved to sql bookings_table

    param 1 previousframe: Tk frame
    param 2 firstnamefield: Entry field
    param 3 secondnamefield: Entry field
    param 4 locationfield: Entry field
    param 5 daycombo: Combo box
    param 6 monthcombo: Combo box
    param 7 yearcombo: Combo box
    param 8 headcountfield: Entry field
    param 9 menutypecombo: Combo box
    param 10 userid: Entry field
    param 11 username: Entry field
    
    return: none
    '''
    confirmBookingFrame = Frame(root)
    confirmBookingFrame.pack()

    title = Label(confirmBookingFrame, text='Thankyou for your request. Your booking is being processed...').pack()

    FN = firstnamefield.get()
    SN = secondnamefield.get()
    LC = locationfield.get()
    HC = headcountfield.get()
    MT = menutypecombo.get()

    #getting and compiling date from combo boxes
    DAY = daycombo.get()
    MON = monthcombo.get()
    YEAR = yearcombo.get()

    #this compiles the date into a format that can be understood by datetime
    DT = str(DAY + '-' + MON + '-' + YEAR)

    #Name of database file
    #'r' shows that it is passing plain text incase '\' are used in file address
    db = r"test.db"

    #create a database connection
    conn = CreateConnection(db)
    InitialiseTables(conn, db)

    if conn == None:
        print('Connection failed')

    #Calls AddData from the db functions file and passes all the retrieved variables from the form and saves in bookings_table
    AddData(conn, FN, SN, LC, DT, HC, MT, userid, username)
    ClearFrame(previousframe)

	

def OpenStaffMenu(previousframe):
    '''
    OpenStaffMenu clears the previous frame and presents a new frame with options for
    staff to click.

    param 1 previousframe: Tk frame
    return: none
    '''
    ClearFrame(previousframe)
    
    staffmenu = Frame(previousframe)
    staffmenu.pack()
    title = Label(staffmenu, text='Welcome to the staff menu! Please choose a service.').pack()

    calendar = Button(staffmenu, text='View Calendar', highlightbackground= 'blue', command = lambda:OpenCalendarFrame(staffmenu))
    calendar.pack()

    reviewbookings = Button(staffmenu, text='Delete Bookings', highlightbackground= 'blue', command = lambda:ReviewBookings(staffmenu))
    reviewbookings.pack()

    addbookingbutton = Button(staffmenu, text='Add booking', highlightbackground= 'blue', command = lambda:OpenAddBookingForm(staffmenu))
    addbookingbutton.pack()
    
    returnbutton = Button(staffmenu, text='Return to main menu', highlightbackground= 'blue', command = lambda:RootWindow(staffmenu))
    returnbutton.pack()



def OpenAddBookingForm(previousframe):
    '''
    OpenAddBookingForm provides the user with a long form for inputting booking details
    as well as button that once pressed confirms a booking to bookings_table from
    the sql database. It is also of note that OpenBookingForm uses a grid system
    for arranging widgets rather than pack.

    param 1 previousframe: Tk frame
    return: none
    '''
    
    ClearFrame(previousframe)
    
    #long lst of all the entry fields for the make booking screen
    addbookingframe = Frame(previousframe)
    addbookingframe.pack()

    firstnamelabel = Label(addbookingframe, text = 'Please enter your first name:')
    firstnamelabel.grid(row = 1, column = 1)
    
    firstnamefield = Entry(addbookingframe)
    firstnamefield.grid(row = 1, column = 3)

    secondnamelabel = Label(addbookingframe, text = 'Please enter your second name:')
    secondnamelabel.grid(row = 2, column = 1)

    secondnamefield = Entry(addbookingframe)
    secondnamefield.grid(row = 2, column = 3)


    locationlabel = Label(addbookingframe, text = 'Please enter the location of your booking:')
    locationlabel.grid(row = 3, column = 1)

    locationfield = Entry(addbookingframe)
    locationfield.grid(row = 3, column = 3) 

    #dayframe,monthframe,yearframe are seperate frames for the month day and year, these each are packed toghether with grid in addbookingframe
    dayframe = Frame(addbookingframe)
    monthframe = Frame(addbookingframe)
    yearframe = Frame(addbookingframe)

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

    headcountlabel = Label(addbookingframe, text = 'Please enter the headcount for your event:')
    headcountlabel.grid(row = 5, column = 1)
    
    headcountfield = Entry(addbookingframe)
    headcountfield.grid(row = 5, column = 3)

    menutypelabel = Label(addbookingframe, text = 'Please choose a menu:')
    menutypelabel.grid(row = 6, column = 1)

    menutypecombo = ttk.Combobox(addbookingframe, values = [
        'Sweet Basic','Sweet and Savoury Basic', 'Sweet luxury', 'Sweet and Savoury Luxury'
        ], width = 15)
    menutypecombo.grid(row = 6, column = 3)


    #TODO - find a better way for assigning userid
    userid = 1
    username = "admin"


    getbutton = Button(addbookingframe, text='Add booking to database', highlightbackground= 'blue',
                       command = lambda:ConfirmBookingToDatabase(addbookingframe, firstnamefield, secondnamefield, locationfield,
                                         daycombo, monthcombo, yearcombo, headcountfield
                                         , menutypecombo, userid, username))
    getbutton.grid(row = 10, column = 2)


    returnbutton = Button(addbookingframe, text='Return to staff menu', highlightbackground= 'blue', command = lambda:OpenStaffMenu(addbookingframe))
    returnbutton.grid(row = 10, column = 1)



def OpenCalendarFrame(previousframe):
    '''
    OpenCalendaFrame uses a Tkinter tree to conveniently display all current bookings in bookings_table

    param 1 previousframe: Tk frame
    return: none
    '''
    ClearFrame(previousframe)

    calendarframe = Frame(previousframe)
    calendarframe.pack()

    title = Label(calendarframe, text='Welcome to the calendar! See what is coming up!').pack()


    db = "test.db"

    conn = CreateConnection(db)
    if conn == None:
        print('Connection failed')

    #SQL command to select data
    sql = '''SELECT eventdate, secondname, location menutype from bookings_table;'''
    #Creates cursor
    c = conn.cursor()
    #Executes SQL command using user input
    results = c.execute(sql).fetchall()

    #Sorts results in chronological order (using dates from date field)
    date = lambda r: dt.strptime(r[0], '%d-%m-%Y')
    results.sort(key=date)
    
    tree = ttk.Treeview(calendarframe)
    tree["columns"]=("one","two","three")
    tree.column("#0", width=270, minwidth=270)
    tree.column("one", width=150, minwidth=150)
    tree.column("two", width=200, minwidth=100)
    tree.column("three", width=100, minwidth=100)
    tree.heading("#0",text="Date")
    tree.heading("one", text="Surname")
    tree.heading("two", text="Location")
    tree.heading("three", text="Menutype")

    #if there are results this for loop inserts each row into a new row in the tree
    if len(results) != 0:    
        i=0 
        for row in results:
            print(row)
            tree.insert('', 'end', i,text=row[0], values=row[1:])
            i+=1
        tree.pack()        
    else:
        print("No results found")

    returnbutton = Button(calendarframe, text='Return to main menu', highlightbackground= 'blue', command = lambda:OpenStaffMenu(calendarframe))
    returnbutton.pack( side = BOTTOM )


#TODO - Need a way to delete bookings with a key binding
    # tree.bind("<Backspace>", command=)


def DeleteBooking(event, passedtree):
    db = "test.db"
    conn = CreateConnection(db)
    c = conn.cursor()

    #items itsnt actually each item in the row but a complex treeview index thingy, so these indexes need to be iterated to a list
    items = passedtree.selection()
    print(items)
    bookingdata = []
    for i in items:
        bookingdata.append(passedtree.item(i)['values'])
    print(bookingdata)
    
    for booking in bookingdata:
        deletesurname = booking[0]
        print(deletesurname)
        deletedatasql = '''DELETE from bookings_table WHERE secondname=?; '''
        c.execute(deletedatasql, (deletesurname,))
        print("Deleted ", deletesurname)
        conn.commit()
        conn.close()
            

##    rid = arg.get_children()
    #Rids of the objects currently in the tree
##    for i in rid:
##        if i != None:
##            arg.delete(rid)

##    secondname = arg.set(rid)['one']

##    print(arg)
##    print('Im here')

##    sql = '''DELETE from bookings_table WHERE secondname = ? ; ''' 
##
##    arg.delete(secondname)
##

##    confirmBookingFrame = Frame(root)
##    confirmBookingFrame.pack()
##
##    title = Label(confirmBookingFrame, text='Thankyou for your request. Your booking is being processed...').pack()

##    ClearFrame(passedtree)

def ReviewBookings(previousframe):
    ClearFrame(previousframe)
    reviewframe = Frame(previousframe)
    reviewframe.pack()

    db = "test.db"
    conn = CreateConnection(db)
    if conn == None:
        print('Connection failed')

    #SQL command to select data
    sql = '''SELECT eventdate, secondname, location, menutype, userid FROM bookings_table WHERE quote = 0 AND quote_accepted = 0;'''
    c = conn.cursor()
    results = c.execute(sql).fetchall()
    conn.close()


    #Sort results in chronological order
    date = lambda r: dt.strptime(r[0], '%d-%m-%Y')
    results.sort(key=date)
    
    tree = ttk.Treeview(reviewframe)
    tree["columns"]=("one","two","three","four")
    tree.column("#0", width=200, minwidth=200)
    tree.column("one", width=150, minwidth=150)
    tree.column("two", width=200, minwidth=100)
    tree.column("three", width=100, minwidth=100)
    tree.column("four", width=30, minwidth=30)
    tree.heading("#0",text="Date")
    tree.heading("one", text="Surname")
    tree.heading("two", text="Location")
    tree.heading("three", text="Menutype")
    tree.heading("four", text="Userid")

    if len(results) != 0:    
        i=0 
        for row in results:
            # print(row)
            tree.insert('', 'end', i,text=row[0], values=row[1:])
            i+=1
        tree.pack()        
    else:
        print("No results found")
    
    #### Magic code
    #### param 1: key press that calls lambda, param 2: lambda function that is passing event and tree, param3: function that lambda calls
    tree.bind("<BackSpace>", lambda event, passedtree=tree : DeleteBooking(event, passedtree))

    returnbutton = Button(reviewframe, text='Return to staff menu', highlightbackground= 'blue', command = lambda:OpenStaffMenu(reviewframe))
    returnbutton.pack( side = BOTTOM )

    userinstructions = Label(reviewframe, text='Highlight a booking and press backspace to remove it from the database')
    userinstructions.pack( side = BOTTOM )



#Main program
root = Tk()
root.minsize(width = '300', height = '400')

RootWindow(root)
root.mainloop()
