from flask_restful import Resource, reqparse
from api.models.operations.operations import NewOperation, DeleteOperation

# Stocks arguments #
parser = reqparse.RequestParser()
parser.add_argument('id', type=int, default=None)
parser.add_argument('stock', type=str, default=None)
parser.add_argument('date', type=str, default=None)
parser.add_argument('sold_date', type=str, default=None)
parser.add_argument('price', type=float, default=None)
parser.add_argument('sold_price', type=float, default=None)
parser.add_argument('portfolio', type=str, default=None)
parser.add_argument('user_id', type=int, default=None)
parser.add_argument('quantity', type=int, default=1)
parser.add_argument('portfolio', type=str, default=None)
parser.add_argument('user_id', type=int, default=None)


class UserOpenOperations(Resource):
    def __init__(self):
        args = parser.parse_args()
        self.stock = args.get('stock')
        self.date = args.get('date')
        self.sold_date = args.get('sold_date')
        self.price = args.get('price')
        self.sold_price = args.get('sold_price')
        self.portfolio = args.get('portfolio')
        self.user_id = args.get('user_id')
        self.quantity = args.get('quantity')

    def post(self):
        new_operation = NewOperation(self.user_id, self.stock, self.date, self.price, self.portfolio, self.quantity)
        if new_operation.valid and new_operation.crud:
            return {'Code': 200, 'Alert': 'Success', 'Data': new_operation.json_data()}
        else:
            return {'Code': 400, 'Alert': 'Fail', 'Message': new_operation.message}

    def delete(self):
        delete_operation = DeleteOperation(self.user_id, self.stock, self.sold_date, self.sold_price, self.portfolio,
                                           self.quantity)
        if delete_operation.valid and delete_operation.crud:
            return {'Code': 200, 'Alert': 'Success', 'Data': delete_operation.json_data()}
        else:
            return {'Code': 400, 'Alert': 'Fail', 'Message': delete_operation.message}






