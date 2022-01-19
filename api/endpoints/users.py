from flask_restful import Resource, reqparse
from api.models.users.users import NewUser, DeleteUser, GetUser, EditUser, AuthUser
from api.database.db_connection import USERS_TABLE
from api.models.crud import retrieve_all_tuples_from_table

### USERS arguments ###
parser = reqparse.RequestParser()
parser.add_argument('id', type=int, default=None)
parser.add_argument('name', type=str, default=None)
parser.add_argument('username', type=str, default=None)
parser.add_argument('email', type=str, default=None)
parser.add_argument('password', type=str, default=None)


class AllUsers(Resource):

    def get(self):
        users_list = retrieve_all_tuples_from_table(USERS_TABLE)
        if users_list:
            users_data_list = []
            for line in users_list:
                user_data = {'Id': line[0], 'Username': line[1], 'Password': line[2], 'Email': line[3], 'User since': line[4]}
                users_data_list.append(user_data)
            if users_data_list:
                return {'Code': 200, 'Alert': 'Success', 'Size': len(users_data_list), 'Data': users_data_list}
            else:
                return {'Code': 400, 'Alert': 'Database is empty.'}
        else:
            return {'Code': 400, 'Alert': 'Database is empty.'}


class User(Resource):

    def __init__(self):
        args = parser.parse_args()
        self.id = args.get('id')
        self.name = args.get('name')
        self.username = args.get('username')
        self.email = args.get('email')
        self.password = args.get('password')

    def get(self):
        user = GetUser(self.id)
        if user.valid and user.crud:
            return {'Code': 200, 'Alert': 'Success', 'Data': user.json_data()}
        else:
            return {'Code': 400, 'Alert': 'Fail', 'Message': user.message}

    def post(self):
        new_user = NewUser(self.name, self.username, self.email, self.password)
        if new_user.valid and new_user.crud:
            return {'Code': 200, 'Alert': 'Success', 'Data': new_user.json_data()}
        else:
            return {'Code': 400, 'Alert': 'Fail', 'Message': new_user.message}

    def delete(self):
        delete_user = DeleteUser(self.id)
        if delete_user.valid and delete_user.crud:
            return {'Code': 200, 'Alert': 'Success', 'Message': delete_user.message}
        else:
            return {'Code': 400, 'Alert': 'Fail', 'Message': delete_user.message}

    def put(self):
        edit_user = EditUser(self)
        if edit_user.valid and edit_user.crud:
            user = GetUser(edit_user.id)
            return {'Code': 200, 'Alert': 'Success', 'Message': edit_user.message, 'Data': user.json_data()}
        else:
            return {'Code': 400, 'Alert': 'Fail', 'Message': edit_user.message}


class AuthentinticateUser(Resource):
    def __init__(self):
        args = parser.parse_args()
        self.username = args.get('username')
        self.password = args.get('password')

    def get(self):
        authenticated_user = AuthUser(self)
        if authenticated_user.valid and authenticated_user.crud:
            return {'Code': 200, 'Alert': 'Success', 'Data': authenticated_user.json_data()}
        else:
            return {'Code': 400, 'Alert': 'Fail', 'Message': authenticated_user.message}
