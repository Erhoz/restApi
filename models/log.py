from sql_alchemy import banco
from datetime import datetime


class LogModel(banco.Model):
    __tablename__ = 'log'

    log_id = banco.Column(banco.Integer, primary_key=True)
    msg = banco.Column(banco.String(500))
    timestamp = banco.Column(banco.DateTime)
    user = banco.Column(banco.String(50))

    def __init__(self, msg, user):
        self.msg = msg
        self.timestamp = datetime.now()
        self.user = user

    def json(self):
        return {
            'log_id' : self.log_id,
            'msg' : self.msg,
            'timestamp' : str(self.timestamp),
            'user' : self.user
            }

    @classmethod
    def find(cls, log_id):
        log = cls.query.filter_by(log_id = int(log_id)).first()
        if log:
            return log
        return None
