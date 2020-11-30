from flask import Flask, jsonify
from flask_restful import Api
from resources.product import Products, Product
from resources.user import Users, User, UserRegister, UserLogin, UserLogout
from resources.log import Logs
from flask_jwt_extended import JWTManager
from blacklist import BLACKLIST
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = '$zb#zcJAXFcgow%^FIGr'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 18000
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = 18000
api = Api(app)
jwt = JWTManager(app)

@app.before_first_request
def create_bd():
    banco.create_all()
    UserRegister.create_admin()

@jwt.token_in_blacklist_loader
def in_blacklist(token):
    return token['jti'] in BLACKLIST

@jwt.revoked_token_loader
def is_invalidated():
    return jsonify({'message': 'You have been logged out.'}), 401

api.add_resource(Products, '/products')
api.add_resource(Product, '/product/<int:produto_id>')
api.add_resource(Users, '/users')
api.add_resource(User, '/users/<int:user_id>')
api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(Logs, '/logs')

if __name__ == '__main__':
    from sql_alchemy import banco
    banco.init_app(app)
    app.run(debug=True)
