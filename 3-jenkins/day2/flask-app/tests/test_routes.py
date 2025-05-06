import pytest
from app import create_app, db
from app.models import Todo

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_get_empty_todos(client):
    response = client.get('/todos')
    assert response.status_code == 200
    assert response.json == []

def test_create_todo(client):
    response = client.post('/todos', json={
        'title': 'Test Todo',
        'description': 'Test Description'
    })
    assert response.status_code == 201
    assert response.json['title'] == 'Test Todo'
    assert response.json['description'] == 'Test Description'
    assert response.json['completed'] is False

def test_get_todo(client):
    # Create a todo first
    client.post('/todos', json={
        'title': 'Test Todo',
        'description': 'Test Description'
    })
    
    # Get the todo
    response = client.get('/todos/1')
    assert response.status_code == 200
    assert response.json['title'] == 'Test Todo'

def test_update_todo(client):
    # Create a todo first
    client.post('/todos', json={
        'title': 'Test Todo',
        'description': 'Test Description'
    })
    
    # Update the todo
    response = client.put('/todos/1', json={
        'title': 'Updated Todo',
        'completed': True
    })
    assert response.status_code == 200
    assert response.json['title'] == 'Updated Todo'
    assert response.json['completed'] is True

def test_delete_todo(client):
    # Create a todo first
    client.post('/todos', json={
        'title': 'Test Todo',
        'description': 'Test Description'
    })
    
    # Delete the todo
    response = client.delete('/todos/1')
    assert response.status_code == 204
    
    # Verify it's deleted
    response = client.get('/todos/1')
    assert response.status_code == 404 