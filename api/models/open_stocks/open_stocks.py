from api.models.crud import check_id_exists_in_table, insert_tuple_on_open_stocks_table, retrieve_tuple_from_id, delete_tuple_from_table_by_id, update_tuples
from api.database.db_connection import OPEN_STOCKS_TABLE
from api.models.open_stocks.valid_ibovespa_symbols import check_if_symbol_is_valid


class OpenStock:

    def __init__(self, id=None, stock=None, date=None, price=None, portfolio=None, user_id=None):

        self.id = id
        self.stock = stock
        self.date = date
        self.price = price
        self.portfolio = portfolio
        self.user_id = user_id
        self.valid = self._validation()
        self.message = None

    def __repr__(self):
        return f'{self.stock} {self.portfolio}'

    def _validate_id(self, table):
        if self.id and (type(self.id) == int):
            if check_id_exists_in_table(self.id, table):
                return True
            else:
                self._set_message('Id not found.')
        else:
            self._set_message('Invalid id.')
            return False

    def _validate_stock(self):
        if self.stock and (type(self.stock) == str) and (len(self.stock) <= 8):
            self.stock = self.stock.upper()
            if check_if_symbol_is_valid(self.stock):
                return True
        else:
            self._set_message('Invalid stock.')
            return False

    def _validate_date(self):
        if self.date:
            return True
        else:
            self._set_message('Invalid date.')
            return False

    def _validate_price(self):
        if self.price and (type(self.price) == float):
            return True
        else:
            self._set_message('Invalid price.')
            return False

    def _validate_portfolio(self):
        if self.portfolio and (type(self.portfolio) == str) and (len(self.portfolio) <= 30):
            return True
        else:
            self._set_message('Invalid portfolio.')
            return False

    def _validate_user_id(self):
        if self.user_id and (type(self.user_id) == int):
            return True
        else:
            self._set_message('Invalid user id.')
            return False

    def _validation(self):
        if self._validate_id(OPEN_STOCKS_TABLE) and self._validate_stock() and self._validate_date() and self._validate_price() \
                and self._validate_portfolio() and self._validate_user_id():
            return True
        else:
            return False

    def _set_message(self, message):
        self.message = message

    def _set_id(self, id):
        self.id = id

    def json_data(self):
        return {'Id': self.id, 'Stock': self.stock, 'Date': str(self.date), 'Price': self.price,
                'Portfolio': self.portfolio, 'User id': self.user_id}


class NewOpenStock(OpenStock):

    def __init__(self, stock=None, date=None, price=None, portfolio=None, user_id=None):

        super().__init__()
        self.stock = stock
        self.date = date
        self.price = price
        self.portfolio = portfolio
        self.user_id = user_id
        self.valid = self._validation()
        self.crud = self._crud()

    def _validation(self):
        if self._validate_stock() and self._validate_date() and self._validate_price() and self._validate_portfolio() \
                and self._validate_user_id():
            return True
        else:
            return False

    def _crud(self):
        if self.valid:
            insert_success, id = insert_tuple_on_open_stocks_table(self)
            self._set_id(id)
            if insert_success:
                return True
            else:
                return False
        else:
            return False


class GetOpenStock(OpenStock):

    def __init__(self, id=None):

        super().__init__()
        self.id = id
        self.valid = self._validation()
        self.crud = self._crud()

    def _validation(self):
        if self._validate_id(OPEN_STOCKS_TABLE):
            return True
        else:
            self._set_message('Invalid id.')
            return False

    def _crud(self):
        if self.valid:
            tuple = retrieve_tuple_from_id(self.id, OPEN_STOCKS_TABLE)
            if tuple:
                self.stock = tuple[1]
                self.date = tuple[2]
                self.price = tuple[3]
                self.portfolio = tuple[4]
                self.user_id = tuple[5]
                self._set_message('Ok.')
                return True
            else:
                self._set_message('Error retrieving id.')
                return False
        else:
            return False


class DeleteOpenStock(OpenStock):
    def __init__(self, id=None):

        super().__init__()
        self.id = id
        self.valid = self._validation()
        self.crud = self._crud()

    def _validation(self):
        if self._validate_id(OPEN_STOCKS_TABLE):
            return True
        else:
            self._set_message('Invalid id.')

    def _crud(self):
        if self.valid:
            if delete_tuple_from_table_by_id(self.id, OPEN_STOCKS_TABLE):
                self._set_message(f'Stock {self.id} deleted.')
                return True
            else:
                return False
        else:
            return False


class EditOpenStock(OpenStock):
    def __init__(self, args):

        super().__init__()
        self.id = args.id
        self.stock = args.stock
        self.date = args.date
        self.price = args.price
        self.portfolio = args.portfolio
        self.user_id = args.user_id
        self.valid = self._validation()
        self.crud = self._crud()

    def _validation(self):
        if self._validate_id(OPEN_STOCKS_TABLE):
            return True
        else:
            self._set_message('Invalid id.')

    def _crud(self):
        if self.id and self._validate_id:
            if self.stock or self.date or self.price or self.portfolio:
                results_list = []
                if self.stock and self._validate_stock():
                    updated_stock = update_tuples(OPEN_STOCKS_TABLE, 'STOCK', self.id, self.stock)
                    if updated_stock:
                        results_list.append(True)
                    else:
                        results_list.append(False)
                if self.date and self._validate_date():
                    updated_stock = update_tuples(OPEN_STOCKS_TABLE, 'DATE', self.id, self.date)
                    if updated_stock:
                        results_list.append(True)
                    else:
                        results_list.append(False)
                if self.price and self._validate_price():
                    updated_stock = update_tuples(OPEN_STOCKS_TABLE, 'PRICE', self.id, self.price)
                    if updated_stock:
                        results_list.append(True)
                    else:
                        results_list.append(False)
                if self.portfolio and self._validate_portfolio():
                    updated_stock = update_tuples(OPEN_STOCKS_TABLE, 'PORTFOLIO', self.id, self.portfolio)
                    if updated_stock:
                        results_list.append(True)
                    else:
                        results_list.append(False)
                if all(i for i in results_list):
                    return True
                else:
                    self._set_message('Fail')
                    return False
            else:
                self._set_message('No update parameters provided.')
        else:
            return False




