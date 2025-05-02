# Assignment: Building a Python Flask Application

## Objective

Your task is to create a Python Flask application that exposes RESTful endpoints to manage customer data. The application should support the following operations:

### GET Requests

1. Retrieve a paginated list of customers:

   - Endpoint: `/api/customers`
   - Default query parameters: `page=1`, `size=10`

2. Filter customers by name:

   - Endpoint: `/api/customers?name=kumar`

3. Filter customers by city:

   - Endpoint: `/api/customers?city=mumbai`

4. Paginate filtered customers by city:

   - Endpoint: `/api/customers?city=mumbai&page=7`

5. Paginate and adjust page size for filtered customers by city:

   - Endpoint: `/api/customers?city=mumbai&page=7&size=20`

6. Retrieve a single customer by phone number:

   - Endpoint: `/api/customers?phone=9000190002`

7. Retrieve a single customer by email:
   - Endpoint: `/api/customers?email=vinod@xmpl.com`

### POST Request

- Add a new customer to the database.
- Endpoint: `/api/customers`
- Request body: JSON object containing customer details (e.g., name, phone, email, city, etc.).

### PUT Request

- Update an existing customer's details.
- Endpoint: `/api/customers/<customer_id>`
- Request body: JSON object containing updated customer details.

### PATCH Request

- Partially update an existing customer's details.
- Endpoint: `/api/customers/<customer_id>`
- Request body: JSON object containing the fields to update.

### DELETE Request

- Delete a customer from the database.
- Endpoint: `/api/customers/<customer_id>`

## Instructions

1. **Setup**:

   - Create a new Flask application.
   - Use an SQLite database (`customers.db`) to store customer data.
   - Use SQLAlchemy for database interactions.

2. **Endpoints**:

   - Implement all the endpoints listed above.
   - Ensure proper validation of query parameters and request bodies.

3. **Pagination**:

   - Implement pagination for the `/api/customers` endpoint.
   - Use `page` and `size` query parameters to control pagination.

4. **Filtering**:

   - Implement filtering logic for `name`, `city`, `phone`, and `email` query parameters.

5. **CRUD Operations**:

   - Implement Create, Read, Update, and Delete operations for customer data.

6. **Testing**:
   - Test your endpoints using tools like Postman or the provided `test-requests.http` file.

## Deliverables

1. A Python Flask application with the required endpoints.
2. A database file (`customers.db`) with sample customer data.
3. A `README.md` file with instructions on how to run the application.
4. A `test-requests.http` file with sample HTTP requests for testing the endpoints.

## Optional

- Add error handling for invalid query parameters or request bodies.
- Implement sorting for the `/api/customers` endpoint (e.g., sort by name or city).
