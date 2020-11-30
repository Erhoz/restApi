from sql_alchemy import banco
from models.log import LogModel


class SaleProductModel(banco.Model):
    __tablename__ = 'sale_product'

    sale_product_id = banco.Column(banco.Integer, primary_key=True)
    sale_id = banco.Column(banco.Integer)
    description = banco.Column(banco.String(200))
    barcod = banco.Column(banco.String(32))
    pbuy = banco.Column(banco.Float(precision=2))
    psell = banco.Column(banco.Float(precision=2))
    amount = banco.Column(banco.Float(precision=3))

    def __init__(self, sale_id, description, barcod, pbuy, psell, amount):
        self.sale_id = sale_id
        self.description = description
        self.barcod = barcod
        self.pbuy = pbuy
        self.psell = psell
        self.amount = amount

    def json(self):
        return {
            'sale_product_id' : self.product_id,
            'sale_id' : self.sale_id,
            'description' : self.description,
            'barcod' : self.barcod,
            'pbuy' : self.pbuy,
            'psell' : self.psell,
            'amount' : self.amount
            }

    @classmethod
    def find(cls, sale_product_id):
        product = cls.query.filter_by(sale_product_id = sale_product_id).first()
        if product:
            return product
        return None

    def save(self):
        banco.session.add(self)
        banco.session.commit()

    def delete(self):
        banco.session.delete(self)
        banco.session.commit()
