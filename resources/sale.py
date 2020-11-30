from flask_restful import Resource, reqparse
from models.sale import saleModel
from flask_jwt_extended import jwt_required

args = reqparse.RequestParser()
args.add_argument('client_id')
args.add_argument('total')
args.add_argument('timestamp')
args.add_argument('effective')

class Sales(Resource):
    @jwt_required
    def get(self):
        return {'sales' : [sale.json() for sale in saleModel.query.all()]}

    @jwt_required
    def post(self, client_id):
        dados = args.parse_args()
        news = SaleModel(client_id)
        news.save()
        return news.json()

class Sale(Resource):

    @jwt_required
    def get(self, produto_id):
        produto = ProdutoModel.find(produto_id)
        if produto:
            return produto.json()
        return {'message' : 'Produto not found'}, 404

    @jwt_required
    def put(self, produto_id):
        dados = Produto.args.parse_args()
        oldp = ProdutoModel.find(produto_id)
        if oldp:
            oldp.update(**dados)
            return oldp.json(), 200
        newp = ProdutoModel(produto_id, **dados)
        produtos.save(newp)
        return newp.json(), 201

    @jwt_required
    def delete(self, produto_id):
        sale = ProdutoModel.find_sale(produto_id)
        if sale:
            sale.delete()
            return {'message' : 'Hotel deleted'}
        return {'message' : 'Hotel not found'}, 404
