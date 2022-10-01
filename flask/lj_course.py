from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from learning_journey import Learning_journey
from course import Course

app = Flask(__name__)
import platform
my_os = platform.system()
if my_os == "Windows":
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root' + '@localhost:3306/all_in_one_db'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root' + '@localhost:3306/all_in_one_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_size': 100,
                                           'pool_recycle': 280}

db = SQLAlchemy(app)

CORS(app)

class Lj_course(db.Model):
    __tablename__ = 'lj_course'

    journey_id = db.Column(db.Integer, db.ForeignKey(Learning_journey.journey_id), primary_key=True,
    nullable = False)
    course_id = db.Column(db.Integer, db.ForeignKey(Course.course_id), primary_key=True,
    nullable = False)

    def __init__(self, journey_id, course_id):
        self.journey_id = journey_id
        self.course_id = course_id

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

    def get_lj_course_by_journey(journey_id):
        lj_course = Lj_course.query.filter_by(journey_id=journey_id).all()
        if len(lj_course):
            return [ljc.to_dict() for ljc in lj_course]
        else:
            return []

    #create lj courses (dom)
    def create_lj_course(journey_id, course_id):
        new_lj_course = Lj_course(journey_id, course_id)

        try:
            db.session.add(new_lj_course)
            db.session.commit()

        except:
            return jsonify(
                {
                    "code" : 500,
                    "data": {
                        "journey_id" : journey_id,
                        "course_id" : course_id
                    },
                    "message": "An error occurred creating a LJ"
                }
            )

        return jsonify(
        {
            "code": 201,
            "data": new_lj_course.to_dict()
        })
    
    def delete_lj_course(journey_id, course_id):
        to_delete = Lj_course.query.filter_by(journey_id=journey_id,course_id=course_id).first()
        if to_delete:
            db.session.delete(to_delete)
            db.session.commit()
            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "lj_course": to_delete.to_dict()
                    }
                }
            )
        return jsonify(
            {
                "code": 404,
                "data": {
                    "lj_course": to_delete.to_dict()
                },
                "message": "Course not found in learning journey."
            }
        ), 404

    def get_lj_course_by_journey_list(journey_id):
        lj_course = Lj_course.query.filter_by(journey_id=journey_id).all()
        courses = []

        if len(lj_course):
          for course in lj_course: 
            if course.course_id not in courses:
                courses.append(course.course_id)
    	
        return courses 
