from initdb import db
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from ljps_role import Ljps_role
from staff import Staff
from flask import Flask, request, jsonify


class Learning_journey(db.Model):
    __tablename__ = 'learning_journey'

    journey_id = db.Column(db.Integer, primary_key=True, nullable=False)
    ljpsr_id = db.Column(db.Integer, db.ForeignKey(Ljps_role.ljpsr_id), nullable=False)
    staff_id = db.Column(db.Integer, db.ForeignKey(Staff.staff_id), nullable=False)
    status = db.Column(db.Integer, nullable=False)

    def __init__(self, journey_id, ljpsr_id, staff_id, status):
        self.journey_id = journey_id
        self.ljpsr_id = ljpsr_id
        self.staff_id = staff_id
        self.status = status

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
    
    def get_learning_journey_by_staff_id(staff_id):
        learning_journey = Learning_journey.query.filter_by(staff_id=staff_id).all()
        if len(learning_journey):
            return [lj.to_dict() for lj in learning_journey]
        else:
            return []

    def get_learning_journey_role_by_id(journey_id):
        learning_journey = Learning_journey.query.filter_by(journey_id=journey_id).first()

        if len(learning_journey):
            return learning_journey.ljpsr_id

        else: 
            return "Error: No role"

    # creating LJ in learning_journey table (dom)
    def create_learning_journey(journey_id, ljpsr_id,staff_id):
        # journey_id = db.session.query(Learning_journey.journey_id).count() + 1
        new_journey = Learning_journey(journey_id, ljpsr_id,staff_id,0)

        try:
            db.session.add(new_journey)
            db.session.commit()

        except:
            return "Failed to create LJ"

        return True
    

    # deleting LJ in learning_journey table (dom)
    def delete_learning_journey(journey_id):
        to_delete = Learning_journey.query.filter_by(journey_id=journey_id).first()

        if to_delete:
            db.session.delete(to_delete)
            db.session.commit()
            return True
        else:
            return "Failed to delete LJ"
