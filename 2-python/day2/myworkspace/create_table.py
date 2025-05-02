# from sqlite3 import connect
from mysql.connector import connect

def main():
    conn_str = 'training.db'
    with open('customers_table.sql') as f:
        sql = f.read()

    # with connect(conn_str) as conn:
    with connect(user='root', password='Welcome#123', database='trainingdb') as conn:
        cur = conn.cursor()
        try:
            cur.execute(sql)
            print('Table created successfully')
        except Exception as e:
            print(e)
    

if __name__ == '__main__':
    main()