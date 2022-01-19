from api.models.open_stocks.open_stocks import OpenStock
from api.models.crud import insert_tuple_on_open_stocks_table, select_stocks_for_closing, \
    insert_tuple_on_closed_stocks_table, retrieve_tuple_from_id, delete_tuple_from_table_by_id
from api.database.db_connection import OPEN_STOCKS_TABLE


class Operation(OpenStock):
    def __init__(self, quantity=1):

        super().__init__()
        self.quantity = quantity

    def _validate_quantity(self):
        if self.quantity and type(self.quantity) == int:
            return True
        else:
            self._set_message('Invalid quantity')

    def json_data(self):
        return {'Stock': self.stock, 'Date': self.date, 'Price': self.price,
                'Portfolio': self.portfolio, 'User id': self.user_id, 'Quantity': self.quantity}


class NewOperation(Operation):
    def __init__(self, user_id=None, stock=None, date=None, price=None, portfolio=None, quantity=1):

        super().__init__()
        self.user_id = user_id
        self.stock = stock
        self.date = date
        self.price = price
        self.portfolio = portfolio
        self.quantity = quantity
        self.valid = self._validation()
        self.crud = self._crud()

    def _validation(self):
        if self._validate_user_id and self._validate_stock() and self._validate_date() and self._validate_price() and \
                self._validate_quantity():
            return True
        else:
            return False

    # def _crud1(self):
    #     if self.valid:
    #         for i in range(self.quantity):
    #             result, id = insert_tuple_on_open_stocks_table(self)
    #             self._set_id(id)
    #             if result:
    #                 self._set_message('Operation added to database.')
    #             else:
    #                 self._set_message('Some error occurred.')
    #                 return False
    #         return True
    #     else:
    #         return False

    def _crud(self):
        if self.valid:
            result, id = insert_tuple_on_open_stocks_table(self)
            self._set_id(id)
            if result:
                self._set_message('Operation added to database.')
            else:
                self._set_message('Some error occurred.')
                return False
            return True
        else:
            return False


class DeleteOperation(NewOperation):
    def __init__(self, user_id=None, stock=None, sold_date=None, sold_price=None,
                 portfolio=None, quantity=1):

        super().__init__()
        self.user_id = user_id
        self.stock = stock
        self.portfolio = portfolio
        self.quantity = quantity
        self.sold_date = sold_date
        self.sold_price = sold_price
        self.valid = self._validation()
        self.crud = self._crud()

    def json_data(self):
        return {'Stock': self.stock, 'Portfolio': self.portfolio, 'Quantity': self.quantity, 'Closed stock ids': self.ids}

    def _validate_sold_date(self):
        if self.sold_date:
            return True
        else:
            self._set_message('Invalid date.')
            return False

    def _validate_sold_price(self):
        if self.sold_price and (type(self.sold_price) == float):
            return True
        else:
            self._set_message('Invalid sold price.')
            return False

    def _validation(self):
        if self._validate_user_id() and self._validate_stock() and self._validate_sold_date() and \
                self._validate_sold_price() and self._validate_quantity():
            return True
        else:
            return False

    def _crud(self):
        if self.valid:
            all_ids = select_stocks_for_closing(self.user_id, self.stock, self.portfolio)
            ids = all_ids[:self.quantity]
            if ids:
                self.ids = ids
                stocks_info = []
                for id_number in ids:
                    stock_tuple = retrieve_tuple_from_id(id_number, OPEN_STOCKS_TABLE)
                    stocks_info.append(stock_tuple)
                for tuple in stocks_info:
                    self.id = tuple[0]
                    self.date = tuple[2]
                    self.price = tuple[3]
                    insert_tuple_on_closed_stocks_table(self)
                    delete_tuple_from_table_by_id(tuple[0], OPEN_STOCKS_TABLE)
                self._set_message('Operation closed.')
                return True
            else:
                self._set_message('Some error ocurred.')
                return False
        else:
            return False
