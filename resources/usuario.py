import sqlite3
from flask_restful import Resource, reqparse
from flask import jsonify
from models.usuario import Users_Model
from models.usuarios_predios import Users_Farms_Model
from models.sanitario import Sanitary_Model
from models.predio import Farms_Model
from models.oveja import Sheep_Model
from models.filiacion import Filiations_Model


from resources.usuarios_predio import AddUserFarm

from security import encrypt_password, check_encrypted_password
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    get_jwt_identity,
    jwt_required,
    get_raw_jwt,
    get_current_user, current_user
)


def send_email(correo, rut, name, last_name):
    from flask_mail import Message
    from app import mail

    msg = Message('Se ha creado una cuenta en SmartSheep',
                  sender='smartsheep@guachmail.com',
                  recipients=[correo]
                  )
    msg.body = 'SmartSheep: \n \n Te damos la bienvenida a SmartSheep.cl, la mejor aplicación para gestión de ganadería ovina. \n \n Recuerda que esta cuenta será sólo tuya. Nunca compartas tu clave. \n \n Estos son tus datos para ingresar: \n  \n Email: {} \n Contraseña: {} \n \n Saludos, Equipo ViedmApp.'.format(
        correo, rut[:4])
    mail.send(msg)
    return 'Sent'


class UserRegister(Resource):

    """
    def post(self):
        data = UserRegister.parser.parse_args()

        if Users_Model.find_by_rut(data['rut']):
            return {'msg': "A user with that rut already exists"}, 400
        if data['password'] == None:
            user = Users_Model(data['rut'], data['name'], data['last_name'], encrypt_password(
                "hola"), data['phone'], data['email'])
        else:
            user = Users_Model(data['rut'], data['name'], data['last_name'], encrypt_password(
                data['password']), data['phone'], data['email'])
        user.save_to_db()
        return {

        }, 201
"""

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True,
                            help="This field cannot be left blank")
        parser.add_argument('last_name', type=str, required=True,
                            help="This field cannot be left blank")
        parser.add_argument('phone', type=int, required=False,
                            help="This field cannot be left blank")
        parser.add_argument('rut', type=str, required=True,
                            help="This field cannot be left blank")
        parser.add_argument('email', type=str, required=True,
                            help="This field cannot be left blank")
        parser.add_argument('password', type=str, required=False,
                            help="This field cannot be left blank")
        parser.add_argument("farms_id", type=str, required=True,
                            help="This field cannot be left blank")
        parser.add_argument("can_edit", type=str, required=False,
                            help="This field cannot be left blank")

        data = parser.parse_args()
        user = Users_Model.find_by_rut(data['rut'])
        if user == None:
            password = data['rut'][:4]
            user = Users_Model(data['rut'], data['name'], data['last_name'], encrypt_password(
                password), data['phone'], data['email'])
            user.save_to_db()
            send_email(data['email'], data['rut'],
                       data['name'], data['last_name'])

        user_farm = Users_Farms_Model('1', '1',
                                      '0', user.id, data["farms_id"])
        if user_farm:
            user_farm.save_to_db()
            return user.json(), 201
        return {'error': 'farm created baddly'}, 401

    @jwt_required
    def put(self):

        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True,
                            help="This field cannot be left blank")
        parser.add_argument('last_name', type=str, required=True,
                            help="This field cannot be left blank")
        parser.add_argument('phone', type=str, required=False)
        data = parser.parse_args()
        current_user = get_jwt_identity()
        user = Users_Model.find_by_id(current_user)
        user.name = data['name']
        user.last_name = data['last_name']
        user.phone = data['phone']
        user.save_to_db()


class UserLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email', type=str, required=True,
                        help="This field cannot be left blank")
    parser.add_argument('password', type=str, required=True,
                        help="This field cannot be left blank")

    def post(self):
        data = UserLogin.parser.parse_args()
        user = Users_Model.find_by_email(data['email'])

        if user and check_encrypted_password(data["password"], user.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {"token": access_token, }, 200

        return {"message": "Invalid credentials"}, 401


class UserList(Resource):
    def get(self, _id):
        farm = Farms_Model.query.get(_id)
        query = []
        for userfarms in farm.users:
            peticion = Users_Model.query.get(userfarms.user_id)
            if peticion not in query:
                query.append(peticion)
        return [user.json() for user in query]


class CheckToken(Resource):
    @jwt_required
    def get(self):
        current_user = get_jwt_identity()
        user = Users_Model.find_by_id(current_user)
        return user.all_info()


class CheckPassword(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('password', type=str, required=False,
                        help="This field cannot be left blank")

    @jwt_required
    def post(self):
        data = CheckPassword.parser.parse_args()
        current_user = get_jwt_identity()
        print(current_user)
        user = Users_Model.find_by_id(current_user)
        if user and check_encrypted_password(data["password"], user.password):
            return 1
        else:
            return 0


class ChangePassword(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('password', type=str, required=False,
                        help="This field cannot be left blank")
    parser.add_argument('password2', type=str, required=False,
                        help="This field cannot be left blank")

    @jwt_required
    def put(self):
        data = ChangePassword.parser.parse_args()
        current_user = get_jwt_identity()
        user = Users_Model.find_by_id(current_user)
        if user and check_encrypted_password(data["password"], user.password):
            user.password = encrypt_password(data['password2'])
            user.save_to_db()
            return 200
        return {'La contraseña actual no es correcta', 404}


class AddAdministrator(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True,
                        help="This field cannot be left blank")
    parser.add_argument('last_name', type=str, required=True,
                        help="This field cannot be left blank")
    parser.add_argument('phone', type=int, required=False,
                        help="This field cannot be left blank")
    parser.add_argument('rut', type=str, required=True,
                        help="This field cannot be left blank")
    parser.add_argument('email', type=str, required=True,
                        help="This field cannot be left blank")
    parser.add_argument('password', type=str, required=False,
                        help="This field cannot be left blank")
    parser.add_argument('name_farm', type=str, required=True,
                        help="This field cannot be left blank")
    parser.add_argument('latitude', type=str, required=False,
                        help="This field cannot be left blank")
    parser.add_argument('longitude', type=str, required=False)
    def post(self):

        data = AddAdministrator.parser.parse_args()
        password = data['rut'][:4]
        user = Users_Model(data['rut'], data['name'], data['last_name'], encrypt_password(
            password), data['phone'], data['email'])
        user.save_to_db()
        send_email(data['email'], data['rut'],
                   data['name'], data['last_name'])

        farm = Farms_Model(data['name_farm'],
                           data['latitude'], data['longitude'])
        farm.save_to_db()
        user_farm = Users_Farms_Model("1", "1",
                                      "1", user.id, farm.id)
        user_farm.save_to_db()
        return 201
