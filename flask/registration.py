from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from course import Course
from staff import Staff

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

class Registration(db.Model):
    __tablename__ = 'registration'

    reg_id = db.Column(db.Integer, primary_key=True, nullable=False)
    course_id = db.Column(db.String(20), db.ForeignKey(Course.course_id), nullable=False)
    staff_id = db.Column(db.Integer, db.ForeignKey(Staff.staff_id), nullable=False)
    reg_status = db.Column(db.String(20), nullable=False)
    completion_status = db.Column(db.String(20), nullable=False)

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

    def get_completed_courses_by_staff_id(staff_id):
        courses = Registration.query.filter_by(staff_id=staff_id).all()
        completed_courses = []
        if len(courses):
            for course in courses:
                course = course.to_dict()
                if course["completion_status"] == "Completed":
                    completed_courses.append(course["course_id"])
        return completed_courses

    def get_ongoing_courses_by_staff_id(staff_id):
        courses = Registration.query.filter_by(staff_id=staff_id).all()
        ongoing_courses = []
        if len(courses):
            for course in courses:
                course = course.to_dict()
                if course["completion_status"] == "OnGoing":
                    ongoing_courses.append(course["course_id"])
        return ongoing_courses