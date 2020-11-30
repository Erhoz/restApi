from sql_alchemy import banco
from datetime import datetime
from flask_jwt_extended import get_raw_jwt

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

    @classmethod
    def get_log_action(cls, action, class_name, object_name, object_id):
        user = get_raw_jwt()['identity']
        log = LogModel("'{}' {} {}: '{}' com o id: '{}'".format(user, action, class_name, object_name, object_id), user)
        return log

    @classmethod
    def get_register_log(cls, class_name, object_name, object_id):
        return LogModel.get_log_action("cadastrou", class_name, object_name, object_id)

    @classmethod
    def get_init_log(cls, class_name, object_name, object_id):
        return LogModel.get_log_action("inciou", class_name, object_name, object_id)

    @classmethod
    def get_modification_log(cls, class_name, object_name, object_id):
        return LogModel.get_log_action("modificou", class_name, object_name, object_id)

    @classmethod
    def get_deactivation_log(cls, class_name, object_name, object_id):
        return LogModel.get_log_action("desativou", class_name, object_name, object_id)

    @classmethod
    def get_deletion_log(cls, class_name, object_name, object_id):
        return LogModel.get_log_action("deletou", class_name, object_name, object_id)
