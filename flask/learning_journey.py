from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from LJPS_role import Ljps_role
from staff import Staff

app = Flask(__name__)
#MAC OS
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root' + '@localhost:3306/all_in_one_db'
#Windows OS
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root' + '@localhost:3306/all_in_one_db'
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
