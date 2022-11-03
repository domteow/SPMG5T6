from flask import Flask, request, jsonify
from initdb import db


class Course(db.Model):
    __tablename__ = 'course'

    course_id = db.Column(db.String(20), primary_key=True, nullable=False)
    course_name = db.Column(db.String(50), nullable=False)
    course_desc = db.Column(db.String(255))
    course_status = db.Column(db.String(15))
    course_type = db.Column(db.String(10))
    course_category = db.Column(db.String(50))
    
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

    def get_course_by_id(course_id):
        course = Course.query.filter_by(course_id=course_id).first()
        if course:
            return course.to_dict()
        else:
            return None

    def get_all_courses():
        courses = Course.query.all()
        if courses:
            return [course.to_dict() for course in courses]
        else:
            return []