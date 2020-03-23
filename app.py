from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
import os

from security import authenticate, identity
from resources.usuario import UserRegister, UserLogin, UserList, CheckToken
from resources.oveja import SheepAdd, SheepList, SheepDelete
from resources.predio import FarmsAdd
from resources.usuarios_predio import AddUserFarm

from flask_jwt_extended import JWTManager
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLACHEMY_TRACK_MODIFICATION'] = False
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
api = Api(app)

jwt = JWTManager(app)


api.add_resource(UserList, '/users/<int:_id>')
api.add_resource(SheepDelete, '/sheep/<int:_id>')
api.add_resource(CheckToken, '/au')
api.add_resource(UserLogin, '/login')
api.add_resource(UserRegister, '/register')
api.add_resource(SheepAdd, '/sheep')
api.add_resource(SheepList, '/sheep/<int:_id>')
api.add_resource(FarmsAdd, '/predio')
api.add_resource(AddUserFarm, '/userpredio')


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(debug=True)
