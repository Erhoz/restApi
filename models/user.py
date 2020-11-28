from sql_alchemy import banco
from models.log import LogModel


class UserModel(banco.Model):
    __tablename__ = 'users'

    user_id = banco.Column(banco.Integer, primary_key=True)
    name = banco.Column(banco.String(50), unique_key=True)
    password = banco.Column(banco.String(40))
    status = banco.Column(banco.Boolean)

    def __init__(self, name, password, status):
        self.name = name
        self.password = password
        self.status = status

    def json(self):
        return {
            'user_id' : self.user_id,
            'name' : self.name,
            'status' : self.status
            }

    @classmethod
    def find(cls, user_id):
        user = cls.query.filter_by(user_id = int(user_id)).first()
        if user:
            return user
        return None

    @classmethod
    def find_by_name(cls, name):
        user = cls.query.filter_by(name = name).first()
        if user:
            return user
        return None

    def crate(self):
        self.status = True
        banco.session.add(self)
        banco.session.add(LogModel("'{}' cadastrou o usuario: '{}' com o id: '{}'".format("user", "user_name", "user_id")))
        banco.session.commit()

    def create_without_log(self):
        self.status = True
        banco.session.add(self)
        banco.session.commit()

    def change_pass(self, new_pass):
        self.password = new_pass
        banco.session.add(self)
        banco.session.add(LogModel("'{}' mudou a senha do usuario: '{}' com o id: '{}'".format("user", "user_name", "user_id")))
        banco.session.commit()


    def deactive(self):
        self.status = False
        banco.session.add(self)
        banco.session.add(LogModel("'{}' desativou o usuario: '{}' com o id: '{}'".format("user", "user_name", "user_id")))
        banco.session.commit()
