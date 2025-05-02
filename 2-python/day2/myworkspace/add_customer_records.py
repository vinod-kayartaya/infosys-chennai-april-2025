# from sqlite3 import connect
from mysql.connector import connect

def add_records():
    # with connect('training.db') as conn:  # conn represents a connection to the db from python 
    with connect(user='root', password='Welcome#123', database='trainingdb') as conn:
        with open('customers.csv') as f:
            f.readline() # skip the first line, since it is a header
            cur = conn.cursor()  # cursor is an object used for executing sql commands
            for each_line in f:
                fields = each_line.strip().split(',')
                try:
                    cur.execute('insert into customers values (%s, %s, %s, %s, %s)', fields)
                except:
                    print('error inserting')
                    pass
            conn.commit()

    print('all customer records added')

if __name__ == '__main__':
    add_records()


# insert into customers values (1, 'Vinod', 'vinod@vinod.co', '9731424784', 'Bangalore');
# insert into customers values (?, ?, ?, ?, ?) (1, 'Vinod', 'vinod@vinod.co''9731424784', 'Bangalore');

# for csv data:
# e-clipboard.web.app
# 9rxPlr