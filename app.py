from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from flask_mail import Mail, Message
import os

from security import authenticate, identity
from resources.usuario import UserRegister, UserLogin, UserList, CheckToken
from resources.oveja import SheepAdd, SheepList, SheepDelete, SheepUpdate
from resources.predio import FarmsAdd
from resources.usuarios_predio import AddUserFarm

from flask_jwt_extended import JWTManager
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLACHEMY_TRACK_MODIFICATION'] = False
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'smartsheepuach@gmail.com'
app.config['MAIL_PASSWORD'] = 'smartsheepcl'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
api = Api(app)
mail = Mail(app)


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
api.add_resource(SheepUpdate, '/updatesheep/<int:_id>')


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(debug=True)
