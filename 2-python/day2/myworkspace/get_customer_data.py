# from sqlite3 import connect
from mysql.connector import connect

def get_all_customers():
    # with connect('training.db') as conn:
    with connect(user='root', password='Welcome#123', database='trainingdb') as conn:

        cur = conn.cursor()
        cur.execute('select * from customers')
        result = cur.fetchall()
        print(f'{"ID":10} {"Name":25} {"Email":35} {"Phone":10} {"City":25}')
        print('-'*114)
        for each_customer in result:
            cust_id, name, email, phone, city = each_customer
            print(f'{cust_id:10} {name:25} {email:35} {phone:10} {city:25}')

def get_one_customer():
    cust_id = int(input('Enter customer id to search: '))
    sql = 'select * from customers where id = ?'
    with connect('training.db') as conn:
        cur = conn.cursor()
        cur.execute(sql, (cust_id, ))
        c1 = cur.fetchone()
        if c1 is None:
            print(f'No customer found for id {cust_id}')
        else:
            _, name, email, phone, city = c1
            print(f'Name    : {name}')
            print(f'Email   : {email}')
            print(f'Phone   : {phone}')
            print(f'City    : {city}')

if __name__ == '__main__':
    # get_one_customer()
    get_all_customers()