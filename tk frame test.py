

#imported modules

from tkinter import *
from tkinter import ttk
# from PIL import ImageTk, Image
import datetime
from datetime import datetime as dt
# import sqlite3
# from sqlite3 import Error
from db_functions import *


#OTHER FUNCTIONS
def ClearFrame(previousframe):
    for obj in previousframe.winfo_children():
        obj.destroy()

#initializes the root window which acts as a main menu with buttons for the customer and staff menus. Arguement is previous frame so that the previous frame can be wiped.
def RootWindow(previousframe):
    #makes a list of everything on the previousframe and destroys them one by one!
    ClearFrame(previousframe)
    frame = Frame(root)
    canvas = Canvas(previousframe)  
    
    photo = PhotoImage(file="logo.gif")
    label = Label(image=photo)
    label.image =photo
    label.pack()
    # img = ImageTk.PhotoImage(Image.open("logo1.jpg"))  
    # canvas.create_image(50, 50, anchor=N, image=photo)
    # canvas.pack()  
    #img = ImageTk.PhotoImage(Image.open("True1.gif"))

    frame.pack()

    menuframe = Frame(root) #, image = img)
    menuframe.pack(side = BOTTOM)

    #when one of these buttons is pressed, the cuntion in the command parameter is called
    customerbutton = Button(frame, text='Open Customer Menu', highlightbackground= 'blue', command = lambda:OpenCustomerMenu(root))
    customerbutton.configure()
    customerbutton.pack()

    staffbutton = Button(frame, text='Open Staff Menu', highlightbackground= 'blue', command = lambda:OpenStaffMenu(root))
    staffbutton.pack()

def destroyTuple(previousframe):	
    # for frames in previousframe:       
    #     #makes a lst of everything on the previousframe and destroys them one by one!
    #     print("Destorying framse")
    #     # lst = frames.pack_slaves()
        # for l in lst:    
        #     l.destroy()
    for l in previousframe:
        l.destroy()
    # lst = previousframe.pack_slaves()
    # for l in previousframe:
    #     l.destroy()
	
#function to instantiate customer menu
def OpenCustomerMenu(previousframe):

    ClearFrame(previousframe)
        
    customermenu = Frame(previousframe)
    customermenu.pack()
    title = Label(customermenu, text='Welcome to the customer menu! Please choose a service.').pack()

    bookingform = Button(customermenu, text='Make a Booking', highlightbackground= 'blue', command = lambda:OpenBookingForm(customermenu))
    bookingform.pack()

    viewquote = Button(customermenu, text='View Quotes', highlightbackground= 'blue', command = lambda:OpenQuote(customermenu))
    viewquote.pack()

    returnbutton = Button(customermenu, text='Return to main menu', highlightbackground= 'blue', command = lambda:RootWindow(customermenu))
    returnbutton.pack()

#function to instantiate booking form frame
def OpenBookingForm(previousframe):
    #makes a lst of everything on the previousframe and destroys them one by one!
    lst = previousframe.pack_slaves()
    for l in lst:
        l.destroy()

    #long lst of all the entry fields for the make booking screen
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


    getbutton = Button(bookingframe, text='Make booking', highlightbackground= 'blue',
                       command = lambda:ConfirmBookingToDatabase(firstnamefield, secondnamefield, locationfield,
                                                                 daycombo, monthcombo, yearcombo, headcountfield
                                                                 , menutypecombo))
    getbutton.grid(row = 10, column = 2)


    returnbutton = Button(bookingframe, text='Return to customer menu', highlightbackground= 'blue', command = lambda:OpenCustomerMenu(bookingframe))
    returnbutton.grid(row = 10, column = 1)


def OpenQuote(previousframe):
    #makes a lst of everything on the previousframe and destroys them one by one!
    lst = previousframe.pack_slaves()
    for l in lst:
        l.destroy()


#this function is called by a button at the end of a  form
def ConfirmBookingToDatabase(firstnamefield, secondnamefield, locationfield, daycombo, monthcombo, yearcombo,
                             headcountfield, menutypecombo):
    
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

    ClearFrame(previousframe)
    
    staffmenu = Frame(previousframe)
    staffmenu.pack()
    title = Label(staffmenu, text='Welcome to the staff menu! Please choose a service.').pack()

    calendar = Button(staffmenu, text='View Calendar', highlightbackground= 'blue', command = lambda:OpenCalendarFrame(staffmenu))
    calendar.pack()

    reviewbooking = Button(staffmenu, text='Review Bookings', highlightbackground= 'blue', command = lambda:ReviewBooking(staffmenu))
    reviewbooking.pack()

    returnbutton = Button(staffmenu, text='Return to main menu', highlightbackground= 'blue', command = lambda:RootWindow(staffmenu))
    returnbutton.pack()



def OpenCalendarFrame(previousframe):
    #makes a lst of everything on the previousframe and destroys them one by one!

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

    #Sort results in chronological order
    date = lambda r: dt.strptime(r[0], '%d-%m-%Y')
    results.sort(key=date)
    
    tree = ttk.Treeview()
    tree["columns"]=("one","two","three")
    tree.column("#0", width=270, minwidth=270)
    tree.column("one", width=150, minwidth=150)
    tree.column("two", width=200, minwidth=100)
    tree.column("three", width=100, minwidth=100)
    tree.heading("#0",text="Date")
    tree.heading("one", text="Surname")
    tree.heading("two", text="Location")
    tree.heading("three", text="Menutype")

    if len(results) != 0:    
        i=0 
        for row in results:
            print(row)
            tree.insert('', 'end', i,text=row[0], values=row[1:])
            i+=1
        tree.pack()        
    else:
        print("No results found")

    returnbutton = Button(calendarframe, text='Return to main menu', highlightbackground= 'blue', command = lambda:RootWindow(calendarframe))
    returnbutton.pack( side = BOTTOM )


# Need a way to delete bookings with a key binding
    # tree.bind("<Backspace>", command=)

def ReviewBooking(previousframe):
    #makes a lst of everything on the previousframe and destroys them one by one!
    lst = previousframe.pack_slaves()
    for l in lst:
        l.destroy()



#Main program
root = Tk()
root.minsize(width = '300', height = '400')

RootWindow(root)
root.mainloop()


