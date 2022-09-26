from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

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

class Ljps_role(db.Model):
    __tablename__ = 'ljps_role'

    ljpsr_id = db.Column(db.Integer, primary_key=True)
    role_title = db.Column(db.String(50), nullable = False)
    role_desc = db.Column(db.String(255))

    def __init__(self, ljpsr_id, role_title, role_desc):
        self.ljpsr_id = ljpsr_id
        self.role_title = role_title
        self.role_desc = role_desc