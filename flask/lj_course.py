from initdb import db
from sqlalchemy import JSON
from learning_journey import Learning_journey
from course import Course
import json
from flask import Flask, request, jsonify


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
        print('************COURSE_ARR*************')
        print(course_arr)
        course_dict = json.loads(course_arr)
        
        list_of_courseid = []
        list_of_lj_courses = []
        print('************CHECKING IF CAN GET LJ COURSE OBJECT*************')
        for skill, courses_for_skill in course_dict.items():

            # print(courses_for_skill)
            for course in courses_for_skill:
                course_id = course['course_id']
                print('*******COURSE ID TO ADD*******')
                print(course_id)

                if course_id not in list_of_courseid:
                    list_of_courseid.append(course_id)
                    new_lj_course = Lj_course(journey_id, course_id)

                    print('journey_id = ',journey_id)
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
                    "message": "Failed to create LJ course"
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
                "message": "Course not found in learning journey."
            }
        )

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

        print('***********course_arr*************')
        print(course_arr)
        course_dict = json.loads(course_arr)
        course_id_add = []
        
        for courses_under_skill in course_dict.values():
            
            for course in courses_under_skill:
                print('***course to be added***')
                print(course)
                if course['course_id'] not in course_id_add:
                    print('***********course*************')
                    print(course['course_id'])
                    course_id_add.append(course['course_id'])
                
        print('***course_dict***')
        print(course_dict)
        
        print('***course_id_add***')
        print(course_id_add)
        
        



        # read the lj courses in the database and check
        # what exists and what doesnt
        DB_courses = [course.course_id for course in Lj_course.query.filter_by(journey_id=journey_id).all()]
        print('********DATABASE COURSES*************')
        print((DB_courses))
        ljc_to_add = []
        ljc_id_to_add = []
        ljc_id_to_remove = []
        # if the course exists in course_arr but not in DB,
        # add the course to DB
        for course_id in course_id_add:
            if course_id not in DB_courses:
                print(course_id)
                new_lj_course = Lj_course(journey_id, course_id)
                ljc_to_add.append(new_lj_course)
                ljc_id_to_add.append(course_id)

        for DB_course_id in DB_courses:
            if DB_course_id not in course_id_add:
                Lj_course.query.filter_by(journey_id=journey_id,course_id=DB_course_id).delete()
                ljc_id_to_remove.append(DB_course_id)
        try:
            db.session.bulk_save_objects(ljc_to_add)
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
        print('********ljc_to_add*************')
        print(ljc_id_to_add)
        print('********ljc_to_remove*************')
        print(ljc_id_to_remove)
        return json.dumps({
            "courses_added" : ljc_id_to_add,
            "courses_removed" : ljc_id_to_remove
        })

    def delete_learning_journey(journey_id):
        to_delete = Lj_course.query.filter_by(journey_id=journey_id).all()

        print(to_delete)
        
        if to_delete:
            
            for course_to_delete in to_delete:
                db.session.delete(course_to_delete)
            db.session.commit()
            return True
        else:
            return "Course not found in learning journey."
        
    

    
        