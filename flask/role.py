from initdb import db
from flask import Flask, request, jsonify

class Role(db.Model):
    __tablename__ = 'role'

    role_id = db.Column(db.Integer, primary_key=True, nullable=False)
    role_name = db.Column(db.String(20), nullable=False)

    def to_dict(self):
        """
        'to_dict' converts the object into a dictionary,
        in which the keys correspond to database columns
        """
        columns = self.__mapper__.column_attrs.keys()
        result = {}
        for column in columns:
            result[column] = getattr(self, column)
        return result

    def get_role_by_id(role_id):
        role = Role.query.filter_by(role_id=role_id).first()
        if role:
            return role.to_dict()
        else:
            return None