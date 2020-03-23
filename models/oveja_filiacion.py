import sqlite3
from db import db
from datetime import datetime


class Sheeps_Filiations_Model(db.Model):
    __tablename__ = "sheeps_filiations"
    id = db.Column(db.Integer, primary_key=True)

    sheep_id = db.Column(db.Integer, db.ForeignKey(
        'sheeps.id'), nullable=False)
    filiation_id = db.Column(db.Integer, db.ForeignKey(
        'filiations.id'), nullable=False)

    relationship = db.Column(db.String(15), nullable=False)

    creation_date = db.Column(db.DateTime(), default=datetime.now())

    def __init__(self, relationship):
        self.relationship = relationship

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
