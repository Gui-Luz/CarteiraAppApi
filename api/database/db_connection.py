import configparser
import os
import api
import psycopg2

config_file = configparser.ConfigParser()
config_file.read(os.path.dirname(api.__file__) + '/config.ini')
USERS_TABLE = config_file['TABLES']['users']
OPEN_STOCKS_TABLE = config_file['TABLES']['open_stocks']
CLOSED_STOCKS_TABLE = config_file['TABLES']['closed_stocks']
STOCK_PRICES = config_file['TABLES']['stock_prices']
DATABASE = config_file['DATABASE']['database']
HOST = config_file['DATABASE']['host']
USER = config_file['DATABASE']['user']
PASSWORD = config_file['DATABASE']['password']


def connect_to_database():
    conn = psycopg2.connect(database=DATABASE, host=HOST, user=USER, password=PASSWORD)
    conn.cursor()
    return conn
