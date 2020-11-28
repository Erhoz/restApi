from flask_restful import Resource, reqparse
from models.client import ClientModel
from flask_jwt_extended import jwt_required

args = reqparse.RequestParser()
args.add_argument('cpf_cnpj')
args.add_argument('name')
args.add_argument('adress')
args.add_argument('email')
args.add_argument('status')

class Clients(Resource):
    @jwt_required
    def get(self):
        return {'clients' : [client.json() for client in ClientModel.query.all()]}

    @jwt_required
    def post(self):
        dados = args.parse_args()
        newc = ClientModel(**dados)
        newc.save()
        return newp.json()

class Client(Resource):

    @jwt_required
    def get(self, client_id):
        client = ClientModel.find(client_id)
        if client:
            return client.json()
        return {'message' : 'client not found'}, 404

    @jwt_required
    def put(self, client_id):
        dados = client.args.parse_args()
        oldc = ClientModel.find(client_id)
        if oldc:
            oldc.update(**dados)
            return oldp.json(), 200
        newc = clientModel(client_id, **dados)
        clients.save(newp)
        return newc.json(), 201

    @jwt_required
    def delete(self, client_id):
        client = ClientModel.find(client_id)
        if client:
            client.delete()
            return {'message' : 'Hotel deleted'}
        return {'message' : 'Hotel not found'}, 404
