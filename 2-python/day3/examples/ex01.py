from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Create an SQLite database engine with the specified database file 'customers.db'.
# The 'echo=True' parameter enables logging of all SQL statements executed.
# This is useful for debugging and understanding the SQL queries being run.
engine = create_engine('sqlite:///customers.db', echo=True)

# Create a declarative base class. This base class is used to define ORM-mapped classes.
Base = declarative_base()

class Customer(Base):
    __tablename__ = 'customers'  # Specifies the name of the table in the database.
    
    # Define the columns of the 'customers' table.
    id = Column(Integer, primary_key=True)  
    name = Column(String(100), nullable=False)  
    email = Column(String(100), unique=True, nullable=False)  
    phone = Column(String(20), unique=True, nullable=False)  
    city = Column(String(50))  
    
    def __repr__(self):
        return f"<Customer(id={self.id}, name='{self.name}', email='{self.email}', phone='{self.phone}', city='{self.city}')>"

# Create the 'customers' table in the database if it does not already exist.
Base.metadata.create_all(engine)

# A session is used to interact with the database, such as adding, querying, updating, and deleting records.
Session = sessionmaker(bind=engine)

# Create a session instance from the session factory.
session = Session()

# Example operations with the Customer table will follow.

# 1. Create new customers
try:
    # Add first customer
    customer1 = Customer(
        name='Amit Sharma',
        email='amit.sharma@example.com',
        phone='9876543210',
        city='Mumbai'
    )
    session.add(customer1)
    
    # Add second customer
    customer2 = Customer(
        name='Priya Verma',
        email='priya.verma@example.com',
        phone='8765432109',
        city='Delhi'
    )
    session.add(customer2)
    
    # Add third customer
    customer3 = Customer(
        name='Rajesh Kumar',
        email='rajesh.kumar@example.com',
        phone='7654321098',
        city='Bangalore'
    )
    session.add(customer3)
    
    session.commit()
    print("Customers added successfully!")
    
except Exception as e:
    session.rollback()
    print(f"Error adding customers: {e}")

# 2. Query all customers
all_customers = session.query(Customer).all()
print("\nAll Customers:")
for customer in all_customers:
    print(customer)

# 3. Query customers by city
mumbai_customers = session.query(Customer).filter_by(city='Mumbai').all()
print("\nMumbai Customers:")
for customer in mumbai_customers:
    print(customer)

# 4. Update a customer
try:
    customer_to_update = session.query(Customer).filter_by(email='amit.sharma@example.com').first()
    if customer_to_update:
        customer_to_update.city = 'Pune'
        session.commit()
        print(f"\nUpdated customer: {customer_to_update}")
except Exception as e:
    session.rollback()
    print(f"Error updating customer: {e}")

# 5. Delete a customer
try:
    customer_to_delete = session.query(Customer).filter_by(email='priya.verma@example.com').first()
    if customer_to_delete:
        session.delete(customer_to_delete)
        session.commit()
        print(f"\nDeleted customer with email: priya.verma@example.com")
except Exception as e:
    session.rollback()
    print(f"Error deleting customer: {e}")

# 6. Demonstrate unique constraint with duplicate email
try:
    duplicate_email = Customer(
        name='Test User',
        email='rajesh.kumar@example.com',  # Duplicate email
        phone='6543210987',
        city='Hyderabad'
    )
    session.add(duplicate_email)
    session.commit()
except Exception as e:
    session.rollback()
    print(f"\nCorrectly failed to add customer with duplicate email: {e}")

# 7. Demonstrate unique constraint with duplicate phone
try:
    duplicate_phone = Customer(
        name='Another User',
        email='another@example.com',
        phone='7654321098',  # Duplicate phone
        city='Chennai'
    )
    session.add(duplicate_phone)
    session.commit()
except Exception as e:
    session.rollback()
    print(f"\nCorrectly failed to add customer with duplicate phone: {e}")

# 8. Query customers using more complex filters
filtered_customers = session.query(Customer).filter(
    Customer.city.in_(['Pune', 'Bangalore'])
).order_by(Customer.name).all()

print("\nCustomers in Pune or Bangalore (ordered by name):")
for customer in filtered_customers:
    print(customer)

# Close the session
session.close()