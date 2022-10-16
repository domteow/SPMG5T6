from configparser import DuplicateSectionError
from multiprocessing.reduction import duplicate
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import JSON
from learning_journey import Learning_journey
from course import Course
import json

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
    course_id = db.Column(db.String(50), db.ForeignKey(Course.course_id), primary_key=True,
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
    def create_lj_course(journey_id, course_arr):
        # parse course_arr from string to json object
        # print(course_arr)
        course_dict = json.loads(course_arr)
        
        list_of_lj_courses = []
        print('************CHECKING IF CAN GET LJ COURSE OBJECT*************')
        for skill, courses_for_skill in course_dict.items():

            # print(courses_for_skill)
            for course in courses_for_skill:
                course_id = course['course_id']
                
                new_lj_course = Lj_course(journey_id, course_id)
                # print('journey_id = ',journey_id)
                # print(new_lj_course)
                list_of_lj_courses.append(new_lj_course) #adding all the course objs to a list to bulk insert
        print(list_of_lj_courses)
        try:
            db.session.bulk_save_objects(list_of_lj_courses)
            db.session.commit()

        except:
            return jsonify(
                {
                    "code" : 500,
                    "data": {
                        "journey_id" : journey_id,
                        "course_id" : course_id
                    },
                    "message": "dom error"
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

    # User story SA-20
    # add/remove lj courses (dom)
    def edit_lj_course(journey_id, course_arr): 
        # check the courses given in course_arr and
        # remove duplicates
        arr = json.loads(course_arr)
        temp = []
        course_dict = {}
        for k,v in arr.items():
            if v not in temp:
                temp.append(v)
                course_dict[k] = v
        # print('***course_dict***')
        # print(course_dict)
        list_of_lj_courses = []
        
        print('************CHECKING IF CAN GET LJ COURSE OBJECT*************')
        for skill, courses_for_skill in course_dict.items():

            # print(courses_for_skill)
            for course in courses_for_skill:
                # print(course)
                course_id = course['course_id']
                
                new_lj_course = Lj_course(journey_id, course_id)
                # print('journey_id = ',journey_id)
                # print(new_lj_course)
                list_of_lj_courses.append(new_lj_course) #adding all the course objs to a list to bulk insert
        print(list_of_lj_courses)



        # read the lj courses in the database and check
        # what exists and what doesnt
        DB_courses = [course for course in Lj_course.query.filter_by(journey_id=journey_id).all()]
        print('********DATABASE COURSES*************')
        print(type(DB_courses))

        # if the course exists in course_arr but not in DB,
        # add the course to DB

        # if the course exists in DB but not in course_arr,
        # remove the course from DB

        
        