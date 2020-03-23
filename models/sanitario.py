import sqlite3
from db import db
from datetime import datetime


class Sanitary_Model(db.Model):
    __tablename__ = "sanitary"
    id = db.Column(db.Integer, primary_key=True)

    sheep_id = db.Column(db.Integer, db.ForeignKey(
        'sheeps.id'), nullable=False)

    sickness = db.Column(db.Text, nullable=False)
    treatment = db.Column(db.Text, nullable=False)

    creation_date = db.Column(db.DateTime(), default=datetime.now())

    def __init__(self, sickness, treatment):
        self.sickness = sickness
        self.treatment = treatment

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
