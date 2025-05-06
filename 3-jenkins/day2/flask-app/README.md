# Flask Todo API

A simple REST API for managing todo items built with Flask and SQLAlchemy.

## Features

- CRUD operations for todo items
- SQLite database
- RESTful API endpoints
- Unit tests with pytest
- Code quality checks with flake8

## Setup

1. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the application:

```bash
flask run
```

## API Endpoints

- `GET /todos` - Get all todos
- `POST /todos` - Create a new todo
- `GET /todos/<id>` - Get a specific todo
- `PUT /todos/<id>` - Update a todo
- `DELETE /todos/<id>` - Delete a todo

## Testing

Run the test suite:

```bash
pytest
```

Run tests with coverage:

```bash
pytest --cov=app tests/
```

## Code Quality

Run flake8:

```bash
flake8 app/ tests/
```

## Development

The application uses:

- Flask for the web framework
- SQLAlchemy for database operations
- pytest for testing
- flake8 for code quality
- gunicorn for production deployment
