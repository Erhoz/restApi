from flask_restful import Resource, reqparse
from models.log import LogModel
from flask_jwt_extended import jwt_required

class Logs(Resource):
    @jwt_required
    def get(self):
        return {'logs' : [log.json() for log in LogModel.query.all()]}
