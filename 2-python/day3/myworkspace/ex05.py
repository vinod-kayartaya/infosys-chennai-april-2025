from flask import Flask, request
from ex03 import Customer, Session

app = Flask("Customer REST Endpoint")

@app.route("/")
def home():
    return """
        <h1>Welcome to Flask REST application</h1>
        <hr>
        <p>This exposes a REST endpoint at /api/customers</p>
        """

@app.route("/api/customers", methods=["GET"])
def handle_get_customers():
    with Session() as session:
        customers = session.query(Customer).all()
        customers = [c.get_as_dict() for c in customers]
        return customers

def error(message, code=404):
    return {"message": message}, code

@app.post("/api/customers")
def handle_create_customer():
    req_body = request.get_json()  # from flask import Flask, request

    required_fields = ['name', 'email', 'phone']
    missing_fields = [field for field in required_fields if not field in req_body]

    if len(missing_fields)>0:
        return error(f'Missing fields: {missing_fields}', 400)

    c1 = Customer(**req_body)
    with Session() as session:
        try:
            session.add(c1)
            session.commit()
            return c1.get_as_dict(), 201
        except Exception as e:
            session.rollback()
            return error(str(e.orig), 500)


@app.get("/api/customers/<int:customer_id>")
def handle_get_customer_by_id(customer_id):
    with Session() as session:
        customer = session.query(Customer).filter_by(id=customer_id).first()
        
        if not customer:
            return error(f'No customer found with id {customer_id}')
        
        return customer.get_as_dict()


app.run(port=1234, debug=True)
