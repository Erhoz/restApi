from flask_restful import Resource, reqparse
from models.produto import ProdutoModel

class Produtos(Resource):
    def get(self):
        return {'produtos' : [produto.json() for produto in ProdutoModel.query.all()]}

class Produto(Resource):
    args = reqparse.RequestParser()
    args.add_argument('description')
    args.add_argument('barcod')
    args.add_argument('pbuy')
    args.add_argument('psell')
    args.add_argument('estoque')

    def get(self, produto_id):
        produto = ProdutoModel.find_product(int(produto_id))
        if produto:
            return produto.json()
        return {'message' : 'Produto not found'}, 404

    def post(self, produto_id):
        if ProdutoModel.find_product(produto_id):
            return{"message" : "Produto id '{}' already exists. ".format(produto_id)}, 400

        dados = Produto.args.parse_args()
        newp = ProdutoModel(int(produto_id), **dados)
        newp.save_product()
        return newp.json()

    def put(self, produto_id):
        dados = Produto.args.parse_args()
        oldp = ProdutoModel.find_product(produto_id)
        if oldp:
            oldp.update_product(**dados)
            oldp.save_product()
            return oldp.json(), 200
        newp = ProdutoModel(int(produto_id), **dados)
        produtos.insert_product(newp)
        return newp.json(), 201

    def delete(self, produto_id):
        product = ProdutoModel.find_product(produto_id)
        if product:
            product.delete_product()
            return {'message' : 'Hotel deleted'}
        return {'message' : 'Hotel not found'}, 404
