import sqlite3
from db import db
from datetime import datetime
from models.oveja_filiacion import Sheeps_Filiations_Model


class Sheep_Model(db.Model):
    __tablename__ = "sheeps"
    id = db.Column(db.Integer, primary_key=True)

    farms_id = db.Column(db.Integer, db.ForeignKey('farms.id'), nullable=False)

    earring = db.Column(db.String(50), nullable=False)
    earring_color = db.Column(db.String(20), nullable=False)
    gender = db.Column(db.String(2), nullable=False)
    breed = db.Column(db.String(80), nullable=False)
    birth_weight = db.Column(db.Float, default=0, nullable=False)
    date_birth = db.Column(db.DateTime())
    purpose = db.Column(db.String(50))
    category = db.Column(db.String(20), nullable=False)
    merit = db.Column(db.Integer, default=0, nullable=False)
    is_dead = db.Column(db.String(2), default=False, nullable=False)

    creation_date = db.Column(db.DateTime(), default=datetime.now())

    sickness = db.relationship('Sanitary_Model', backref='sheep')
    relations = db.relationship('Sheeps_Filiations_Model', backref='sheep')

    def __init__(self, earring, earring_color, gender, breed, birth_weight, date_birth, purpose, category, merit, is_dead, farms_id):
        self.earring = earring
        self.earring_color = earring_color
        self.gender = gender
        self.breed = breed
        self.birth_weight = birth_weight
        self.date_birth = date_birth
        self.purpose = purpose
        self.category = category
        self.merit = merit
        self.is_dead = is_dead
        self.farms_id = farms_id

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def json(self):
        return {'_id': self.id, 'earring': self.earring, 'earring_color': self.earring_color, 'gender': self.gender, 'breed': self.breed,
                'birth_weight': self.birth_weight, 'date_birth': self.date_birth, 'purpose': self.purpose, 'category': self.category, 'merit': self.merit,
                'is_dead': self.is_dead}

    @classmethod
    def get_all(cls):
        return[sheep.json() for sheep in cls.query.all()]
