from sqlalchemy import create_engine, Column, Integer, String, or_
from sqlalchemy.orm import declarative_base,  sessionmaker

# connection string to work with MySQL
# sqlite+mysql-connector-python:///root:Welcome#123@localhost:3306/trainingdb
# sqlite+pymysql:///root:Welcome#123@localhost:3306/trainingdb
# pip install pymysql cryptography
# engine = create_engine('mysql+pymysql://root:Welcome#123@localhost:3306/infosysdb')

engine = create_engine('sqlite:///customers.db', echo=False)
Base = declarative_base() # this returns a class, which provides all high level functions to perform DB operations (such as INSERT/UPDATE/DELETE)

class Customer(Base):
    __tablename__ = 'customers'  
    
    id = Column(Integer, primary_key=True)  
    name = Column(String(100), nullable=False)  
    email = Column(String(100), unique=True, nullable=False)  
    phone = Column(String(20), unique=True, nullable=False)  
    city = Column(String(50))  
    
    def __repr__(self):
        return f"Customer(id={self.id}, name='{self.name}', email='{self.email}', phone='{self.phone}', city='{self.city}')"
    
    def get_as_dict(self):
        return dict(
            id=self.id, 
            name=self.name, 
            city=self.city, 
            email=self.email, 
            phone=self.phone)
    
    def print(self):
        print(f'Name  : {self.id}')
        print(f'Name  : {self.name}')
        print(f'Email : {self.email}')
        print(f'Phone : {self.phone}')
        print(f'City  : {self.city}')
        print()

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine) # returns a class for us to create session objects

def accept_and_add_customer_data():
    print('Enter new customer details:')
    name = input('Name  :')
    email = input('Email :')
    phone = input('Phone :')
    city = input('City  :')

    # create a new customer object
    c1 = Customer(name=name, email=email, phone=phone, city=city)
    # create a session object; represents an active DB connection
    with Session() as session:
        session.add(c1)
        session.commit()  # creates SQL cmds (INSERT/UPDATE/DELETE); sends to the DB for execution


def display_all_customers():
    with Session() as session:
        for c in session.query(Customer).all():
            c.print()


def display_customers_from_city():
    search_city = input('Enter city to search for customers: ')

    with Session() as session:
        customers = session.query(Customer) \
            .filter_by(city=search_city) \
            .all()
        
        if len(customers) == 0:
            print(f'No customers found in the city {search_city}')
            return
        
        print(f'Customers from the city of {search_city}:')
        for c in customers:
            c.print()

def search_by_email_or_phone():
    email = input('Enter email: ')
    phone = input('Enter phone: ')
    with Session() as session:
        # customers = session.query(Customer).filter(
        #     or_(Customer.email==email, Customer.phone==phone)
        # ).all()

        customers = session.query(Customer).filter(
            (Customer.email==email) | (Customer.phone==phone)
        ).all()

        for c in customers:
            print(c)

def search_by_cities():
    cities = input('Enter cities to search (comma separated): ').split(',')
    cities = [c.strip() for c in cities]
    with Session() as session:
        customers = session.query(Customer).filter(Customer.city.in_(cities)).all()
        for c in customers:
            print(c)

def search_by_id_and_update():
    id_to_search = input('Enter customer id to search: ')
    with Session() as session:
        c1 = session.query(Customer).filter_by(id=id_to_search).first()
    
        if not c1:
            print(f'No customer data found for id "{id_to_search}"')
            return
        
        print('Enter values to change (or just press enter to keep the same):')
        name = input(f'Name [{c1.name}]: ')
        email = input(f'Name [{c1.email}]: ')
        phone = input(f'Name [{c1.phone}]: ')
        city = input(f'Name [{c1.city}]: ')

        # modify the value of a session object directly and commit
        # when an entity object in the session is modified, it is considered as `dirty`
        # during session.commit(), `dirty` objects result in sql update command
        if name.strip(): c1.name = name
        if email.strip(): c1.email = email
        if phone.strip(): c1.phone = phone
        if city.strip(): c1.city = city

        try:
            session.commit()
            print('Data updated successfully')
        except Exception as e:
            print(f'There was an error: {e}')


def search_by_email_and_delete():
    email_to_search = input('Enter customer email to search: ')
    with Session() as session:
        c1 = session.query(Customer).filter_by(email=email_to_search).first()
    
        if not c1:
            print(f'No customer data found for email id "{email_to_search}"')
            return
        
        print('Customer data found:')
        c1.print()

        choice = input('Are you sure you want to delete this? (yes/[no]) ')
        if choice == 'yes':
            try:
                session.delete(c1)
                session.commit()
                print('Deleted successfully!')
            except Exception as e:
                print(f'Something went wrong - {e}')
                session.rollback()

if __name__ == '__main__':
    search_by_email_or_phone()
    # search_by_cities()
    # search_by_id_and_update()
    # display_customers_from_city()
    # search_by_email_and_delete()
    # accept_and_add_customer_data()
    # display_all_customers()