import configparser
import os
from flask import Flask
from flask_restful import Api
from api.endpoints.users import User, AllUsers, AuthentinticateUser
from api.endpoints.open_stocks import OpenStock, AllOpenStocks
from api.endpoints.closed_stocks import ClosedStock, AllClosedStocks
from api.endpoints.operations import UserOpenOperations
from api.endpoints.portfolios import Portfolio
from api.endpoints.records import UserRecords

config_file = configparser.ConfigParser()
#config_file.read('config.ini')
config_file.read(os.path.dirname(__file__) + '/config.ini')


#ENV
DEBUG = bool(config_file['ENV']['debug'])
PORT = int(config_file['ENV']['port'])


app = Flask(__name__)
app.config['SECRET-KEY'] = config_file['APP']['secret_key']
api_server = Api(app)


# Endpoints #
api_server.add_resource(User, config_file['ENDPOINTS']['user'])
api_server.add_resource(AllUsers, config_file['ENDPOINTS']['all_users'])
api_server.add_resource(AuthentinticateUser, config_file['ENDPOINTS']['auth_user'])

api_server.add_resource(OpenStock, config_file['ENDPOINTS']['open_stock'])
api_server.add_resource(AllOpenStocks, config_file['ENDPOINTS']['all_open_stocks'])

api_server.add_resource(ClosedStock, config_file['ENDPOINTS']['closed_stock'])
api_server.add_resource(AllClosedStocks, config_file['ENDPOINTS']['all_closed_stocks'])

api_server.add_resource(UserOpenOperations, config_file['ENDPOINTS']['open_operations'])

api_server.add_resource(Portfolio, config_file['ENDPOINTS']['portfolios'])
api_server.add_resource(UserRecords, config_file['ENDPOINTS']['records'])


if __name__ == '__main__':
    app.run(debug=DEBUG, port=PORT)
