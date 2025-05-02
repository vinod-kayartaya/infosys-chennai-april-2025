# Setting Up Swagger Documentation for Flask API

This guide explains how to install and configure Swagger documentation for your Flask Customer Management API.

## 1. Install Required Packages

First, install Flask-RESTx which provides Swagger UI integration:

```bash
pip install flask-restx
```

This package includes:

- Flask extension for building REST APIs
- Swagger UI integration
- Request validation
- Response serialization

## 2. Project Structure

Your project structure should look like this:

```
customer_api/
├── app.py           # Main application file with Flask-RESTx implementation
├── customers.db     # SQLite database (created automatically)
├── requirements.txt # Project dependencies
└── static/          # (Optional) for any static files
```

## 3. Requirements File

Create a `requirements.txt` file with the following content:

```
flask==2.3.3
flask-restx==1.1.0
sqlalchemy==2.0.20
```

Install all dependencies:

```bash
pip install -r requirements.txt
```

## 4. Running the Application

Run the application:

```bash
python app.py
```

## 5. Accessing the Swagger Documentation

Open your web browser and navigate to:

```
http://127.0.0.1:5000/swagger/
```

You'll see the interactive Swagger UI that allows you to:

- Browse API endpoints
- View request/response models
- Test API calls directly from the browser
- See documentation for parameters and response codes

## 6. Key Features of the Swagger Documentation

### 6.1 API Models

The Swagger UI shows detailed models for:

- Customer data structure
- Request payloads
- Response formats

### 6.2 Interactive Testing

You can:

- Expand each endpoint to see details
- Click "Try it out" to test the endpoint
- Fill in parameters and request bodies
- Execute requests and see responses

### 6.3 Error Codes

Documentation includes possible error responses:

- 400: Bad Request (validation errors)
- 404: Not Found
- 409: Conflict (e.g., duplicate email)
- 500: Server Error

## 7. Customizing the Swagger Documentation

You can customize your Swagger documentation by modifying:

### 7.1 API Metadata

Update the `Api` initialization in `app.py`:

```python
api = Api(
    app,
    version='1.0',
    title='Your Custom API Title',
    description='Your custom description',
    doc='/custom-path/',  # Change the URL path
    # Add other options as needed
)
```

### 7.2 Add Additional Documentation

For each endpoint, you can add more detailed documentation:

```python
@ns_customers.doc(description='A detailed description of this endpoint',
                 responses={
                     200: 'Success response description',
                     400: 'Error description',
                     # Add other response codes
                 })
def get(self):
    # Method implementation
```

### 7.3 Security Documentation

To document API security (if implemented):

```python
authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'X-API-KEY'
    }
}

api = Api(
    # Other parameters
    authorizations=authorizations,
    security='apikey'  # Apply globally
)
```

## 8. Export OpenAPI Specification

You can export the OpenAPI specification by visiting:

```
http://127.0.0.1:5000/swagger.json
```

This JSON file can be used with other tools that support OpenAPI specifications.
