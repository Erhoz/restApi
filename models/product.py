from sql_alchemy import banco
from models.log import LogModel


class ProductModel(banco.Model):
    __tablename__ = 'produtos'

    product_id = banco.Column(banco.Integer, primary_key=True)
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
            'product_id' : self.product_id,
            'description' : self.description,
            'barcod' : self.barcod,
            'pbuy' : self.pbuy,
            'psell' : self.psell,
            'estoque' : self.estoque
            }

    @classmethod
    def find(cls, product_id):
        product = cls.query.filter_by(product_id = int(product_id)).first()
        if product:
            return product
        return None

    @classmethod
    def find_by_barcod(cls, barcod):
        product = cls.query.filter_by(barcod = int(barcod)).first()

    def get_register_log(self):
        return LogModel.get_register_log("produto", self.description, self.product_id)

    def get_modification_log(self):
        return LogModel.get_modification_log("produto", self.description, self.product_id)

    def get_deletion_log(self):
        return LogModel.get_deletion_log("produto", self.description, self.product_id)

    def save(self):
        banco.session.add(self)
        banco.session.flush()
        banco.session.add(get_register_log)
        banco.session.commit()

    def update(self, description, barcod, pbuy, psell, estoque, user):
        banco.session.add(self.get_modification_log())
        self.description = description
        self.barcod = barcod
        self.pbuy = pbuy
        self.psell = psell
        self.estoque = estoque
        banco.session.add(self)
        banco.session.commit()

    def delete(self):
        banco.session.delete(self)
        banco.session.add(self.get_deletion_log())
        banco.session.commit()
