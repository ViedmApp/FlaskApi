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


class FarmsAdd(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True,
                        help="This field cannot be left blank")
    parser.add_argument('latitude', type=str, required=False,
                        help="This field cannot be left blank")
    parser.add_argument('longitude', type=str, required=False)
    @jwt_required
    def post(self):
        data = FarmsAdd.parser.parse_args()
        farm = Farms_Model(data['name'], data['latitude'], data['longitude'])

        if farm:
            farm.save_to_db()
        current_user = get_jwt_identity()

        user_farm = Users_Farms_Model("1", "1",
                                      "1", current_user, farm.id)
        if user_farm:
            user_farm.save_to_db()
            return farm.json(), 201
        return {'error': 'farm created baddly'}, 401

    def put(self):
        return "farm Actualizado"

    @jwt_required
    def get(self):
        current_user = get_jwt_identity()
        user = Users_Model.query.get(current_user)
        query = []
        for userfarms in user.farms:
            peticion = Farms_Model.query.get(userfarms.farms_id)
            if peticion not in query:
                query.append(peticion)

        return [farm.json() for farm in query]
