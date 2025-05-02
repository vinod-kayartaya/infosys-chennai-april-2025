# Python SQLite Customer Management System

## Assignment Overview

Create a command-line interface (CLI) application in Python that manages customer data using SQLite database. The application should provide a menu-driven interface to perform CRUD (Create, Read, Update, Delete) operations on a customers table.

## Requirements

### Database Schema

Create a SQLite database with a table named `customers` having the following structure:

```sql
CREATE TABLE customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT,
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Features

The application should provide the following functionality:

1. **Main Menu Display**

   - Show a clear, numbered menu with all available operations
   - Handle invalid input gracefully
   - Provide an option to exit the application

2. **Create Customer (C)**

   - Add new customer records
   - Validate email format
   - Ensure phone number format is correct
   - Handle duplicate email addresses

3. **Read Customer Data (R)**

   - View all customers
   - Search customer by ID
   - Search customer by email
   - Filter customers by name pattern

4. **Update Customer (U)**

   - Update customer details by ID
   - Allow partial updates (only specified fields)
   - Validate updated email if changed
   - Show before/after data

5. **Delete Customer (D)**
   - Delete customer by ID
   - Confirm before deletion
   - Show deleted customer details

### Technical Requirements

1. **Code Structure**

   - Use Object-Oriented Programming (OOP)
   - Implement proper error handling
   - Follow PEP 8 style guidelines
   - Include docstrings and comments

2. **Database Operations**

   - Use parameterized queries to prevent SQL injection
   - Implement proper connection handling
   - Use context managers for database operations

3. **Input Validation**
   - Validate all user inputs
   - Provide clear error messages
   - Implement data sanitization

## Sample Menu Interface

```
=== Customer Management System ===
    0. Exit
    1. Add New Customer
    2. View All Customers
    3. Search Customer by ID
    4. Search Customer by Email
    5. Update Customer
    6. Delete Customer
    Enter your choice (0-6):
```

## More challenges

1. **Data Export/Import**

   - Export customer data to CSV
   - Import customer data from CSV

2. **Advanced Search**

   - Search by multiple criteria
   - Sort results by different fields

3. **Logging**

   - Implement logging for all operations
   - Log errors and important events

## Submission Guidelines

1. Create a GitHub repository for this assignment and push the code
2. Include a README.md with:

   - Setup instructions
   - Usage examples
   - Dependencies list
   - Any assumptions made

3. Provide sample data for testing
4. Include any additional documentation

## Resources

- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [Python SQLite3 Documentation](https://docs.python.org/3/library/sqlite3.html)
- [Python Input Validation Best Practices](https://docs.python.org/3/howto/input.html)
- [PEP 8 Style Guide](https://www.python.org/dev/peps/pep-0008/)
