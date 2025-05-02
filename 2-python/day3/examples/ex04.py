from flask import Flask, request
from flask_restx import Api, Resource, fields, reqparse
from sqlalchemy import create_engine, Column, Integer, String, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
import csv
import io

# Initialize Flask application
app = Flask(__name__)

# Initialize Flask-RESTx API with Swagger documentation
api = Api(
    app,
    version='1.0',
    title='Customer Management API',
    description='A RESTful API for managing customer information',
    doc='/swagger/',
    validate=True
)

# Create namespaces for better organization
ns_customers = api.namespace('customers', description='Customer operations')
ns_bulk = api.namespace('customers/bulk', description='Bulk customer operations')
ns_export = api.namespace('customers/export', description='Customer export operations')
ns_search = api.namespace('customers/search', description='Customer search operations')

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

# Helper function
def get_session():
    """Create and return a new database session"""
    return Session()

# Define models for request/response serialization
customer_model = api.model('Customer', {
    'id': fields.Integer(readonly=True, description='Customer unique identifier'),
    'name': fields.String(required=True, description='Customer name'),
    'email': fields.String(required=True, description='Customer email address'),
    'phone': fields.String(required=True, description='Customer phone number'),
    'city': fields.String(description='Customer city')
})

customer_input_model = api.model('CustomerInput', {
    'name': fields.String(required=True, description='Customer name'),
    'email': fields.String(required=True, description='Customer email address'),
    'phone': fields.String(required=True, description='Customer phone number'),
    'city': fields.String(description='Customer city')
})

customer_update_model = api.model('CustomerUpdate', {
    'name': fields.String(description='Customer name'),
    'email': fields.String(description='Customer email address'),
    'phone': fields.String(description='Customer phone number'),
    'city': fields.String(description='Customer city')
})

bulk_import_model = api.model('BulkImport', {
    'csv_data': fields.String(required=True, description='CSV data with customer information'),
    'has_header': fields.Boolean(default=True, description='Whether CSV data includes a header row')
})

bulk_response_model = api.model('BulkResponse', {
    'success': fields.Boolean(description='Operation success status'),
    'message': fields.String(description='Response message'),
    'success_count': fields.Integer(description='Number of successfully imported customers'),
    'failed_count': fields.Integer(description='Number of failed imports'),
    'failed_rows': fields.List(fields.Raw, description='Details of failed rows')
})

export_response_model = api.model('ExportResponse', {
    'success': fields.Boolean(description='Operation success status'),
    'count': fields.Integer(description='Number of exported customers'),
    'csv_data': fields.String(description='CSV data containing all customers')
})

# Define search parser
search_parser = reqparse.RequestParser()
search_parser.add_argument('name', type=str, help='Filter by name (partial match)')
search_parser.add_argument('email', type=str, help='Filter by email (partial match)')
search_parser.add_argument('phone', type=str, help='Filter by phone (partial match)')
search_parser.add_argument('city', type=str, help='Filter by city (partial match)')
search_parser.add_argument('order_by', type=str, choices=['name', 'email', 'city'], 
                         help='Field to order results by')

# Customer routes
@ns_customers.route('/')
class CustomerList(Resource):
    @ns_customers.doc('list_customers')
    @ns_customers.marshal_list_with(customer_model)
    @ns_customers.param('name', 'Filter by name (partial match)')
    @ns_customers.param('email', 'Filter by email (partial match)')
    @ns_customers.param('phone', 'Filter by phone (partial match)')
    @ns_customers.param('city', 'Filter by city (partial match)')
    def get(self):
        """List all customers with optional filtering"""
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
            return [customer.to_dict() for customer in customers]
        finally:
            session.close()
    
    @ns_customers.doc('create_customer')
    @ns_customers.expect(customer_input_model)
    @ns_customers.response(201, 'Customer created successfully')
    @ns_customers.response(400, 'Validation error')
    @ns_customers.response(409, 'Email or phone already exists')
    @ns_customers.marshal_with(customer_model, code=201)
    def post(self):
        """Create a new customer"""
        data = api.payload
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
            
            return new_customer.to_dict(), 201
        except IntegrityError as e:
            session.rollback()
            error_message = str(e)
            if "UNIQUE constraint failed: customers.email" in error_message:
                api.abort(409, "Email address already exists")
            elif "UNIQUE constraint failed: customers.phone" in error_message:
                api.abort(409, "Phone number already exists")
            else:
                api.abort(409, error_message)
        except Exception as e:
            session.rollback()
            api.abort(500, str(e))
        finally:
            session.close()


@ns_customers.route('/<int:id>')
@ns_customers.param('id', 'The customer identifier')
@ns_customers.response(404, 'Customer not found')
class CustomerItem(Resource):
    @ns_customers.doc('get_customer')
    @ns_customers.marshal_with(customer_model)
    def get(self, id):
        """Get a specific customer by ID"""
        session = get_session()
        try:
            customer = session.query(Customer).filter_by(id=id).first()
            
            if not customer:
                api.abort(404, f"Customer with ID {id} not found")
            
            return customer.to_dict()
        finally:
            session.close()
    
    @ns_customers.doc('update_customer')
    @ns_customers.expect(customer_update_model)
    @ns_customers.marshal_with(customer_model)
    def put(self, id):
        """Update a customer"""
        data = api.payload
        session = get_session()
        
        try:
            customer = session.query(Customer).filter_by(id=id).first()
            
            if not customer:
                api.abort(404, f"Customer with ID {id} not found")
            
            if 'name' in data:
                customer.name = data['name']
            if 'email' in data:
                customer.email = data['email']
            if 'phone' in data:
                customer.phone = data['phone']
            if 'city' in data:
                customer.city = data['city']
            
            session.commit()
            return customer.to_dict()
        except IntegrityError as e:
            session.rollback()
            error_message = str(e)
            if "UNIQUE constraint failed: customers.email" in error_message:
                api.abort(409, "Email address already exists")
            elif "UNIQUE constraint failed: customers.phone" in error_message:
                api.abort(409, "Phone number already exists")
            else:
                api.abort(409, error_message)
        except Exception as e:
            session.rollback()
            api.abort(500, str(e))
        finally:
            session.close()
    
    @ns_customers.doc('delete_customer')
    @ns_customers.response(204, 'Customer deleted')
    def delete(self, id):
        """Delete a customer"""
        session = get_session()
        try:
            customer = session.query(Customer).filter_by(id=id).first()
            
            if not customer:
                api.abort(404, f"Customer with ID {id} not found")
            
            session.delete(customer)
            session.commit()
            return '', 204
        except Exception as e:
            session.rollback()
            api.abort(500, str(e))
        finally:
            session.close()


@ns_search.route('/')
class CustomerSearch(Resource):
    @ns_search.doc('search_customers')
    @ns_search.expect(search_parser)
    @ns_search.marshal_list_with(customer_model)
    def get(self):
        """Advanced search for customers with multiple criteria"""
        args = search_parser.parse_args()
        session = get_session()
        
        try:
            query = session.query(Customer)
            
            if args['name']:
                query = query.filter(Customer.name.like(f"%{args['name']}%"))
            if args['email']:
                query = query.filter(Customer.email.like(f"%{args['email']}%"))
            if args['phone']:
                query = query.filter(Customer.phone.like(f"%{args['phone']}%"))
            if args['city']:
                query = query.filter(Customer.city.like(f"%{args['city']}%"))
            
            # Support for ordering
            if args['order_by']:
                if args['order_by'] == 'name':
                    query = query.order_by(Customer.name)
                elif args['order_by'] == 'email':
                    query = query.order_by(Customer.email)
                elif args['order_by'] == 'city':
                    query = query.order_by(Customer.city)
            
            customers = query.all()
            return [customer.to_dict() for customer in customers]
        finally:
            session.close()


@ns_bulk.route('/')
class CustomerBulkImport(Resource):
    @ns_bulk.doc('bulk_import')
    @ns_bulk.expect(bulk_import_model)
    @ns_bulk.marshal_with(bulk_response_model)
    def post(self):
        """Import multiple customers from CSV data"""
        data = api.payload
        csv_data = data['csv_data']
        has_header = data.get('has_header', True)
        
        # Parse CSV data
        csv_file = io.StringIO(csv_data)
        csv_reader = csv.reader(csv_file)
        
        rows = list(csv_reader)
        
        if not rows:
            api.abort(400, "CSV data is empty")
        
        if has_header:
            header = rows[0]
            data_rows = rows[1:]
        else:
            header = ['name', 'email', 'phone', 'city']
            data_rows = rows
        
        if len(header) < 3:
            api.abort(400, "CSV must have at least name, email, and phone columns")
        
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
            
            return {
                'success': success_count > 0,
                'message': f"Import complete: {success_count} succeeded, {len(failed_rows)} failed",
                'success_count': success_count,
                'failed_count': len(failed_rows),
                'failed_rows': failed_rows
            }, 200 if success_count > 0 else 400
        except Exception as e:
            session.rollback()
            api.abort(500, str(e))
        finally:
            session.close()


@ns_export.route('/')
class CustomerExport(Resource):
    @ns_export.doc('export_customers')
    @ns_export.marshal_with(export_response_model)
    def get(self):
        """Export all customers as CSV"""
        session = get_session()
        try:
            customers = session.query(Customer).all()
            
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
            
            return {
                'success': True,
                'count': len(customers),
                'csv_data': csv_data
            }
        finally:
            session.close()


if __name__ == '__main__':
    app.run(debug=True)