from flask_restful import Resource, reqparse
from api.models.portfolios.portfolio import GetPortfolio

# Stocks arguments #
parser = reqparse.RequestParser()
parser.add_argument('portfolio', type=str, default=None)
parser.add_argument('user_id', type=int, default=None)


class Portfolio(Resource):
    def __init__(self):
        args = parser.parse_args()
        self.user_id = args.get('user_id')

    def get(self):
        get_operations = GetPortfolio(self.user_id)
        if get_operations.valid and get_operations.crud:
            return {'Code': 200, 'Alert': 'Success', 'Data': get_operations.json_data()}
        else:
            return {'Code': 400, 'Alert': 'Fail', 'Message': get_operations.message}
