from collections import defaultdict
from api.models.crud import retrieve_user_tuples_from_table
from api.database.db_connection import OPEN_STOCKS_TABLE
from api.models.open_stocks.open_stocks import OpenStock
from api.models.crud import retrieve_stock_info_from_stocks_price_table


class Portfolio(OpenStock):
    def __init__(self, user_id=None):

        super().__init__()
        self.user_id = user_id
        self.valid = self._validation()

    def _validation(self):
        if self._validate_user_id:
            return True
        else:
            return False

    def _set_message(self, message):
        self.message = message


class GetPortfolio(Portfolio):

    def __init__(self, user_id=None):

        super().__init__()
        self.user_id = user_id
        self.valid = self._validation()
        self.crud = self._crud()
        self.portfolio_details = self._get_portfolio_details()
        self.portfolio_totals = self._get_portfolio_totals()

    def json_data(self):
        return {'User': self.user_id, 'Portfolio totals': self.portfolio_totals,
                'Portfolio details': self.portfolio_details}

    def _crud(self):
        if self.valid:
            tuples = retrieve_user_tuples_from_table(OPEN_STOCKS_TABLE, self.user_id)
            return tuples
        else:
            return None

    def _get_portfolio_details(self):
        if self.crud:
            portfolio_dict = defaultdict(list)
            for line in self.crud:
                portfolio = line[0]
                stock_symbol = line[1]
                mean_price = round(line[2], 2)
                quantity = line[3]
                total_invested = mean_price * quantity

                try:
                    #symbol, name, price, updated_at = request_stock_price(stock_symbol)
                    symbol, name, price, updated_at, _ = retrieve_stock_info_from_stocks_price_table(stock_symbol)
                    current_total = round(price * quantity, 2)
                    result = round(round(price * quantity, 2) - (mean_price * quantity), 2)
                    price_variation = round(GetPortfolio.calculate_variation(price, mean_price), 2)
                    portfolio_dict[portfolio].append({'Stock': stock_symbol, 'Name': name,
                                                      'Mean price': mean_price, 'Quantity': quantity,
                                                      'Total invested': total_invested, 'Current price': price,
                                                      'Variation': price_variation, 'Current total': current_total,
                                                      'Result': result, 'Updated_at': str(updated_at)})
                except Exception as e:
                    print(e)
                    portfolio_dict[portfolio].append({'Stock': stock_symbol, 'Name': None,
                                                      'Mean price': mean_price, 'Quantity': quantity,
                                                      'Total invested': total_invested, 'Current price': None,
                                                      'Variation': None, 'Current total': None, 'Result': None,
                                                      'Updated_at': None})

            return portfolio_dict
        else:
            self._set_message('Portfolio not found')
            return None

    def _get_portfolio_totals(self):
        if self.portfolio_details:
            portfolio_totals_dict = {}
            for portfolio in self.portfolio_details:
                total_invested = 0
                quantity = 0
                current_total = 0
                for stock in self.portfolio_details[portfolio]:
                    total_invested += stock['Total invested']
                    quantity += stock['Quantity']
                    current_total += stock['Current total']
                portfolio_totals_dict[portfolio] = {'Quantity': quantity, 'Total invested': total_invested,
                                                    'Current total': current_total,
                                                    'Total variation': round(self.calculate_variation(current_total,
                                                                                                      total_invested),
                                                                             2)}

            return portfolio_totals_dict
        else:
            self._set_message('Portfolio not found')
            return None

    @staticmethod
    def calculate_variation(current_price, mean_price):
        return ((current_price / mean_price) - 1) * 100
