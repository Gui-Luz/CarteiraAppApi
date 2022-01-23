from api.database.db_connection import connect_to_database, OPEN_STOCKS_TABLE, USERS_TABLE, CLOSED_STOCKS_TABLE, \
    STOCK_PRICES


def sql():
    conn = connect_to_database()
    cursor = conn.cursor()
    return cursor, conn


# READ #
def retrieve_all_tuples_from_table(table):
    syntax = f"SELECT * FROM {table};"
    cursor, conn = sql()
    cursor.execute(syntax)
    tuples = cursor.fetchall()
    conn.close()
    return tuples


def retrieve_user_tuples_from_table(table, user_id):
    syntax = f"SELECT PORTFOLIO, STOCK, AVG (PRICE), COUNT (STOCK) FROM {table} WHERE USER_ID = {user_id} GROUP BY PORTFOLIO, STOCK;"
    cursor, conn = sql()
    cursor.execute(syntax)
    tuples = cursor.fetchall()
    conn.close()
    return tuples


def retrieve_user_closed_records(user_id):
    syntax = f"SELECT STOCK, DATE, PRICE, PORTFOLIO, SOLD_PRICE, SOLD_DATE, " \
             f"COUNT (ID) , array_agg (ID) as id_list FROM closed_stocks WHERE USER_ID = {user_id} GROUP BY STOCK, DATE, PRICE, PORTFOLIO, SOLD_PRICE, " \
             f"SOLD_DATE;"
    cursor, conn = sql()
    cursor.execute(syntax)
    tuples = cursor.fetchall()
    conn.close()
    return tuples


def retrieve_user_open_records(user_id):
    syntax = f"SELECT STOCK, DATE, PRICE, PORTFOLIO, " \
             f"COUNT (ID) , array_agg (ID) as id_list FROM open_stocks WHERE USER_ID = {user_id} GROUP BY STOCK, DATE, PRICE, PORTFOLIO;"
    cursor, conn = sql()
    cursor.execute(syntax)
    tuples = cursor.fetchall()
    conn.close()
    return tuples


def check_id_exists_in_table(id, table):
    syntax = f"SELECT EXISTS(SELECT * FROM {table} WHERE ID = {id});"
    cursor, conn = sql()
    cursor.execute(syntax)
    result_bol = cursor.fetchone()[0]
    conn.close()
    if result_bol == 1:
        return True
    else:
        return False


def retrieve_tuple_from_id(id, table):
    syntax = f"SELECT * FROM {table} WHERE ID = {id};"
    cursor, conn = sql()
    cursor.execute(syntax)
    tuple = cursor.fetchone()
    conn.close()
    return tuple


def retrieve_stock_info_from_stocks_price_table(stock):
    syntax = f"SELECT * FROM {STOCK_PRICES} WHERE stock = '{stock}';"
    cursor, conn = sql()
    cursor.execute(syntax)
    tuple = cursor.fetchone()
    conn.close()
    return tuple


def select_username_password(username):
    try:
        syntax = f"SELECT PASSWORD FROM {USERS_TABLE} WHERE USERNAME = '{username}';"
        cursor, conn = sql()
        cursor.execute(syntax)
        password_fetched = cursor.fetchone()[0]
        conn.close()
        return password_fetched
    except:
        return None


def select_id_from_username(username):
    syntax = f"SELECT ID FROM {USERS_TABLE} WHERE USERNAME = '{username}';"
    cursor, conn = sql()
    cursor.execute(syntax)
    password_fetched = cursor.fetchone()[0]
    conn.close()
    return password_fetched


def select_stocks_for_closing(user_id, stock, portfolio):
    syntax = f"""SELECT ID FROM {OPEN_STOCKS_TABLE} 
                WHERE USER_ID = {user_id}
                AND STOCK = '{stock}' 
                AND PORTFOLIO = '{portfolio}' 
                ORDER BY DATE;"""
    cursor, conn = sql()
    cursor.execute(syntax)
    id_tuples = cursor.fetchall()
    ids = [id_number[0] for id_number in id_tuples]
    conn.close()
    return ids


# CREATE #
def insert_tuple_on_closed_stocks_table(stock):
    try:
        syntax = f"""INSERT INTO {CLOSED_STOCKS_TABLE} (ID, STOCK, DATE, PRICE, SOLD_DATE, SOLD_PRICE, PORTFOLIO, 
                    USER_ID) VALUES ('{stock.id}', '{stock.stock}', '{stock.date}', '{stock.price}', '{stock.sold_date}', 
                    '{stock.sold_price}', '{stock.portfolio}', '{stock.user_id}')"""
        cursor, conn = sql()
        cursor.execute(syntax)
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(e)
        return False


def insert_tuple_on_open_stocks_table(stock):
    try:
        cursor, conn = sql()
        for i in range(stock.quantity):
            syntax = f"""INSERT INTO {OPEN_STOCKS_TABLE} (STOCK, DATE, PRICE, PORTFOLIO, 
                        USER_ID) VALUES ('{stock.stock}', '{stock.date}', '{stock.price}',
                        '{stock.portfolio}', '{stock.user_id}')"""
            cursor.execute(syntax)
        id = cursor.lastrowid
        conn.commit()
        conn.close()
        return True, id
    except Exception as e:
        print(e)
        return False, None


def insert_tuple_on_users_table(user):
    try:
        syntax = f"""INSERT INTO {USERS_TABLE} (NAME, USERNAME, PASSWORD, EMAIL, USER_SINCE) 
                    VALUES ('{user.name}', '{user.username}', '{user.password_hash}', '{user.email}',
                    '{user.user_since}')"""
        cursor, conn = sql()
        cursor.execute(syntax)
        id = cursor.lastrowid
        conn.commit()
        conn.close()
        return True, id
    except Exception as e:
        print(e)
        return False, None


# DELETE #
def delete_tuple_from_table_by_id(id, table):
    try:
        syntax = f"DELETE FROM {table} WHERE ID = {id};"
        cursor, conn = sql()
        cursor.execute(syntax)
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(e)
        return False


# UPDATE #
def update_tuples(table, param, id, value):
    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute(f"""
        UPDATE {table}
        SET {param} = '{value}' WHERE ID = {id};
        """)
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(e)
        return False


if __name__ == '__main__':
    retrieve_all_tuples_from_table(CLOSED_STOCKS_TABLE)


