from collections import defaultdict
from api.models.closed_stocks.closed_stocks import ClosedStock
from api.models.crud import retrieve_user_open_records, retrieve_user_closed_records, check_id_exists_in_table
from api.database.db_connection import USERS_TABLE


class GetUserRecords(ClosedStock):
    def __init__(self, user_id=None):

        super().__init__()
        self.user_id = user_id
        self.stocks = defaultdict(list)
        self.records_totals = None
        self.valid = self._validation()
        self.crud = self._crud()

    def json_data(self):
        return {'User': self.user_id, 'Stocks': self.stocks, 'Totals': self.results}

    def _validation(self):
        if self.user_id and check_id_exists_in_table(self.user_id, USERS_TABLE):
            return True
        else:
            return False

    def _get_open_stocks(self):
        tuples = retrieve_user_open_records(self.user_id)
        for stock_tuple in tuples:
            stock, date, price, portfolio, quantity = stock_tuple
            self.stocks[portfolio].append({'Stock': stock, 'Date': str(date), 'Price': price, 'Sold date': None,
                                           'Sold price': None, 'Quantity': quantity, 'Result': 0,
                                           'Status': 'Open'})
        return True

    def _get_closed_stocks(self):
        tuples = retrieve_user_closed_records(self.user_id)
        for stock_tuple in tuples:
            stock, date, price, portfolio, sold_price, sold_date, quantity = stock_tuple
            result = (sold_price - price) * quantity
            self.stocks[portfolio].append(
                {'Stock': stock, 'Date': str(date), 'Price': price, 'Sold date': str(sold_date),
                 'Sold price': sold_price, 'Quantity': quantity, 'Result': result, 'Status': 'Closed'})
        return True

    def _get_closed_results(self):
        portfolio_results = {}
        for portfolio in self.stocks:
            results = 0
            for line in self.stocks[portfolio]:
                results += line['Result']
            portfolio_results[portfolio] = results
        self.results = portfolio_results
        return True

    def _crud(self):
        if self.valid:
            self._get_open_stocks()
            self._get_closed_stocks()
            self._get_closed_results()
            return True
        else:
            self._set_message('Some error ocurred.')
            return False
