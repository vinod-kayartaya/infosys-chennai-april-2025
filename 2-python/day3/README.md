# Day 3: REST API Development

## Table of Contents

1. [REST API Development with Flask](#rest-api-development-with-flask)
2. [API Documentation](#api-documentation)
3. [Final Project](#final-project)

## REST API Development with Flask

### Understanding REST APIs

REST (Representational State Transfer) is an architectural style for designing networked applications. It's based on a set of principles that define how web standards should be used.

Key REST principles:

- **Client-Server Architecture**: Separation of concerns between client and server
- **Stateless**: Each request contains all information needed to process it
- **Cacheable**: Responses must define themselves as cacheable or not
- **Uniform Interface**: Standardized way of communicating between client and server
- **Layered System**: Client can't tell if it's connected directly to the server
- **Code on Demand**: Servers can temporarily extend client functionality

### Flask Framework Basics

Flask is a lightweight web framework for Python that's perfect for building REST APIs. It's known for its simplicity and flexibility.

Key Flask concepts:

- **Application**: The main Flask object that handles requests
- **Route**: A URL pattern that maps to a function
- **View Function**: The function that handles a request
- **Request**: The data sent by the client
- **Response**: The data sent back to the client
- **Blueprint**: A way to organize related routes

#### Basic Flask Application

```python
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def hello_world():
    return jsonify({"message": "Hello, World!"})

if __name__ == '__main__':
    app.run(debug=True)
```

### Route Handling

Routes in Flask define the URL patterns that your API will respond to. They can handle different HTTP methods and include parameters.

#### Basic Routes

```python
@app.route('/users', methods=['GET'])
def get_users():
    return jsonify({"users": ["John", "Jane"]})

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    return jsonify({"user_id": user_id, "name": "John"})
```

#### Route Parameters

Flask supports several types of route parameters:

- **String**: Default type, matches any string
- **int**: Matches integers
- **float**: Matches floating-point numbers
- **path**: Matches strings including slashes
- **uuid**: Matches UUID strings

```python
@app.route('/users/<string:name>')
def get_user_by_name(name):
    return jsonify({"name": name})

@app.route('/products/<float:price>')
def get_products_by_price(price):
    return jsonify({"price": price})
```

### Request/Response Cycle

The request/response cycle in Flask involves:

1. Client sends a request to the server
2. Flask receives the request and routes it to the appropriate function
3. The function processes the request and generates a response
4. Flask sends the response back to the client

#### Handling Requests

```python
from flask import request

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')

    # Process the data
    user = {"name": name, "email": email}

    return jsonify(user), 201
```

#### Sending Responses

```python
from flask import jsonify, make_response

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = {"id": user_id, "name": "John"}

    # Different ways to send responses
    return jsonify(user)  # JSON response
    return make_response(jsonify(user), 200)  # Custom status code
    return jsonify(user), 201  # Status code as tuple
```

### Error Handling

Error handling in Flask allows you to gracefully handle exceptions and return appropriate error responses.

#### Basic Error Handling

```python
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({"error": "Internal server error"}), 500
```

#### Custom Exceptions

```python
class UserNotFound(Exception):
    pass

@app.errorhandler(UserNotFound)
def handle_user_not_found(error):
    return jsonify({"error": "User not found"}), 404

@app.route('/users/<int:user_id>')
def get_user(user_id):
    user = find_user(user_id)
    if not user:
        raise UserNotFound()
    return jsonify(user)
```

### Middleware and Extensions

Middleware and extensions in Flask allow you to add functionality to your application without modifying the core code.

#### Using Middleware

```python
from flask import request
import time

@app.before_request
def before_request():
    request.start_time = time.time()

@app.after_request
def after_request(response):
    duration = time.time() - request.start_time
    response.headers['X-Request-Duration'] = str(duration)
    return response
```

#### Popular Flask Extensions

1. **Flask-SQLAlchemy**: SQL ORM for Flask

   ```python
   from flask_sqlalchemy import SQLAlchemy

   db = SQLAlchemy(app)

   class User(db.Model):
       id = db.Column(db.Integer, primary_key=True)
       name = db.Column(db.String(80))
   ```

2. **Flask-Migrate**: Database migrations

   ```python
   from flask_migrate import Migrate

   migrate = Migrate(app, db)
   ```

3. **Flask-JWT-Extended**: JWT authentication

   ```python
   from flask_jwt_extended import JWTManager, jwt_required

   jwt = JWTManager(app)

   @app.route('/protected')
   @jwt_required()
   def protected():
       return jsonify({"message": "Protected route"})
   ```

## API Documentation

### Introduction to Swagger/OpenAPI

Swagger/OpenAPI is a specification for documenting REST APIs. It provides a standardized way to describe your API, including:

- Available endpoints and operations
- Operation parameters
- Authentication methods
- Contact information
- License information

#### Basic OpenAPI Structure

```yaml
openapi: 3.0.0
info:
  title: User API
  version: 1.0.0
  description: API for managing users
paths:
  /users:
    get:
      summary: Get all users
      responses:
        '200':
          description: List of users
```

### API Documentation Best Practices

1. **Be Consistent**: Use consistent naming and formatting
2. **Include Examples**: Provide examples of requests and responses
3. **Document Errors**: List all possible error responses
4. **Use Clear Descriptions**: Explain what each endpoint does
5. **Include Authentication**: Document how to authenticate

#### Example Documentation

```yaml
paths:
  /users/{id}:
    get:
      summary: Get user by ID
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: User found
          content:
            application/json:
              schema:
                type: object
                properties:
                  id:
                    type: integer
                  name:
                    type: string
        '404':
          description: User not found
```

### Interactive Documentation

Interactive documentation allows users to try out your API directly from the documentation.

#### Using Swagger UI

```python
from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.json'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "User API"
    }
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
```

### Versioning Strategies

API versioning is important for maintaining backward compatibility while evolving your API.

#### URL Versioning

```
/api/v1/users
/api/v2/users
```

#### Header Versioning

```
Accept: application/vnd.myapi.v1+json
```

#### Content Type Versioning

```
Content-Type: application/vnd.myapi.v1+json
```

## Final Project

### Building a Complete REST API

For the final project, you'll build a complete REST API for a task management system. The API will include:

1. **User Management**

   - Registration and authentication
   - User profiles
   - Role-based access control

2. **Task Management**

   - Create, read, update, and delete tasks
   - Assign tasks to users
   - Track task status

3. **Project Management**
   - Create and manage projects
   - Add tasks to projects
   - Track project progress

### Project Structure

```
task_manager/
├── app/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── task.py
│   │   └── project.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── users.py
│   │   ├── tasks.py
│   │   └── projects.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   └── task_service.py
│   └── utils/
│       ├── __init__.py
│       └── validators.py
├── config.py
├── requirements.txt
└── run.py
```

### Implementation Steps

1. **Set Up the Project**

   ```python
   # run.py
   from app import create_app

   app = create_app()

   if __name__ == '__main__':
       app.run(debug=True)
   ```

2. **Define Models**

   ```python
   # app/models/user.py
   from app import db

   class User(db.Model):
       id = db.Column(db.Integer, primary_key=True)
       username = db.Column(db.String(80), unique=True, nullable=False)
       email = db.Column(db.String(120), unique=True, nullable=False)
       password_hash = db.Column(db.String(128))
   ```

3. **Create Routes**

   ```python
   # app/routes/users.py
   from flask import Blueprint, jsonify, request

   users_bp = Blueprint('users', __name__)

   @users_bp.route('/users', methods=['GET'])
   def get_users():
       users = User.query.all()
       return jsonify([user.to_dict() for user in users])
   ```

4. **Implement Authentication**

   ```python
   # app/routes/auth.py
   from flask import Blueprint, request, jsonify
   from flask_jwt_extended import create_access_token

   auth_bp = Blueprint('auth', __name__)

   @auth_bp.route('/login', methods=['POST'])
   def login():
       data = request.get_json()
       user = User.query.filter_by(username=data['username']).first()

       if user and user.check_password(data['password']):
           access_token = create_access_token(identity=user.id)
           return jsonify({"token": access_token})

       return jsonify({"error": "Invalid credentials"}), 401
   ```

5. **Add Error Handling**

   ```python
   # app/__init__.py
   from flask import jsonify

   def create_app():
       app = Flask(__name__)

       @app.errorhandler(404)
       def not_found(error):
           return jsonify({"error": "Not found"}), 404

       @app.errorhandler(500)
       def server_error(error):
           return jsonify({"error": "Internal server error"}), 500

       return app
   ```

6. **Document the API**
   ```yaml
   # swagger.yaml
   openapi: 3.0.0
   info:
     title: Task Manager API
     version: 1.0.0
   paths:
     /users:
       get:
         summary: Get all users
         responses:
           '200':
             description: List of users
   ```

### Testing Implementation

1. **Unit Tests**

   ```python
   # tests/test_models.py
   import unittest
   from app import create_app, db
   from app.models.user import User

   class TestUserModel(unittest.TestCase):
       def setUp(self):
           self.app = create_app()
           self.app.config['TESTING'] = True
           self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
           self.client = self.app.test_client()
           with self.app.app_context():
               db.create_all()

       def test_create_user(self):
           user = User(username='test', email='test@example.com')
           user.set_password('password')
           self.assertEqual(user.username, 'test')
   ```

2. **Integration Tests**
   ```python
   # tests/test_routes.py
   class TestUserRoutes(unittest.TestCase):
       def test_get_users(self):
           response = self.client.get('/users')
           self.assertEqual(response.status_code, 200)
           data = json.loads(response.data)
           self.assertIsInstance(data, list)
   ```

### Documentation

1. **API Documentation**

   - Use Swagger/OpenAPI to document all endpoints
   - Include request/response examples
   - Document authentication requirements

2. **Code Documentation**

   - Add docstrings to all functions and classes
   - Include type hints
   - Document complex algorithms

3. **User Documentation**
   - Create a README with setup instructions
   - Include usage examples
   - Document environment variables

## Additional Resources

1. [Flask Documentation](https://flask.palletsprojects.com/)
2. [OpenAPI Specification](https://swagger.io/specification/)
3. [Flask-SQLAlchemy Documentation](https://flask-sqlalchemy.palletsprojects.com/)
4. [Flask-JWT-Extended Documentation](https://flask-jwt-extended.readthedocs.io/)
5. [REST API Design Best Practices](https://restfulapi.net/)

## Next Steps

1. Practice building REST APIs with Flask
2. Learn about API security best practices
3. Explore advanced Flask features like blueprints and extensions
4. Study API design patterns and anti-patterns
5. Learn about API testing strategies
