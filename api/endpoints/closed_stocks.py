from flask_restful import Resource, reqparse
from api.models.closed_stocks.closed_stocks import NewClosedStock, DeleteClosedStock, GetClosedStock, EditClosedStock
from api.database.db_connection import CLOSED_STOCKS_TABLE
from api.models.crud import retrieve_all_tuples_from_table

### USERS arguments ###
parser = reqparse.RequestParser()
parser.add_argument('id', type=int, default=None)
parser.add_argument('stock', type=str, default=None)
parser.add_argument('date', type=str, default=None)
parser.add_argument('price', type=float, default=None)
parser.add_argument('portfolio', type=str, default=None)
parser.add_argument('user_id', type=int, default=None)
parser.add_argument('quantity', type=int, default=1)
parser.add_argument('sold_price', type=float, default=None)
parser.add_argument('sold_date', type=str, default=None)


class AllClosedStocks(Resource):
    def get(self):
        stock_list = retrieve_all_tuples_from_table(CLOSED_STOCKS_TABLE)
        if stock_list:
            stocks_data_list = []
            for line in stock_list:
                stock_data = {'Id': line[0], 'Stock': line[1], 'Date': str(line[2]), 'Price': line[3], 'Sold date': str(line[7]),
                              'Sold price': line[6], 'Portfolio': line[4], 'User_id': line[5]}
                stocks_data_list.append(stock_data)
            if stocks_data_list:
                return {'Code': 200, 'Alert': 'Success', 'Size': len(stocks_data_list), 'Data': stocks_data_list}
            else:
                return {'Code': 400, 'Alert': 'Database is empty.'}
        else:
            return {'Code': 400, 'Alert': 'Database is empty.'}


class ClosedStock(Resource):

    def __init__(self):
        args = parser.parse_args()
        self.id = args.get('id')
        self.stock = args.get('stock')
        self.date = args.get('date')
        self.price = args.get('price')
        self.portfolio = args.get('portfolio')
        self.user_id = args.get('user_id')
        self.sold_price = args.get('sold_price')
        self.sold_date = args.get('sold_date')

    def post(self):
        new_closed_stock = NewClosedStock(self.id, self.sold_price, self.sold_date)
        if new_closed_stock.valid and new_closed_stock.crud:
            return {'Code': 200, 'Alert': 'Success', 'Data': new_closed_stock.json_data()}
        else:
            return {'Code': 400, 'Alert': 'Fail', 'Message': new_closed_stock.message}

    def get(self):
        new_closed_stock = GetClosedStock(self.id)
        if new_closed_stock.valid and new_closed_stock.crud:
            return {'Code': 200, 'Alert': 'Success', 'Data': new_closed_stock.json_data()}
        else:
            return {'Code': 400, 'Alert': 'Fail', 'Message': new_closed_stock.message}

    def delete(self):
        delete_closed_stock = DeleteClosedStock(self.id)
        if delete_closed_stock.valid and delete_closed_stock.crud:
            return {'Code': 200, 'Alert': 'Success', 'Data': delete_closed_stock.message}
        else:
            return {'Code': 400, 'Alert': 'Fail', 'Message': delete_closed_stock.message}

    def put(self):
        edit_stock = EditClosedStock(self)
        if edit_stock.valid and edit_stock.crud:
            edit_stock = GetClosedStock(self.id)
            return {'Code': 200, 'Alert': 'Success', 'Message': edit_stock.message, 'Data': edit_stock.json_data()}
        else:
            return {'Code': 400, 'Alert': 'Fail', 'Message': edit_stock.message}

