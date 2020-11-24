from sql_alchemy import banco


class ProdutoModel(banco.Model):
    __tablename__ = 'produto'

    produto_id = banco.Column(banco.Integer, primary_key=True)
    description = banco.Column(banco.String(200))
    barcod = banco.Column(banco.String(32))
    pbuy = banco.Column(banco.Float(precision=2))
    psell = banco.Column(banco.Float(precision=2))
    estoque = banco.Column(banco.Float(precision=3))

    def __init__(self, produto_id, description, barcod, pbuy, psell, estoque):
        self.produto_id = produto_id
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
    def find_product(cls, produto_id):
        product = cls.query.filter_by(produto_id = int(produto_id)).first()
        if product:
            return product
        return None

    def save_product(self):
        banco.session.add(self)
        banco.session.commit()

    def update_product(self, description, barcod, pbuy, psell, estoque):
        self.description = description
        self.barcod = barcod
        self.pbuy = pbuy
        self.psell = psell
        self.estoque = estoque

    def delete_product(self):
        banco.session.delete(self)
        banco.session.commit()
