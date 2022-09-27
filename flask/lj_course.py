from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from learning_journey import Learning_journey
from course import Course

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

class Lj_course(db.Model):
    __tablename__ = 'lj_course'

    journey_id = db.Column(db.Integer, db.ForeignKey('Learning_journey.journey_id'), primary_key=True,
    nullable = False)
    course_id = db.Column(db.Integer, db.ForeignKey('Course.course_id'), primary_key=True,
    nullable = False)

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