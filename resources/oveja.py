import sqlite3
from flask_restful import Resource, reqparse
from models.oveja import Sheep_Model
from models.predio import Farms_Model
from security import encrypt_password
from flask_jwt import jwt_required
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
)


class SheepAdd(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('earring', type=str, required=True,
                        help="This field cannot be left blank")
    parser.add_argument('earring_color', type=str, required=True,
                        help="This field cannot be left blank")
    parser.add_argument('gender', type=str, required=True,
                        help="This field cannot be left blank")
    parser.add_argument('breed', type=str, required=True,
                        help="This field cannot be left blank")
    parser.add_argument('birth_weight', type=str, required=True,
                        help="This field cannot be left blank")
    parser.add_argument('date_birth', type=str, required=False,
                        help="This field cannot be left blank")
    parser.add_argument('purpose', type=str, required=False,
                        help="This field cannot be left blank")
    parser.add_argument('category', type=str, required=False,
                        help="This field cannot be left blank")
    parser.add_argument('merit', type=str, required=True,
                        help="This field cannot be left blank")
    parser.add_argument('is_dead', type=str, required=True,
                        help="This field cannot be left blank")
    parser.add_argument('farms_id', type=str, required=True,
                        help="This field cannot be left blank")

    @jwt_required
    def post(self):
        current_id = get_jwt_identity()
        data = SheepAdd.parser.parse_args()
        sheep = Sheep_Model(
            data['earring'], data['earring_color'], data['gender'], data['breed'], data['birth_weight'],
            data['date_birth'], data['purpose'], data['category'], data['merit'], data['is_dead'], data['farms_id'])
        if sheep:
            sheep.save_to_db()
            return sheep.json(), 201
        return {'error': 'sheep created baddly'}, 401

    def put(self):
        return "Oveja Actualizado"


class SheepDelete(Resource):
    @jwt_required
    def delete(self, _id):
        print(_id)
        sheep = Sheeps_Model.find_by_id(_id)
        if sheep:
            sheep.delete_from_db()
        return {'message': 'Sheep deleted'}


class SheepList(Resource):

    def get(self, _id):
        farm = Farms_Model.query.get(_id)
        return [sheep.json() for sheep in farm.sheeps]
