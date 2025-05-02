from sqlalchemy import create_engine, Column, Integer, String, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import sys

# Create engine that connects to SQLite database
engine = create_engine('sqlite:///customers.db', echo=False)  # Set echo to False to reduce output noise

# Create declarative base class
Base = declarative_base()

# Define Customer class
class Customer(Base):
    __tablename__ = 'customers'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(20), unique=True, nullable=False)
    city = Column(String(50))
    
    def __repr__(self):
        return f"<Customer(id={self.id}, name='{self.name}', email='{self.email}', phone='{self.phone}', city='{self.city}')>"

# Create the table in the database
Base.metadata.create_all(engine)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

def clear_screen():
    """Clear the terminal screen based on OS"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(title):
    """Print a header for menu sections"""
    clear_screen()
    print("=" * 50)
    print(f"{title:^50}")
    print("=" * 50)
    print()

def print_customer(customer):
    """Format and print customer information"""
    print(f"ID: {customer.id}")
    print(f"Name: {customer.name}")
    print(f"Email: {customer.email}")
    print(f"Phone: {customer.phone}")
    print(f"City: {customer.city}")

def add_customer():
    """Add a new customer to the database"""
    print_header("Add New Customer")
    
    try:
        name = input("Enter customer name: ")
        if not name.strip():
            print("Error: Name cannot be empty.")
            input("Press Enter to continue...")
            return
            
        email = input("Enter customer email: ")
        if not email.strip():
            print("Error: Email cannot be empty.")
            input("Press Enter to continue...")
            return
            
        phone = input("Enter customer phone: ")
        if not phone.strip():
            print("Error: Phone cannot be empty.")
            input("Press Enter to continue...")
            return
            
        city = input("Enter customer city (optional): ")
        
        # Create new customer
        new_customer = Customer(
            name=name,
            email=email,
            phone=phone,
            city=city
        )
        
        session.add(new_customer)
        session.commit()
        print("\nCustomer added successfully!")
        
    except Exception as e:
        session.rollback()
        print(f"\nError adding customer: {e}")
    
    input("\nPress Enter to continue...")

def list_customers():
    """Display all customers in the database"""
    print_header("Customer List")
    
    customers = session.query(Customer).all()
    
    if not customers:
        print("No customers found in the database.")
    else:
        print(f"Total customers: {len(customers)}\n")
        for customer in customers:
            print_customer(customer)
            print("-" * 30)
    
    input("\nPress Enter to continue...")

def search_customers():
    """Search for customers based on different criteria"""
    print_header("Search Customers")
    
    print("Search by:")
    print("1. ID")
    print("2. Name")
    print("3. Email")
    print("4. Phone")
    print("5. City")
    print("0. Back to main menu")
    
    choice = input("\nSelect an option: ")
    
    if choice == '0':
        return
    
    if choice not in ['1', '2', '3', '4', '5']:
        print("Invalid option selected.")
        input("Press Enter to continue...")
        return
    
    search_value = input("Enter search value: ")
    
    try:
        if choice == '1':
            if not search_value.isdigit():
                print("ID must be a number.")
                input("Press Enter to continue...")
                return
                
            customer = session.query(Customer).filter_by(id=int(search_value)).first()
            if customer:
                print("\nCustomer found:")
                print_customer(customer)
            else:
                print(f"\nNo customer found with ID: {search_value}")
                
        elif choice == '2':
            customers = session.query(Customer).filter(Customer.name.like(f"%{search_value}%")).all()
            
        elif choice == '3':
            customers = session.query(Customer).filter(Customer.email.like(f"%{search_value}%")).all()
            
        elif choice == '4':
            customers = session.query(Customer).filter(Customer.phone.like(f"%{search_value}%")).all()
            
        elif choice == '5':
            customers = session.query(Customer).filter(Customer.city.like(f"%{search_value}%")).all()
        
        if choice != '1':
            if customers:
                print(f"\nFound {len(customers)} matching customers:")
                for customer in customers:
                    print("-" * 30)
                    print_customer(customer)
            else:
                print(f"\nNo customers found matching your search.")
    
    except Exception as e:
        print(f"\nError during search: {e}")
    
    input("\nPress Enter to continue...")

def update_customer():
    """Update an existing customer's information"""
    print_header("Update Customer")
    
    email = input("Enter email of customer to update: ")
    
    try:
        customer = session.query(Customer).filter_by(email=email).first()
        
        if not customer:
            print(f"\nNo customer found with email: {email}")
            input("Press Enter to continue...")
            return
        
        print("\nCustomer found:")
        print_customer(customer)
        print("\nEnter new values (leave blank to keep current value):")
        
        name = input(f"Name [{customer.name}]: ")
        new_email = input(f"Email [{customer.email}]: ")
        phone = input(f"Phone [{customer.phone}]: ")
        city = input(f"City [{customer.city}]: ")
        
        if name.strip():
            customer.name = name
        if new_email.strip():
            customer.email = new_email
        if phone.strip():
            customer.phone = phone
        if city.strip():
            customer.city = city
        
        session.commit()
        print("\nCustomer updated successfully!")
        
    except Exception as e:
        session.rollback()
        print(f"\nError updating customer: {e}")
    
    input("\nPress Enter to continue...")

def delete_customer():
    """Delete a customer from the database"""
    print_header("Delete Customer")
    
    email = input("Enter email of customer to delete: ")
    
    try:
        customer = session.query(Customer).filter_by(email=email).first()
        
        if not customer:
            print(f"\nNo customer found with email: {email}")
            input("Press Enter to continue...")
            return
        
        print("\nCustomer to delete:")
        print_customer(customer)
        
        confirm = input("\nAre you sure you want to delete this customer? (y/n): ")
        
        if confirm.lower() == 'y':
            session.delete(customer)
            session.commit()
            print("\nCustomer deleted successfully!")
        else:
            print("\nDeletion cancelled.")
        
    except Exception as e:
        session.rollback()
        print(f"\nError deleting customer: {e}")
    
    input("\nPress Enter to continue...")

def bulk_import():
    """Import multiple customers from CSV format input"""
    print_header("Bulk Import Customers")
    
    print("Enter customer data in CSV format:")
    print("name,email,phone,city")
    print("Example: John Doe,john@example.com,555-1234,New York")
    print("Enter a blank line when finished.")
    print("\nStart entering data:")
    
    lines = []
    while True:
        line = input()
        if not line.strip():
            break
        lines.append(line)
    
    if not lines:
        print("\nNo data entered.")
        input("Press Enter to continue...")
        return
    
    success_count = 0
    fail_count = 0
    
    for line in lines:
        try:
            parts = [part.strip() for part in line.split(',')]
            
            if len(parts) < 3:
                print(f"Error: Invalid format in line: {line}")
                fail_count += 1
                continue
                
            name = parts[0]
            email = parts[1]
            phone = parts[2]
            city = parts[3] if len(parts) > 3 else ""
            
            customer = Customer(
                name=name,
                email=email,
                phone=phone,
                city=city
            )
            
            session.add(customer)
            session.commit()
            success_count += 1
            
        except Exception as e:
            session.rollback()
            print(f"Error importing line '{line}': {e}")
            fail_count += 1
    
    print(f"\nImport complete: {success_count} succeeded, {fail_count} failed")
    input("Press Enter to continue...")

def export_customers():
    """Export customers to CSV format"""
    print_header("Export Customers")
    
    customers = session.query(Customer).all()
    
    if not customers:
        print("No customers found to export.")
        input("Press Enter to continue...")
        return
    
    print("CSV Output:")
    print("name,email,phone,city")
    
    for customer in customers:
        print(f"{customer.name},{customer.email},{customer.phone},{customer.city}")
    
    print(f"\nExported {len(customers)} customers.")
    input("\nPress Enter to continue...")

def show_menu():
    """Display the main menu and handle user choices"""
    while True:
        print_header("Customer Management System")
        
        print("1. Add New Customer")
        print("2. List All Customers")
        print("3. Search Customers")
        print("4. Update Customer")
        print("5. Delete Customer")
        print("6. Bulk Import Customers")
        print("7. Export Customers")
        print("0. Exit")
        
        choice = input("\nSelect an option: ")
        
        if choice == '1':
            add_customer()
        elif choice == '2':
            list_customers()
        elif choice == '3':
            search_customers()
        elif choice == '4':
            update_customer()
        elif choice == '5':
            delete_customer()
        elif choice == '6':
            bulk_import()
        elif choice == '7':
            export_customers()
        elif choice == '0':
            print("\nExiting program. Goodbye!")
            session.close()
            sys.exit(0)
        else:
            print("\nInvalid option. Please try again.")
            input("Press Enter to continue...")

# Start the program
if __name__ == "__main__":
    show_menu()