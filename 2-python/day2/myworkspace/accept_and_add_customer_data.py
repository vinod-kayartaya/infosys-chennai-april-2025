# from sqlite3 import connect
from mysql.connector import connect

def accept_and_add_customer_data():
    print('Enter customer details: ')
    name = input('Name  : ')
    email = input('Email : ')
    phone = input('Phone : ')
    city = input('City  : ')

    with connect(user='root', password='Welcome#123', database='trainingdb') as conn:

    # with connect('training.db') as conn:  # conn represents a connection to the db from python 
        cur = conn.cursor()  # cursor is an object used for executing sql commands
        cur.execute('insert into customers(name, email, phone, city) values (%s, %s, %s, %s)', (name, email, phone, city))
        conn.commit()
        
    print('new customer record added')

if __name__ == '__main__':
    accept_and_add_customer_data()
