from flask_restful import Resource, reqparse
from api.models.records.records import GetUserRecords

# Stocks arguments #
parser = reqparse.RequestParser()
parser.add_argument('user_id', type=str, default=None)


class UserRecords(Resource):

    def __init__(self):
        args = parser.parse_args()
        self.user_id = args.get('user_id')

    def get(self):
        get_records = GetUserRecords(self.user_id)
        if get_records.valid and get_records.crud:
            return {'Code': 200, 'Alert': 'Success', 'Data': get_records.json_data()}
        else:
            return {'Code': 400, 'Alert': 'Fail', 'Message': get_records.message}