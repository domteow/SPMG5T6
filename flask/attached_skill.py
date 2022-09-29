from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from skill import Skill
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

class Attached_skill(db.Model):
    __tablename__ = 'attached_skill'

    course_id = db.Column(db.String(20), db.ForeignKey('Course.course_id'), primary_key=True,
    nullable = False)
    skill_id = db.Column(db.Integer, db.ForeignKey('Skill.skill_id'), primary_key=True,
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

    def get_attached_course_by_skill_id(skill_id):
        attached_skill = Attached_skill.query.filter_by(skill_id=skill_id).all()
        if len(attached_skill):
            return [atts.to_dict() for atts in attached_skill]
        else:
            return []

    # For list of course IDs
    def get_attached_course_by_skill_id_list(skill_id):
        courses = []
        attached_course = Attached_skill.query.filter_by(skill_id=skill_id).all()

        if len(attached_course):
            for course in attached_course:
                if course.course_id not in courses:
                    courses.append(course.course_id)

        return courses 
    
    # FOR ONE COURSE
    def get_attached_skill_by_course_id(course_id):
        attached_skill = Attached_skill.query.filter_by(course_id=course_id).all()

        if len(attached_skill):
            return [atts.to_dict() for atts in attached_skill]
        else:
            return []


    # pls help me check if correct ... 

    # FOR MANY COURSES
    # parses in list of course_ids and try to find the attached skill for each course  
    def get_attached_skill_by_course_ids(course_ids):
        attached_skill = []
        # loop through each course 
        for course_id in course_ids: 
            # this assumes that one course have > 1 skill 
            get_skill = Attached_skill.query.filter_by(course_id=course_id).all()
            # creates a key using course_id

            # appends each skill to the course 
            for skill in get_skill: 
                if skill.skill_id not in attached_skill:
                    attached_skill.append(skill.skill_id)
                    
        return attached_skill



