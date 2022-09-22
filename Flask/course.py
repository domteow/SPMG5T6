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

class Courses(db.Model):
    __tablename__ = 'course'

    course_id = db.Column(db.String(20), primary_key=True, nullable=False)
    course_name = db.Column(db.String(50), nullable=False)
    course_desc = db.Column(db.String(255))
    course_status = db.Column(db.String(15))
    course_type = db.Column(db.String(10))
    course_category = db.Column(db.String(50))
