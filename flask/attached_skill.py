from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from skill import Skill


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root' + \
                                        '@localhost:3306/is212'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_size': 100,
                                           'pool_recycle': 280}

db = SQLAlchemy(app)

CORS(app)

class Attached_skill(db.Model):
    __tablename__ = 'attached_skill'

    course_id = db.Column(db.Integer, db.ForeignKey(Course.course_id),
    nullable = False)
    skill_id = db.Column(db.Integer, db.ForeignKey(Skill.skill_id), 
    nullable = False)
    