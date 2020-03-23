import sqlite3
from db import db
from datetime import datetime


class Filiations_Model(db.Model):
    __tablename__ = "filiations"
    id = db.Column(db.Integer, primary_key=True)

    type_recess = db.Column(db.String(80))
    date_recess = db.Column(db.DateTime())

    creation_date = db.Column(db.DateTime(), default=datetime.now())

    related_sheeps = db.relationship(
        'Sheeps_Filiations_Model', backref='relationty')

    def __init__(self, type_recess, date_recess):
        self.type_recess = type_recess
        self.date_recess = date_recess

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
