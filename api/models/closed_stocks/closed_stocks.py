from api.models.open_stocks.open_stocks import OpenStock
from api.models.crud import check_id_exists_in_table, retrieve_tuple_from_id, insert_tuple_on_closed_stocks_table, delete_tuple_from_table_by_id, update_tuples
from api.database.db_connection import OPEN_STOCKS_TABLE, CLOSED_STOCKS_TABLE


class ClosedStock(OpenStock):
    def __init__(self, sold_price=None, sold_date=None):

        super().__init__()
        self.sold_price = sold_price
        self.sold_date = sold_date

    def _validate_id(self, table):
        if self.id:
            if check_id_exists_in_table(self.id, table):
                return True
            else:
                self._set_message('Id not found.')
                return False
        else:
            self._set_message('No id provided.')
            return False

    def _validate_sold_price(self):
        if self.sold_price and (type(self.sold_price) == float):
            return True
        else:
            self._set_message('Invalid price.')
            return False

    def _validate_sold_date(self):
        if self.sold_date:
            return True
        else:
            self._set_message('Invalid date.')
            return False

    def json_data(self):
        return {'Id': self.id, 'Stock': self.stock, 'Date': str(self.date), 'Price': self.price, 'Sold Date': str(self.sold_date),
                'Sold Price': self.sold_price, 'Portfolio': self.portfolio, 'User id': self.user_id}


class NewClosedStock(ClosedStock):
    def __init__(self, id=None, sold_price=None, sold_date=None):

        super().__init__()
        self.id = id
        self.sold_price = sold_price
        self.sold_date = sold_date
        self.valid = self._validation()
        self.crud = self._crud()

    def _validation(self):
        if self._validate_id(OPEN_STOCKS_TABLE) and self._validate_sold_price() and self._validate_sold_date():
            return True
        else:
            return False

    def _crud(self):
        if self.valid:
            self._set_message('Ok.')
            tuple = retrieve_tuple_from_id(self.id, OPEN_STOCKS_TABLE)
            self.id = tuple[0]
            self.stock = tuple[1]
            self.date = tuple[2]
            self.price = tuple[3]
            self.portfolio = tuple[4]
            self.user_id = tuple[5]
            if insert_tuple_on_closed_stocks_table(self):
                if delete_tuple_from_table_by_id(self.id, OPEN_STOCKS_TABLE):
                    return True
            else:
                self._set_message('Error adding stock to database.')
        else:
            return False


class DeleteClosedStock(ClosedStock):
    def __init__(self, id=None):

        super().__init__()
        self.id = id
        self.valid = self._validation()
        self.crud = self._crud()

    def _validation(self):
        if self._validate_id(CLOSED_STOCKS_TABLE):
            return True
        else:
            return False

    def _crud(self):
        if self.valid:
            if delete_tuple_from_table_by_id(self.id, CLOSED_STOCKS_TABLE):
                self._set_message(f'Stock {self.id} deleted.')
                return True
        else:
            return False

class GetClosedStock(ClosedStock):
    def __init__(self, id=None):

        super().__init__()
        self.id = id
        self.valid = self._validation()
        self.crud = self._crud()

    def _validation(self):
        if self._validate_id(CLOSED_STOCKS_TABLE):
            return True
        else:
            return False

    def _crud(self):
        if self.valid:
            self._set_message('Ok.')
            tuple = retrieve_tuple_from_id(self.id, CLOSED_STOCKS_TABLE)
            if tuple:
                self.id = tuple[0]
                self.stock = tuple[1]
                self.date = tuple[2]
                self.price = tuple[3]
                self.portfolio = tuple[4]
                self.user_id = tuple[5]
                self.sold_price = tuple[6]
                self.sold_date = tuple[7]
                return True
            else:
                return False
        else:
            return False


class EditClosedStock(ClosedStock):
    def __init__(self, args):

        super().__init__()
        self.id = args.id
        self.stock = args.stock
        self.date = args.date
        self.price = args.price
        self.portfolio = args.portfolio
        self.user_id = args.user_id
        self.sold_date = args.sold_date
        self.sold_price = args.sold_price
        self.valid = self._validation()
        self.crud = self._crud()

    def _validation(self):
        if self._validate_id(CLOSED_STOCKS_TABLE):
            return True
        else:
            return False

    def _crud(self):
        if self.valid:
            if self.stock or self.date or self.price or self.portfolio:
                results_list = []
                if self.stock and self._validate_stock():
                    updated_stock = update_tuples(CLOSED_STOCKS_TABLE, 'STOCK', self.id, self.stock)
                    if updated_stock:
                        results_list.append(True)
                    else:
                        results_list.append(False)
                if self.date and self._validate_date():
                    updated_stock = update_tuples(CLOSED_STOCKS_TABLE, 'DATE', self.id, self.date)
                    if updated_stock:
                        results_list.append(True)
                    else:
                        results_list.append(False)
                if self.price and self._validate_price():
                    updated_stock = update_tuples(CLOSED_STOCKS_TABLE, 'PRICE', self.id, self.price)
                    if updated_stock:
                        results_list.append(True)
                    else:
                        results_list.append(False)
                if self.portfolio and self._validate_portfolio():
                    updated_stock = update_tuples(CLOSED_STOCKS_TABLE, 'PORTFOLIO', self.id, self.portfolio)
                    if updated_stock:
                        results_list.append(True)
                    else:
                        results_list.append(False)
                if self.sold_date and self._validate_sold_date():
                    updated_stock = update_tuples(CLOSED_STOCKS_TABLE, 'SOLD_DATE', self.id, self.sold_date)
                    if updated_stock:
                        results_list.append(True)
                    else:
                        results_list.append(False)
                if self.sold_price and self._validate_sold_price():
                    updated_stock = update_tuples(CLOSED_STOCKS_TABLE, 'SOLD_PRICE', self.id, self.sold_price)
                    if updated_stock:
                        results_list.append(True)
                    else:
                        results_list.append(False)
                if all(i for i in results_list):
                    self._set_message(f'Stock {self.id} updated.')
                    return True
                else:
                    self._set_message('Fail')
                    return False
            else:
                self._set_message('No update parameters provided.')
        else:
            return False
