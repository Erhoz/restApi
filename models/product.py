from sql_alchemy import banco
from models.log import LogModel
from flask_jwt_extended import get_raw_jwt


class ProductModel(banco.Model):
    __tablename__ = 'produtos'

    produto_id = banco.Column(banco.Integer, primary_key=True)
    description = banco.Column(banco.String(200))
    barcod = banco.Column(banco.String(32))
    pbuy = banco.Column(banco.Float(precision=2))
    psell = banco.Column(banco.Float(precision=2))
    estoque = banco.Column(banco.Float(precision=3))

    def __init__(self, description, barcod, pbuy, psell, estoque):
        self.description = description
        self.barcod = barcod
        self.pbuy = pbuy
        self.psell = psell
        self.estoque = estoque

    def json(self):
        return {
            'produto_id' : self.produto_id,
            'description' : self.description,
            'barcod' : self.barcod,
            'pbuy' : self.pbuy,
            'psell' : self.psell,
            'estoque' : self.estoque
            }

    @classmethod
    def find(cls, produto_id):
        product = cls.query.filter_by(produto_id = int(produto_id)).first()
        if product:
            return product
        return None

    @classmethod
    def find_by_barcod(cls, barcod):
        product = cls.query.filter_by(barcod = int(barcod)).first()

    def save(self):
        banco.session.add(self)
        user = get_raw_jwt()['identity']
        log = LogModel("'{}' cadastrou o produto: '{}' com o id: '{}'".format(user, self.description, self.produto_id), user)
        banco.session.add(log)
        banco.session.commit()

    def update_product(self, description, barcod, pbuy, psell, estoque, user):
        self.description = description
        self.barcod = barcod
        self.pbuy = pbuy
        self.psell = psell
        self.estoque = estoque
        banco.session.add(LogModel(user_name + " atualizou o produto: \"" + self.description + "\" com o id: \"" + self.id + "\"", user.id, user.name))
        banco.session.add(self)
        banco.session.commit()

    def delete_product(self):
        banco.session.delete(self)
        banco.session.commit()
