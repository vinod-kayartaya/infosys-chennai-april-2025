from flask import Flask, request, jsonify
from sqlalchemy import create_engine, Column, Integer, String, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
import csv
import io

# Initialize Flask application
app = Flask(__name__)

# Create database engine
engine = create_engine('sqlite:///customers.db', echo=False)
Base = declarative_base()

# Define Customer model
class Customer(Base):
    __tablename__ = 'customers'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(20), unique=True, nullable=False)
    city = Column(String(50))
    
    def __repr__(self):
        return f"<Customer(id={self.id}, name='{self.name}', email='{self.email}', phone='{self.phone}', city='{self.city}')>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'city': self.city
        }

# Create tables
Base.metadata.create_all(engine)

# Create session factory
Session = sessionmaker(bind=engine)

# Helper functions
def get_session():
    """Create and return a new database session"""
    return Session()

def validate_customer_data(data, update=False):
    """Validate customer data from request"""
    errors = []
    
    if not update or 'name' in data:
        if not data.get('name') or not isinstance(data.get('name'), str):
            errors.append("Name is required and must be a string")
    
    if not update or 'email' in data:
        if not data.get('email') or not isinstance(data.get('email'), str):
            errors.append("Email is required and must be a string")
    
    if not update or 'phone' in data:
        if not data.get('phone') or not isinstance(data.get('phone'), str):
            errors.append("Phone is required and must be a string")
    
    if 'city' in data and data['city'] is not None and not isinstance(data.get('city'), str):
        errors.append("City must be a string if provided")
    
    return errors

# API Routes

@app.route('/api/customers', methods=['GET'])
def get_customers():
    """Get all customers or filter by query parameters"""
    session = get_session()
    try:
        query = session.query(Customer)
        
        # Apply filters from query parameters if they exist
        if request.args.get('name'):
            query = query.filter(Customer.name.like(f"%{request.args.get('name')}%"))
        if request.args.get('email'):
            query = query.filter(Customer.email.like(f"%{request.args.get('email')}%"))
        if request.args.get('phone'):
            query = query.filter(Customer.phone.like(f"%{request.args.get('phone')}%"))
        if request.args.get('city'):
            query = query.filter(Customer.city.like(f"%{request.args.get('city')}%"))
        
        customers = query.all()
        result = [customer.to_dict() for customer in customers]
        
        return jsonify({
            'success': True,
            'count': len(result),
            'customers': result
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
    finally:
        session.close()

@app.route('/api/customers/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    """Get a single customer by ID"""
    session = get_session()
    try:
        customer = session.query(Customer).filter_by(id=customer_id).first()
        
        if not customer:
            return jsonify({
                'success': False,
                'error': f"Customer with ID {customer_id} not found"
            }), 404
        
        return jsonify({
            'success': True,
            'customer': customer.to_dict()
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
    finally:
        session.close()

@app.route('/api/customers', methods=['POST'])
def create_customer():
    """Create a new customer"""
    if not request.is_json:
        return jsonify({
            'success': False,
            'error': "Request must be JSON"
        }), 400
    
    data = request.get_json()
    errors = validate_customer_data(data)
    
    if errors:
        return jsonify({
            'success': False,
            'errors': errors
        }), 400
    
    session = get_session()
    try:
        new_customer = Customer(
            name=data['name'],
            email=data['email'],
            phone=data['phone'],
            city=data.get('city', '')
        )
        
        session.add(new_customer)
        session.commit()
        
        return jsonify({
            'success': True,
            'message': "Customer created successfully",
            'customer': new_customer.to_dict()
        }), 201
    except IntegrityError as e:
        session.rollback()
        error_message = str(e)
        if "UNIQUE constraint failed: customers.email" in error_message:
            return jsonify({
                'success': False,
                'error': "Email address already exists"
            }), 409
        elif "UNIQUE constraint failed: customers.phone" in error_message:
            return jsonify({
                'success': False,
                'error': "Phone number already exists"
            }), 409
        else:
            return jsonify({
                'success': False,
                'error': error_message
            }), 409
    except Exception as e:
        session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
    finally:
        session.close()

@app.route('/api/customers/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    """Update an existing customer"""
    if not request.is_json:
        return jsonify({
            'success': False,
            'error': "Request must be JSON"
        }), 400
    
    data = request.get_json()
    errors = validate_customer_data(data, update=True)
    
    if errors:
        return jsonify({
            'success': False,
            'errors': errors
        }), 400
    
    session = get_session()
    try:
        customer = session.query(Customer).filter_by(id=customer_id).first()
        
        if not customer:
            return jsonify({
                'success': False,
                'error': f"Customer with ID {customer_id} not found"
            }), 404
        
        if 'name' in data:
            customer.name = data['name']
        if 'email' in data:
            customer.email = data['email']
        if 'phone' in data:
            customer.phone = data['phone']
        if 'city' in data:
            customer.city = data['city']
        
        session.commit()
        
        return jsonify({
            'success': True,
            'message': "Customer updated successfully",
            'customer': customer.to_dict()
        }), 200
    except IntegrityError as e:
        session.rollback()
        error_message = str(e)
        if "UNIQUE constraint failed: customers.email" in error_message:
            return jsonify({
                'success': False,
                'error': "Email address already exists"
            }), 409
        elif "UNIQUE constraint failed: customers.phone" in error_message:
            return jsonify({
                'success': False,
                'error': "Phone number already exists"
            }), 409
        else:
            return jsonify({
                'success': False,
                'error': error_message
            }), 409
    except Exception as e:
        session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
    finally:
        session.close()

@app.route('/api/customers/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    """Delete a customer"""
    session = get_session()
    try:
        customer = session.query(Customer).filter_by(id=customer_id).first()
        
        if not customer:
            return jsonify({
                'success': False,
                'error': f"Customer with ID {customer_id} not found"
            }), 404
        
        session.delete(customer)
        session.commit()
        
        return jsonify({
            'success': True,
            'message': f"Customer {customer_id} deleted successfully"
        }), 200
    except Exception as e:
        session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
    finally:
        session.close()

@app.route('/api/customers/search', methods=['GET'])
def search_customers():
    """Advanced search endpoint with multiple criteria"""
    session = get_session()
    try:
        query = session.query(Customer)
        
        # Get all query parameters
        params = request.args.to_dict()
        
        if 'id' in params:
            query = query.filter(Customer.id == params['id'])
        if 'name' in params:
            query = query.filter(Customer.name.like(f"%{params['name']}%"))
        if 'email' in params:
            query = query.filter(Customer.email.like(f"%{params['email']}%"))
        if 'phone' in params:
            query = query.filter(Customer.phone.like(f"%{params['phone']}%"))
        if 'city' in params:
            query = query.filter(Customer.city.like(f"%{params['city']}%"))
        
        # Support for ordering
        if 'order_by' in params:
            if params['order_by'] == 'name':
                query = query.order_by(Customer.name)
            elif params['order_by'] == 'email':
                query = query.order_by(Customer.email)
            elif params['order_by'] == 'city':
                query = query.order_by(Customer.city)
        
        customers = query.all()
        result = [customer.to_dict() for customer in customers]
        
        return jsonify({
            'success': True,
            'count': len(result),
            'customers': result
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
    finally:
        session.close()

@app.route('/api/customers/bulk', methods=['POST'])
def bulk_import():
    """Import multiple customers from CSV data"""
    if not request.is_json:
        return jsonify({
            'success': False,
            'error': "Request must be JSON"
        }), 400
    
    data = request.get_json()
    
    if 'csv_data' not in data:
        return jsonify({
            'success': False,
            'error': "CSV data is required"
        }), 400
    
    csv_data = data['csv_data']
    
    # Parse CSV data
    csv_file = io.StringIO(csv_data)
    csv_reader = csv.reader(csv_file)
    
    rows = list(csv_reader)
    
    if not rows:
        return jsonify({
            'success': False,
            'error': "CSV data is empty"
        }), 400
    
    # Check for header row
    has_header = data.get('has_header', True)
    
    if has_header:
        header = rows[0]
        data_rows = rows[1:]
    else:
        header = ['name', 'email', 'phone', 'city']
        data_rows = rows
    
    if len(header) < 3:
        return jsonify({
            'success': False,
            'error': "CSV must have at least name, email, and phone columns"
        }), 400
    
    success_count = 0
    failed_rows = []
    
    session = get_session()
    
    try:
        for row in data_rows:
            if len(row) < 3:
                failed_rows.append({
                    'row': row,
                    'error': "Row must have at least name, email, and phone"
                })
                continue
            
            # Maps header column names to row values
            row_data = {}
            for i, value in enumerate(row):
                if i < len(header):
                    row_data[header[i].lower()] = value
            
            # Ensure required fields exist
            if 'name' not in row_data or 'email' not in row_data or 'phone' not in row_data:
                failed_rows.append({
                    'row': row,
                    'error': "Missing required fields"
                })
                continue
            
            try:
                new_customer = Customer(
                    name=row_data['name'],
                    email=row_data['email'],
                    phone=row_data['phone'],
                    city=row_data.get('city', '')
                )
                
                session.add(new_customer)
                session.commit()
                success_count += 1
                
            except IntegrityError as e:
                session.rollback()
                failed_rows.append({
                    'row': row,
                    'error': str(e)
                })
            except Exception as e:
                session.rollback()
                failed_rows.append({
                    'row': row,
                    'error': str(e)
                })
        
        return jsonify({
            'success': True,
            'message': f"Import complete: {success_count} succeeded, {len(failed_rows)} failed",
            'success_count': success_count,
            'failed_count': len(failed_rows),
            'failed_rows': failed_rows
        }), 200 if success_count > 0 else 400
    except Exception as e:
        session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
    finally:
        session.close()

@app.route('/api/customers/export', methods=['GET'])
def export_customers():
    """Export all customers as CSV"""
    session = get_session()
    try:
        customers = session.query(Customer).all()
        
        if not customers:
            return jsonify({
                'success': True,
                'message': "No customers found to export",
                'csv_data': ""
            }), 200
        
        # Create CSV in memory
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow(['id', 'name', 'email', 'phone', 'city'])
        
        # Write data
        for customer in customers:
            writer.writerow([
                customer.id,
                customer.name,
                customer.email,
                customer.phone,
                customer.city
            ])
        
        csv_data = output.getvalue()
        
        return jsonify({
            'success': True,
            'count': len(customers),
            'csv_data': csv_data
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
    finally:
        session.close()

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': "Resource not found"
    }), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        'success': False,
        'error': "Method not allowed"
    }), 405

@app.errorhandler(500)
def server_error(error):
    return jsonify({
        'success': False,
        'error': "Internal server error"
    }), 500

if __name__ == '__main__':
    app.run(debug=True)