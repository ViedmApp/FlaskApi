import sqlite3
from flask_restful import Resource, reqparse
from models.oveja import Sheep_Model
from models.usuario import Users_Model
from models.predio import Farms_Model
from models.usuarios_predios import Users_Farms_Model

from security import encrypt_password
from flask_jwt import jwt_required
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
)


class AddUserFarm(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('can_edit', type=str, required=True,
                        help="This field cannot be left blank")
    parser.add_argument('can_see', type=str, required=False,
                        help="This field cannot be left blank")
    parser.add_argument('super_user', type=str, required=False)
    parser.add_argument('user_id', type=str, required=True,
                        help="This field cannot be left blank")
    parser.add_argument('farms_id', type=str, required=True,
                        help="This field cannot be left blank")

    @jwt_required
    def post(self):
        data = AddUserFarm.parser.parse_args()

        user_ = Users_Model.query.get(data['user_id'])
        farm_ = Farms_Model.query.get(data['farms_id'])

        user_farm = Users_Farms_Model(data['can_edit'], data['can_see'],
                                      data['super_user'], data['user_id'], data["farms_id"])
        if user_farm:
            user_farm.save_to_db()
            return user_farm.json(), 201
        return {'error': 'farm created baddly'}, 401

    @jwt_required
    def get(self):
        current_user = get_jwt_identity()
        user = Users_Model.query.get(current_user)
        print(user.farms)
        return [userfarm.json() for userfarm in user.farms]
