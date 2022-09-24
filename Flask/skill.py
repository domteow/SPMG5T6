from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root' + \
                                        '@localhost:3306/is212'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_size': 100,
                                           'pool_recycle': 280}

db = SQLAlchemy(app)

CORS(app)

class Skill(db.Model):
    __tablename__ = 'skill'

    skill_id = db.Column(db.Integer, primary_key=True, nullable=False)
    skill_name = db.Column(db.String(50))
    skill_desc = db.Column(db.String(255))

    def __init__(self, skill_id, skill_name, skill_desc):
        self.skill_id = skill_id
        self.skill_name = skill_name
        self.skill_desc = skill_desc
        

