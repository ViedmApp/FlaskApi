import sqlite3
from db import db
from datetime import datetime


class Farms_Model(db.Model):
    __tablename__ = "farms"
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(80))
    latitude = db.Column(db.String(10))
    longitude = db.Column(db.String(10))

    creation_date = db.Column(db.DateTime(), default=datetime.now())

    users = db.relationship('Users_Farms_Model',
                            backref=db.backref('farm', lazy=True))
    sheeps = db.relationship(
        'Sheep_Model', backref=db.backref('farm', lazy=True))

    def __init__(self, name, latitude, longitude):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def json(self):
        return{'id': self.id, 'name': self.name, 'latitude': self.latitude, 'longitude': self.longitude}
