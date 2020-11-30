from flask_restful import Resource, reqparse
from models.user import UserModel
from flask_jwt_extended import create_access_token, jwt_required, get_raw_jwt
from werkzeug.security import safe_str_cmp
from blacklist import BLACKLIST

args = reqparse.RequestParser()
args.add_argument('name', type=str, required=True, help="the field 'user_name' cannot be left")
args.add_argument('password', type=str, required=True, help="the field 'password' cannot be left")
args.add_argument('status')

class Users(Resource):
    def get(self):
        return {'users' : [user.json() for user in UserModel.query.all()]}

class User(Resource):

    @jwt_required
    def get(self, user_id):
        user = UserModel.find(int(user_id))
        if user:
            return user.json()
        return {'message' : 'User not found'}, 404

    @jwt_required
    def delete(self, user_id):
        user = UserModel.find(produto_id)
        if user:
            user.delete()
            return {'message' : 'user has been disabled'}
        return {'message' : 'User not found'}, 404

class UserRegister(Resource):

    @jwt_required
    def post(self):
        data = args.parse_args()

        if UserModel.find_by_name(data['name']):
            return {"message" : "name '{}' already exists. ".format(data['name'])}, 400

        new_user = UserModel(**data)
        new_user.create()
        return {'message': 'User created successfully!' }, 201

    @classmethod
    def create_admin(cls):
        admin = UserModel("admin", "admin", True)
        admin.create_without_log()

class UserLogin(Resource):

    @classmethod
    def post(cls):
        data = args.parse_args()

        user = UserModel.find_by_name(data['name'])
        if user:
            if user.status:
                if safe_str_cmp(user.password, data['password']):
                    access_token = create_access_token(identity=user.name, expires_in=18000)
                    return {'access_token': access_token}, 200
                return {'message': 'incorrect password'}, 401
            return {'message': 'this user has been disabled'}, 401
        return {'message': 'User not found'}, 404

class UserLogout(Resource):

    @jwt_required
    def post(self):
        jwt_id = get_raw_jwt()['jti']
        BLACKLIST.add(jwt_id)
        return {'message': 'Logged out successfully!'}, 200
