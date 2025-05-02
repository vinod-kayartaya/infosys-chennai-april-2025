# Day 2: Concurrency, Database Operations and Testing

## Table of Contents

1. [Concurrency in Python](#concurrency-in-python)
2. [Python Database Fundamentals](#python-database-fundamentals)
3. [Object-Relational Mapping (ORM)](#object-relational-mapping-orm)
4. [Testing in Python](#testing-in-python)

## Concurrency in Python

### Understanding Threading

Threading is a programming concept that allows multiple threads of execution to run concurrently within a single process. In Python, threading is particularly useful for I/O-bound tasks, such as network operations or file I/O, where the program spends most of its time waiting for external resources.

Key concepts in threading:

- **Thread**: A sequence of instructions that can be executed independently
- **Global Interpreter Lock (GIL)**: Python's mechanism that allows only one thread to execute Python code at a time
- **Thread Safety**: Ensuring that shared resources are accessed safely by multiple threads
- **Race Condition**: A situation where the behavior of a program depends on the relative timing of events

The following example demonstrates basic threading in Python:

```python
import threading
import time

def task(name, delay):
    print(f"Thread {name} starting")
    time.sleep(delay)
    print(f"Thread {name} finished")

# Create threads
thread1 = threading.Thread(target=task, args=("A", 2))
thread2 = threading.Thread(target=task, args=("B", 1))

# Start threads
thread1.start()
thread2.start()

# Wait for threads to complete
thread1.join()
thread2.join()
```

### Working with Threading Module

#### Thread Synchronization

When multiple threads access shared resources, synchronization mechanisms are needed to prevent race conditions. Python provides several synchronization primitives:

1. **Locks**: The most basic synchronization primitive that allows only one thread to access a resource at a time
2. **RLocks**: Reentrant locks that can be acquired multiple times by the same thread
3. **Semaphores**: Allow a limited number of threads to access a resource
4. **Events**: Allow threads to communicate with each other
5. **Conditions**: Allow threads to wait for a condition to be met

Here's an example of using a lock for thread synchronization:

```python
import threading

# Lock for thread synchronization
lock = threading.Lock()
counter = 0

def increment():
    global counter
    with lock:
        current = counter
        time.sleep(0.1)  # Simulate some work
        counter = current + 1

# Create multiple threads
threads = []
for _ in range(10):
    t = threading.Thread(target=increment)
    threads.append(t)
    t.start()

# Wait for all threads to complete
for t in threads:
    t.join()

print(f"Final counter value: {counter}")
```

#### Thread Pool

A thread pool is a group of pre-initialized threads that are ready to perform tasks. This approach is more efficient than creating new threads for each task, as it reduces the overhead of thread creation and destruction.

Python's `concurrent.futures` module provides a high-level interface for working with thread pools:

```python
from concurrent.futures import ThreadPoolExecutor

def process_item(item):
    # Simulate processing
    time.sleep(1)
    return f"Processed {item}"

items = range(5)
with ThreadPoolExecutor(max_workers=3) as executor:
    results = list(executor.map(process_item, items))
```

### Introduction to asyncio

asyncio is Python's library for writing concurrent code using the async/await syntax. It's particularly well-suited for I/O-bound tasks and provides a more efficient alternative to threading for many use cases.

Key concepts in asyncio:

- **Coroutine**: A function that can be paused and resumed
- **Event Loop**: The central execution unit that manages coroutines
- **Task**: A wrapper around a coroutine that allows it to be scheduled
- **Future**: An object that represents the result of an asynchronous operation

#### Basic Async Function

Here's a simple example of an async function:

```python
import asyncio

async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)

async def main():
    print("Started")
    await say_after(1, "Hello")
    await say_after(2, "World")
    print("Finished")

asyncio.run(main())
```

#### Concurrent Tasks

asyncio allows you to run multiple tasks concurrently:

```python
async def main():
    task1 = asyncio.create_task(say_after(1, "Hello"))
    task2 = asyncio.create_task(say_after(2, "World"))

    print("Started")
    await task1
    await task2
    print("Finished")
```

### Async/Await Syntax

The async/await syntax is a way to write asynchronous code that looks similar to synchronous code. It makes it easier to reason about asynchronous operations and avoid callback hell.

Here's an example of using async/await with the aiohttp library for making HTTP requests:

```python
import asyncio
import aiohttp

async def fetch_url(session, url):
    async with session.get(url) as response:
        return await response.text()

async def main():
    urls = [
        "https://api.example.com/1",
        "https://api.example.com/2",
        "https://api.example.com/3"
    ]

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url) for url in urls]
        results = await asyncio.gather(*tasks)
        return results
```

### Choosing Between Threading and asyncio

When deciding between threading and asyncio, consider the following factors:

- Use **threading** when:

  - Working with I/O-bound operations
  - Need to run CPU-bound tasks in parallel
  - Working with legacy code or libraries that don't support async

- Use **asyncio** when:
  - Working with I/O-bound operations
  - Need high concurrency with many connections
  - Working with modern async libraries
  - Want to avoid thread overhead

## Python Database Fundamentals

### SQL Basics

SQL (Structured Query Language) is the standard language for interacting with relational databases. It provides a set of commands for creating, reading, updating, and deleting data.

Key SQL concepts:

- **Tables**: Collections of related data organized in rows and columns
- **Primary Keys**: Unique identifiers for each row in a table
- **Foreign Keys**: References to primary keys in other tables
- **Indexes**: Data structures that improve the speed of data retrieval
- **Transactions**: Units of work that are executed as a single operation

#### Basic SQL Commands

Here are some common SQL commands:

```sql
-- Create table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert data
INSERT INTO users (name, email) VALUES ('John Doe', 'john@example.com');

-- Select data
SELECT * FROM users WHERE name LIKE 'John%';

-- Update data
UPDATE users SET name = 'Jane Doe' WHERE id = 1;

-- Delete data
DELETE FROM users WHERE id = 1;
```

#### Joins

Joins are used to combine rows from two or more tables based on a related column:

```sql
-- Inner join
SELECT orders.id, users.name
FROM orders
INNER JOIN users ON orders.user_id = users.id;

-- Left join
SELECT users.name, orders.id
FROM users
LEFT JOIN orders ON users.id = orders.user_id;
```

### CRUD Operations with Python

Python provides several libraries for interacting with databases, including sqlite3, psycopg2 (for PostgreSQL), and mysql-connector-python (for MySQL).

Here are some common database functions and operations:

#### Connection Functions

- `connect()`: Establishes connection to database
- `close()`: Closes database connection
- `commit()`: Commits current transaction
- `rollback()`: Rolls back current transaction

#### Cursor Functions

- `cursor()`: Creates cursor object for executing queries
- `execute()`: Executes a single SQL query
- `executemany()`: Executes same SQL query with different parameters
- `fetchone()`: Fetches next row of query result
- `fetchall()`: Fetches all remaining rows
- `fetchmany(size)`: Fetches specified number of rows

#### Transaction Functions

- `begin()`: Starts a new transaction
- `savepoint()`: Creates a savepoint within transaction
- `release()`: Releases a savepoint
- `commit()`: Makes changes permanent
- `rollback()`: Undoes changes since last commit

#### Utility Functions

- `rowcount`: Number of rows affected by last query
- `lastrowid`: ID of last inserted row
- `description`: Information about result columns
- `tables()`: Lists available tables
- `columns()`: Lists columns in a table

Here's an example of performing CRUD operations using the sqlite3 library:

```python
import sqlite3

def create_connection():
    return sqlite3.connect('example.db')

def create_user(conn, name, email):
    sql = '''INSERT INTO users(name, email) VALUES(?,?)'''
    cur = conn.cursor()
    cur.execute(sql, (name, email))
    conn.commit()
    return cur.lastrowid

def get_user(conn, user_id):
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE id=?", (user_id,))
    return cur.fetchone()

def update_user(conn, user_id, name, email):
    sql = '''UPDATE users SET name=?, email=? WHERE id=?'''
    cur = conn.cursor()
    cur.execute(sql, (name, email, user_id))
    conn.commit()

def delete_user(conn, user_id):
    sql = 'DELETE FROM users WHERE id=?'
    cur = conn.cursor()
    cur.execute(sql, (user_id,))
    conn.commit()
```

### Transactions and ACID Properties

Transactions are units of work that are executed as a single operation. They ensure that a set of database operations either all succeed or all fail, maintaining data integrity.

ACID properties of transactions:

- **Atomicity**: All operations in a transaction are completed successfully, or none of them are
- **Consistency**: The database remains in a valid state before and after the transaction
- **Isolation**: Concurrent transactions do not interfere with each other
- **Durability**: Once a transaction is committed, its changes are permanent

Here's an example of a transaction that transfers money between two accounts:

```python
def transfer_money(conn, from_account, to_account, amount):
    try:
        # Start transaction
        conn.execute('BEGIN')

        # Deduct from source account
        conn.execute(
            'UPDATE accounts SET balance = balance - ? WHERE id = ?',
            (amount, from_account)
        )

        # Add to destination account
        conn.execute(
            'UPDATE accounts SET balance = balance + ? WHERE id = ?',
            (amount, to_account)
        )

        # Commit transaction
        conn.commit()

    except Exception as e:
        # Rollback on error
        conn.rollback()
        raise e
```

## Object-Relational Mapping (ORM)

### Introduction to SQLAlchemy

SQLAlchemy is a popular Python ORM that provides a high-level interface for interacting with databases. It allows you to work with databases using Python objects instead of writing raw SQL.

Key concepts in SQLAlchemy:

- **Engine**: The starting point for any SQLAlchemy application
- **Session**: The primary interface for database operations
- **Model**: A Python class that represents a database table
- **Query**: A way to retrieve data from the database

#### Basic Setup

Here's how to set up SQLAlchemy:

```python
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine('sqlite:///example.db')
Session = sessionmaker(bind=engine)
```

#### Model Definitions

Models in SQLAlchemy are Python classes that represent database tables:

```python
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)

    def __repr__(self):
        return f"<User(name='{self.name}', email='{self.email}')>"
```

### Query Operations

SQLAlchemy provides a powerful query API for retrieving data from the database:

```python
# Create session
session = Session()

# Create
new_user = User(name='John Doe', email='john@example.com')
session.add(new_user)
session.commit()

# Read
user = session.query(User).filter_by(name='John Doe').first()
users = session.query(User).all()

# Update
user.name = 'Jane Doe'
session.commit()

# Delete
session.delete(user)
session.commit()
```

### Relationships and Joins

SQLAlchemy allows you to define relationships between models, making it easy to work with related data:

```python
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    amount = Column(Integer)

    user = relationship("User", back_populates="orders")

# Add relationship to User model
User.orders = relationship("Order", back_populates="user")

# Query with relationships
user = session.query(User).first()
for order in user.orders:
    print(f"Order {order.id}: ${order.amount}")
```

## Testing in Python

### Introduction to unittest

unittest is Python's built-in testing framework. It provides a set of tools for constructing and running tests.

Key concepts in unittest:

- **TestCase**: A class that contains test methods
- **Test Suite**: A collection of test cases
- **Test Runner**: A program that runs tests and reports the results
- **Assertion**: A statement that checks if a condition is true

Here's an example of a test case:

```python
import unittest

class TestCalculator(unittest.TestCase):
    def setUp(self):
        # Setup code that runs before each test
        self.calc = Calculator()

    def test_addition(self):
        result = self.calc.add(2, 3)
        self.assertEqual(result, 5)

    def test_subtraction(self):
        result = self.calc.subtract(5, 3)
        self.assertEqual(result, 2)

    def tearDown(self):
        # Cleanup code that runs after each test
        pass

if __name__ == '__main__':
    unittest.main()
```

### Writing Test Cases

When writing test cases, it's important to follow these best practices:

- Test one thing at a time
- Use descriptive test names
- Arrange, Act, Assert pattern
- Test edge cases and error conditions

Here's an example of a test case for a User model:

```python
class TestUserModel(unittest.TestCase):
    def test_user_creation(self):
        user = User(name='John', email='john@example.com')
        self.assertEqual(user.name, 'John')
        self.assertEqual(user.email, 'john@example.com')

    def test_invalid_email(self):
        with self.assertRaises(ValueError):
            User(name='John', email='invalid-email')
```

### Test-Driven Development (TDD)

Test-Driven Development (TDD) is a software development approach where tests are written before the code. The process follows these steps:

1. Write a failing test
2. Write the minimal code to make the test pass
3. Refactor the code

Here's an example of TDD for a ShoppingCart class:

1. Write failing test

```python
def test_calculate_total():
    cart = ShoppingCart()
    cart.add_item('apple', 1.00)
    cart.add_item('banana', 2.00)
    assert cart.calculate_total() == 3.00
```

2. Write minimal implementation

```python
class ShoppingCart:
    def __init__(self):
        self.items = []

    def add_item(self, name, price):
        self.items.append((name, price))

    def calculate_total(self):
        return sum(price for _, price in self.items)
```

3. Refactor and improve

```python
class ShoppingCart:
    def __init__(self):
        self.items = []

    def add_item(self, name, price):
        if price < 0:
            raise ValueError("Price cannot be negative")
        self.items.append((name, price))

    def calculate_total(self):
        return sum(price for _, price in self.items)

    def remove_item(self, name):
        self.items = [item for item in self.items if item[0] != name]
```

## Additional Resources

1. [Python Threading Documentation](https://docs.python.org/3/library/threading.html)
2. [asyncio Documentation](https://docs.python.org/3/library/asyncio.html)
3. [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
4. [Python Testing Documentation](https://docs.python.org/3/library/unittest.html)
5. [pytest Documentation](https://docs.pytest.org/)

## Next Steps

1. Practice writing concurrent code using both threading and asyncio
2. Implement a real-world database application using SQLAlchemy
3. Write comprehensive test suites for your applications
4. Learn about database optimization and indexing
5. Explore advanced testing techniques like property-based testing
