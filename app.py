from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api, Resource
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
db = SQLAlchemy(app)

# Initialize the API object
api = Api(app, version='1.0', title='Product API', description='API for managing products')


SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
API_URL = '/static/swagger.json'  # Our API url (can of course be a local resource)

# Call factory function to create our blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "Test application"
    },
    # oauth_config={  # OAuth config. See https://github.com/swagger-api/swagger-ui#oauth2-configuration .
    #    'clientId': "your-client-id",
    #    'clientSecret': "your-client-secret-if-required",
    #    'realm': "your-realms",
    #    'appName': "your-app-name",
    #    'scopeSeparator': " ",
    #    'additionalQueryStringParams': {'test': "hello"}
    # }
)

app.register_blueprint(swaggerui_blueprint)

# Product model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)

    @classmethod
    def get_all_products(cls):
        return cls.query.all()

# for creating tables for the models that i created 
with app.app_context():
    db.create_all()



@app.route('/addproduct', methods=['POST'])
def add_product():
    if request.method == 'POST':
        data = request.json
        new_product = Product(name=data.get('name'), description=data.get('description'))
        db.session.add(new_product)
        db.session.commit()
        return jsonify({"message": "Product added successfully"})

# Create a route for getting all products
@app.route('/products', methods=['GET'])
def get_all_products():
    products = Product.query.all()
    output = []
    for product in products:
        product_data = {'id': product.id, 'name': product.name, 'description': product.description}
        output.append(product_data)
    return jsonify({'products': output})

@app.route('/product/<int:id>', methods=['GET','DELETE'])
def product(id):
    if request.method == 'GET':
        # Get a single product by ID
        product = Product.query.get_or_404(id)
        product_data = {'id': product.id, 'name': product.name, 'description': product.description}
        return jsonify({'product': product_data})

    elif request.method == 'DELETE':
        # Delete a product by ID
        product = Product.query.get_or_404(id)
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message": "Product deleted successfully"})

# create a route for updating product 
@app.route('/updateproduct/<int:id>', methods=['PUT'])
def update_product(id):
    if request.method == 'PUT':
        data = request.json
        product = Product.query.get_or_404(id)
        product.name = data.get('name', product.name)
        product.description = data.get('description', product.description)
        db.session.commit()
        return jsonify({"message": "Product updated successfully"})



if __name__ == '__main__':
    ...
    db.create_all()
    app.run(debug=True)
