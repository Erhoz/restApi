from sql_alchemy import banco
from models.log import LogModel
from datetime import datetime


class SaleModel(banco.Model):
    __tablename__ = 'sale'

    sale_id = banco.Column(banco.Integer, primary_key=True)
    client_id = banco.Column(banco.Integer)
    total = banco.Column(banco.Float(precision=2))
    timestamp = banco.Column(banco.DateTime)
    effective = banco.Column(banco.Boolean)

    def __init__(self, client_id, total, timestamp, effective):
        self.client_id = client_id
        self.total = total
        self.timestamp = timestamp
        self.effective = effective

    def json(self):
        return {
            'sale_id' : self.sale_id,
            'client_id' : self.client_id,
            'total' : self.total,
            'timestamp' : self.timestamp,
            'effective' : self.effective,
            }

    @classmethod
    def find(cls, sale_id):
        sale = cls.query.filter_by(sale_id = sale_id).first()
        if sale:
            return sale
        return None

    def get_init_log(self):
        return LogModel.get_init_log("venda", self.description, self.sale_id)

    def get_modification_log(self):
        return LogModel.get_modification_log("venda", self.description, self.sale_id)

    def get_deletion_log(self):
        return LogModel.get_deletion_log("venda", self.description, self.sale_id)

    def save(self):
        banco.session.add(self)
        banco.session.flush()
        banco.session.add(self.get_init_log())
        banco.session.commit()

    def delete(self):
        banco.session.delete(self)
        banco.session.add(self.get_deletion_log())
        banco.session.commit()
