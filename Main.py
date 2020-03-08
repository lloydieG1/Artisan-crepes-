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

    viewquote = Button(customermenu, text='View Quotes', highlightbackground= 'blue', command = lambda:OpenQuote(customermenu))
    viewquote.pack()

    returnbutton = Button(customermenu, text='Return to main menu', highlightbackground= 'blue', command = lambda:RootWindow(customermenu))
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

    reviewbookings = Button(staffmenu, text='Review Bookings', highlightbackground= 'blue', command = lambda:ReviewBookings(staffmenu))
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


    getbutton = Button(addbookingframe, text='Add booking to database', highlightbackground= 'blue',
                       command = lambda:ConfirmBookingToDatabase(firstnamefield, secondnamefield, locationfield,
                                                                 daycombo, monthcombo, yearcombo, headcountfield
                                                                 , menutypecombo))
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
    
def MakeQuote(event, arg):
    '''
    MakeQuote opens a dialogue box when pressing enter on a highlighted row from the tree
    that prompts the user for a quote.

    TODO - quotes do not save to database

    param 1 event: TODO - im really not entirely sure what event is here, pressing enter?
    param 2 arg: Tk tree
    return: none
    '''

    #arg.focus() returns the currently selected tow in the tree
    curItem = arg.focus()
    print(curItem)
    print('Im here')
    quote = tkinter.simpledialog.askinteger("Make quote...", "Quote:")
    

    ##TODO - Need a function to update tree with a quote here
    print(arg.item(curItem))

def ReviewBookings(previousframe):
    '''
    ReviewBookings displays a tree of chronilogically ordered current bookings to the user.
    You then have the option of selecting a booking with enter to provide a quote.

    param 1 previousframe: Tk frame
    return: none
    '''    
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
            print(row)
            tree.insert('', 'end', i,text=row[0], values=row[1:])
            i+=1
        tree.pack()        
    else:
        print("No results found")

    #TODO - what the fuck is this doing and why
    tree.bind("<Return>", lambda event, arg=tree: MakeQuote(event, arg))

    returnbutton = Button(reviewframe, text='Return to staff menu', highlightbackground= 'blue', command = lambda:OpenStaffMenu(reviewframe))
    returnbutton.pack( side = BOTTOM )



#Main program
root = Tk()
root.minsize(width = '300', height = '400')

RootWindow(root)
root.mainloop()
