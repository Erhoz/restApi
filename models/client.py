from sql_alchemy import banco
from models.log import LogModel


class ClientModel(banco.Model):
    __tablename__ = 'clients'

    client_id = banco.Column(banco.Integer, primary_key=True)
    cpf_cnpj = banco.Column(banco.String(15))
    name = banco.Column(banco.String(200))
    adress = banco.Column(banco.String(500))
    email = banco.Column(banco.String(100))
    status = banco.Column(banco.Boolean)


    def __init__(self, cpf_cnpj, name, adress, email, status):
        self.cpf_cnpj = cpf_cnpj
        self.name = name
        self.adress = adress
        self.email = email
        self.status = status

    def json(self):
        return {
            'client_id' : self.client_id,
            'cpf_cnpj' : self.cpf_cnpj,
            'name' : self.name,
            'adress' : self.adress,
            'email' : self.email,
            'status' : self.status
            }

    @classmethod
    def find(cls, client_id):
        client = cls.query.filter_by(client_id = client_id).first()
        if client:
            return client
        return None

    @classmethod
    def find_by_cpf_cnpj(cls, cpf_cnpj):
        client = cls.query.filter_by(cpf_cnpj = int(cpf_cnpj)).first()

    def get_register_log(self):
        return LogModel.get_register_log("cliente", self.name, self.client_id)

    def get_modification_log(self):
        return LogModel.get_modification_log("cliente", self.name, self.client_id)

    def get_deactivation_log(self):
        return LogModel.get_deactivation_log("cliente", self.name, self.user_id)

    def save(self):
        banco.session.add(self)
        banco.session.flush()
        banco.session.add(get_register_log)
        banco.session.commit()

    def update(self, cpf_cnpj, name, adress, email, status):
        banco.session.add(self.get_modification_log())
        self.cpf_cnpj = cpf_cnpj
        self.name = name
        self.adress = adress
        self.email = email
        self.status = status
        banco.session.add(self)
        banco.session.commit()

    def deactive(self):
        self.status = False
        banco.session.add(self)
        banco.session.add(self.get_deactivation_log())
        banco.session.commit()
