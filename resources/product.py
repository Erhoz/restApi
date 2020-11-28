from flask_restful import Resource, reqparse
from models.product import ProductModel
from flask_jwt_extended import jwt_required

args = reqparse.RequestParser()
args.add_argument('description')
args.add_argument('barcod')
args.add_argument('pbuy')
args.add_argument('psell')
args.add_argument('estoque')

class Products(Resource):
    @jwt_required
    def get(self):
        return {'products' : [product.json() for product in ProductModel.query.all()]}

    @jwt_required
    def post(self):
        dados = args.parse_args()
        newp = ProductModel(**dados)
        newp.save()
        return newp.json()

class Product(Resource):

    @jwt_required
    def get(self, produto_id):
        produto = ProdutoModel.find_product(int(produto_id))
        if produto:
            return produto.json()
        return {'message' : 'Produto not found'}, 404

    @jwt_required
    def put(self, produto_id):
        dados = Produto.args.parse_args()
        oldp = ProdutoModel.find_product(produto_id)
        if oldp:
            oldp.update_product(**dados)
            return oldp.json(), 200
        newp = ProdutoModel(int(produto_id), **dados)
        produtos.insert_product(newp)
        return newp.json(), 201

    @jwt_required
    def delete(self, produto_id):
        product = ProdutoModel.find_product(produto_id)
        if product:
            product.delete_product()
            return {'message' : 'Hotel deleted'}
        return {'message' : 'Hotel not found'}, 404
