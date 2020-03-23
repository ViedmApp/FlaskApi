import sqlite3
from db import db
from datetime import datetime


class Users_Farms_Model(db.Model):
    __tablename__ = "users_farms"
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    farms_id = db.Column(db.Integer, db.ForeignKey('farms.id'), nullable=False)

    can_edit = db.Column(db.String(10), default="F", nullable=False)
    can_see = db.Column(db.String(10), default="T", nullable=False)
    super_user = db.Column(db.String(10), default="F", nullable=False)

    creation_date = db.Column(db.DateTime(), default=datetime.now())

    def __init__(self, can_edit, can_see, super_user, user_id, farms_id):
        self.can_edit = can_edit
        self.can_see = can_see
        self.super_user = super_user
        self.user_id = user_id
        self.farms_id = farms_id

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def json(self):
        return{'can_edit': self.can_edit, 'can_see': self.can_see, 'super_user': self.super_user}

    @classmethod
    def get_alls(cls):
        return [farm.json() for farm in cls.query.all()]
