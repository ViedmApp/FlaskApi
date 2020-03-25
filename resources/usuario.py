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
    msg.body = 'Hola {} {} Se creo con éxito una cuenta en SmartSheep su contraseña por defecto es : {}'.format(
        name, last_name, rut[:4])
    mail.send(msg)
    return 'Sent'


class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True,
                        help="This field cannot be left blank")
    parser.add_argument('last_name', type=str, required=True,
                        help="This field cannot be left blank")
    parser.add_argument('rut', type=str, required=True,
                        help="This field cannot be left blank")
    parser.add_argument('email', type=str, required=True,
                        help="This field cannot be left blank")
    parser.add_argument('password', type=str, required=False,
                        help="This field cannot be left blank")
    parser.add_argument('phone', type=int, required=False,
                        help="This field cannot be left blank")
    parser.add_argument("farms_id", type=str, required=True,
                        help="This field cannot be left blank")
    parser.add_argument("can_edit", type=str, required=True,
                        help="This field cannot be left blank")
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
        data = UserRegister.parser.parse_args()
        user = Users_Model.find_by_rut(data['rut'])
        if user == None:
            password = data['rut'][:4]
            user = Users_Model(data['rut'], data['name'], data['last_name'], encrypt_password(
                password), data['phone'], data['email'])
            user.save_to_db()
            send_email(data['email'], data['rut'],
                       data['name'], data['last_name'])

        user_farm = Users_Farms_Model(data['can_edit'], "T",
                                      "F", user.id, data["farms_id"])
        if user_farm:
            user_farm.save_to_db()
            return user.json(), 201
        return {'error': 'farm created baddly'}, 401


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
