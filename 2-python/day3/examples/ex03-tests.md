# Testing the Customer Management REST API

Below are examples of how to test the Flask REST API using curl commands. You can also use tools like Postman for a more user-friendly experience.

## 1. Start the API Server

```bash
python app.py
```

The server will start on http://127.0.0.1:5000

## 2. Create a Customer (POST)

```bash
curl -X POST http://127.0.0.1:5000/api/customers \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Smith",
    "email": "john.smith@example.com",
    "phone": "555-123-4567",
    "city": "New York"
  }'
```

## 3. Get All Customers (GET)

```bash
curl -X GET http://127.0.0.1:5000/api/customers
```

## 4. Get a Single Customer (GET)

```bash
curl -X GET http://127.0.0.1:5000/api/customers/1
```

## 5. Update a Customer (PUT)

```bash
curl -X PUT http://127.0.0.1:5000/api/customers/1 \
  -H "Content-Type: application/json" \
  -d '{
    "city": "Boston"
  }'
```

## 6. Delete a Customer (DELETE)

```bash
curl -X DELETE http://127.0.0.1:5000/api/customers/1
```

## 7. Search Customers (GET)

```bash
curl -X GET "http://127.0.0.1:5000/api/customers/search?city=New%20York&order_by=name"
```

## 8. Bulk Import Customers (POST)

```bash
curl -X POST http://127.0.0.1:5000/api/customers/bulk \
  -H "Content-Type: application/json" \
  -d '{
    "has_header": true,
    "csv_data": "name,email,phone,city\nJane Doe,jane@example.com,555-987-6543,Los Angeles\nRobert Johnson,robert@example.com,555-456-7890,Chicago"
  }'
```

## 9. Export Customers as CSV (GET)

```bash
curl -X GET http://127.0.0.1:5000/api/customers/export
```

## Postman Collection

You can also create a Postman collection for easier testing:

1. Create a new collection named "Customer Management API"
2. Add request examples for each endpoint:
   - GET all customers
   - GET single customer
   - POST new customer
   - PUT update customer
   - DELETE customer
   - GET search customers
   - POST bulk import
   - GET export customers
3. Set the appropriate request headers and body formats
