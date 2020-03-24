import sqlite3
from db import db
from datetime import datetime


class Users_Model(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)

    rut = db.Column(db.String(15), unique=True, nullable=False)
    name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    phone = db.Column(db.Integer())

    password = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)

    creation_date = db.Column(db.DateTime(), default=datetime.now())

    farms = db.relationship('Users_Farms_Model',
                            backref=db.backref('user', lazy=True))

    def __init__(self, rut, name, last_name, password, phone, email):
        self.rut = rut
        self.name = name
        self.last_name = last_name
        self.password = password
        self.phone = phone
        self.email = email

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def json(self):
        return{'name': self.name, 'last_name': self.last_name, 'rut': self.rut, 'email': self.email}

    def all_info(self):
        return{'rut': self.rut, 'email': self.email, 'name': self.name, 'last_name': self.last_name}

    @classmethod
    def get_alls(cls):
        return [user.json() for user in cls.query.all()]

    @classmethod
    def find_by_rut(cls, rut):
        return cls.query.filter_by(rut=rut).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()
