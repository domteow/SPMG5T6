from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from ljps_role import Ljps_role
from staff import Staff

app = Flask(__name__)
#MAC OS
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root' + '@localhost:3306/all_in_one_db'
#Windows OS
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root' + '@localhost:3306/all_in_one_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_size': 100,
                                           'pool_recycle': 280}

db = SQLAlchemy(app)

CORS(app)

class Learning_journey(db.Model):
    __tablename__ = 'learning_journey'

    journey_id = db.Column(db.Integer, primary_key=True, nullable=False)
    ljpsr_id = db.Column(db.Integer, db.ForeignKey(Ljps_role.ljpsr_id), nullable=False)
    staff_id = db.Column(db.Integer, db.ForeignKey(Staff.staff_id), nullable=False)
    status = db.Column(db.Integer, nullable=False)

    def __init__(self, journey_id, role_id, staff_id, status):
        self.journey_id = journey_id
        self.role_id = role_id
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
