from flask_restful import Resource, reqparse
from api.models.open_stocks.open_stocks import NewOpenStock, GetOpenStock, DeleteOpenStock, EditOpenStock
from api.models.crud import retrieve_all_tuples_from_table
from api.database.db_connection import OPEN_STOCKS_TABLE

# Stocks arguments #
parser = reqparse.RequestParser()
parser.add_argument('id', type=int, default=None)
parser.add_argument('stock', type=str, default=None)
parser.add_argument('date', type=str, default=None)
parser.add_argument('price', type=float, default=None)
parser.add_argument('portfolio', type=str, default=None)
parser.add_argument('user_id', type=int, default=None)
parser.add_argument('quantity', type=int, default=1)


class AllOpenStocks(Resource):

    def get(self):
        stock_list = retrieve_all_tuples_from_table(OPEN_STOCKS_TABLE)
        if stock_list:
            stocks_data_list = []
            for line in stock_list:
                stock_data = {'Id': line[0], 'Stock': line[1], 'Date': str(line[2]), 'Price': line[3], 'Portfolio': line[4], 'User_id': line[5]}
                stocks_data_list.append(stock_data)
            if stocks_data_list:
                return {'Code': 200, 'Alert': 'Success', 'Size': len(stocks_data_list), 'Data': stocks_data_list}
            else:
                return {'Code': 400, 'Alert': 'Database is empty.'}
        else:
            return {'Code': 400, 'Alert': 'Database is empty.'}


class OpenStock(Resource):

    def __init__(self):
        args = parser.parse_args()
        self.id = args.get('id')
        self.stock = args.get('stock')
        self.date = args.get('date')
        self.price = args.get('price')
        self.portfolio = args.get('portfolio')
        self.user_id = args.get('user_id')

    def post(self):

        new_open_stock = NewOpenStock(self.stock, self.date, self.price, self.portfolio, self.user_id)
        if new_open_stock.valid and new_open_stock.crud:
            return {'Code': 200, 'Alert': 'Success', 'Data': new_open_stock.json_data()}
        else:
            return {'Code': 400, 'Alert': 'Fail', 'Message': new_open_stock.message}

    def get(self):
        get_stock = GetOpenStock(self.id)
        if get_stock.valid and get_stock.crud:
            return {'Code': 200, 'Alert': 'Success', 'Data': get_stock.json_data()}
        else:
            return {'Code': 400, 'Alert': 'Fail', 'Message': get_stock.message}

    def delete(self):
        delete_stock = DeleteOpenStock(self.id)
        if delete_stock.valid and delete_stock.crud:
            return {'Code': 200, 'Alert': 'Success', 'Data': delete_stock.message}
        else:
            return {'Code': 400, 'Alert': 'Fail', 'Message': delete_stock.message}

    def put(self):
        edit_stock = EditOpenStock(self)
        if edit_stock.valid and edit_stock.crud:
            edit_stock = GetOpenStock(edit_stock.id)
            return {'Code': 200, 'Alert': 'Success', 'Message': edit_stock.message, 'Data': edit_stock.json_data()}
        else:
            return {'Code': 400, 'Alert': 'Fail', 'Message': edit_stock.message}
