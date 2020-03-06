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

def get():

    db = "test.db"

    conn = CreateConnection(db)
    if conn == None:
        print('Connection failed')

    #SQL command to insert data
    sql = '''SELECT * FROM bookings_table;'''
    #Creates cursor
    c = conn.cursor()
    #Executes SQL command using user input
    results = c.execute(sql).fetchall()
    return results