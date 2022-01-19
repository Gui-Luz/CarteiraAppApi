import os
import configparser
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime
import api
from api.models.crud import check_id_exists_in_table, insert_tuple_on_users_table, retrieve_tuple_from_id, \
    delete_tuple_from_table_by_id, update_tuples, select_username_password, select_id_from_username
from api.database.db_connection import USERS_TABLE


config_file = configparser.ConfigParser()
config_file.read(os.path.dirname(api.__file__) + '/config.ini')
JWT_SALT = str(config_file['JWT']['salt'])


class User:
    def __init__(self, name=None, id=None, username=None, email=None):

        self.id = id
        self.name = name
        self.username = username
        self.email = email
        self.password_hash = None
        self.user_since = None

    def __repr__(self):
        return f'Username: {self.username}'

    def _validate_id(self):
        if self.id and type(self.id == int):
            if check_id_exists_in_table(self.id, USERS_TABLE):
                return True
            else:
                self._set_message('Id not found.')
                return False
        else:
            self._set_message('Invalid id.')
            return False

    def _validate_name(self):
        if (type(self.name) == str) and (len(self.name) <= 50):
            return True
        else:
            return False

    def _validate_username(self):
        if (type(self.username) == str) and (len(self.username) <= 30):
            return True
        else:
            return False

    def _validate_password(self):
        if self.password_hash and (type(self.password_hash) == str):
            return True
        else:
            self._set_message('Invalid password.')
            return False

    def _validate_email(self):
        if (type(self.email) == str) and (len(self.email) <= 50):
            return True
        else:
            self._set_message('Invalid email.')
            pass

    def _set_message(self, message):
        self.message = message

    def json_data(self):
        return {'Id': self.id, 'Username': self.username, 'Email': self.email, 'Password': self.password_hash,
                'User since': self.user_since}

    def _set_id(self, id):
        self.id = id

    @staticmethod
    def _set_password_hash(password):
        if password:
            return generate_password_hash(password)
        else:
            return None


class GetUser(User):

    def __init__(self, user_id):

        super().__init__()
        self.id = user_id
        self.valid = self._valid()
        self.crud = self._crud()

    def _valid(self):
        if self._validate_id():
            return True
        else:
            return False

    def _crud(self):
        if self.valid:
            user_data = retrieve_tuple_from_id(self.id, USERS_TABLE)
            if user_data:
                self.username = user_data[1]
                self.password_hash = user_data[2]
                self.email = user_data[3]
                self.user_since = user_data[4]
                self._set_message('User found.')
                return True
            else:
                self._set_message('User not found.')
                return False
        else:
            return False


class NewUser(User):

    def __init__(self, name, username, email, password):

        super().__init__()
        self.id = None
        self.name = name
        self.username = username
        self.password_hash = self._set_password_hash(password)
        self.email = email
        self.user_since = str(datetime.now())
        self.message = None
        self.valid = self._valid()
        self.crud = self._crud()

    def _valid(self):
        if self._validate_username() and self._validate_email() and self._validate_password() and self._validate_name():
            return True
        else:
            return False

    def _crud(self):
        if self.valid:
            insert_user, id = insert_tuple_on_users_table(self)
            self._set_id(id)
            if insert_user:
                self._set_message('User created.')
                return True
            else:
                self._set_message('Error inserting user in database.')
                return False


class DeleteUser(User):

    def __init__(self, user_id):

        super().__init__()
        self.id = user_id
        self.valid = self._valid()
        self.crud = self._crud()

    def _valid(self):
        if self._validate_id():
            return True
        else:
            return False

    def _crud(self):
        if self.valid:
            if delete_tuple_from_table_by_id(self.id, USERS_TABLE):
                self._set_message('User deleted.')
                return True
            else:
                self._set_message('Error deleting user from database.')
                return False
        else:
            return False


class EditUser(User):
    def __init__(self, args):

        super().__init__()
        self.id = args.id
        self.username = args.username
        self.email = args.email
        self.password = args.password
        self.valid = self._valid()
        self.crud = self._crud()

    def _valid(self):
        if self._validate_id():
            return True
        else:
            return False

    def _crud(self):
        if self.valid:
            crud_results = []
            if self.username or self.email or self.password:
                if self.username and self._validate_username():
                    updated_user = update_tuples(USERS_TABLE, 'USERNAME', self.id, self.username)
                    if updated_user:
                        crud_results.append(True)
                    else:
                        crud_results.append(False)
                if self.email and self._validate_email():
                    updated_user = update_tuples(USERS_TABLE, 'EMAIL', self.id, self.email)
                    if updated_user:
                        crud_results.append(True)
                    else:
                        crud_results.append(False)
                if self.password:
                    self.password_hash = self._set_password_hash(self.password)
                    if self._validate_password():
                        updated_user = update_tuples(USERS_TABLE, 'PASSWORD', self.id, self.password_hash)
                        if updated_user:
                            crud_results.append(True)
                        else:
                            crud_results.append(False)
                    else:
                        crud_results.append(False)
                if all(i for i in crud_results):
                    self._set_message('User updated.')
                    return True
                else:
                    self._set_message('Fail')
                    return False
            else:
                self._set_message('No update parameters provided')
                return False
        else:
            return False


class AuthUser(User):

    def __init__(self, args):
        super().__init__()
        self.username = args.username
        self.password = args.password
        self.password_hash = self._set_password_hash(self.password)
        self.valid = self._valid()
        self.crud = self._crud()

    def _valid(self):
        if self._validate_username():
            return True
        else:
            return False

    def _crud(self):
        if self.valid:
            user_password = select_username_password(self.username)
            if user_password and check_password_hash(user_password, self.password):
                self._set_id(select_id_from_username(self.username))
                enconded_jwt = jwt.encode({'id': self.id, 'username': self.username}, JWT_SALT, algorithm='HS256')
                self._set_jwt(enconded_jwt)
                self._set_name_email()
                return True
            else:
                self._set_message('Usuário e senha não conferem.')
                return None
        else:
            self._set_message('Usuário e senha não conferem.')
            return None

    def _set_jwt(self, encoded_jwt):
        self.jwt = encoded_jwt

    def _set_name_email(self):
        id, name, username, password, email, user_since = retrieve_tuple_from_id(self.id, USERS_TABLE)
        self.name = name
        self.email = email
        self.user_since = user_since

    def json_data(self):
        return {'Id': self.id, 'Name':self.name, 'Email': self.email, 'Username': self.username,
                'User since':self.user_since, 'Jwt': self.jwt}
