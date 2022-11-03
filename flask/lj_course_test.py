import unittest
import flask_testing
import json
from initdb import db
from app import app
from lj_course import Lj_course
from flask import jsonify

class TestLearning_journey(flask_testing.TestCase):
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {}
    app.config['TESTING'] = True
    def create_app(self):
        return app

    def setUp(self):
        db.create_all()
        self.ljc1 = Lj_course(journey_id=1, course_id="COR001")
        self.ljc2 = Lj_course(journey_id=1, course_id="FIN001")
        db.session.add(self.ljc1)
        db.session.add(self.ljc2)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()   

    def test_to_dict(self):

        self.assertEqual(self.ljc1.to_dict(), {
            "journey_id" : 1,
            "course_id" : "COR001",
        })

    def test_get_lj_course_by_journey(self):
        self.assertEqual(Lj_course.get_lj_course_by_journey_list(journey_id=1)
        ,["COR001","FIN001"])

    def test_create_lj_course(self):
        
        result = Lj_course.create_lj_course(journey_id=1, course_arr='{"Problem Solving ":[{"course_id":"COR001","course_name":"Systems Thinking and Design"},{"course_id":"FIN001","course_name":"Data Collection and Analysis"}],"Critical Thinking":[{"course_id":"COR001","course_name":"Systems Thinking and Design"},{"course_id":"FIN001","course_name":"Data Collection and Analysis"}]}')

        self.assertEqual(result.status,'200 OK')


    def test_delete_lj_course(self):

        result = Lj_course.delete_lj_course(journey_id=1, course_id="FIN001")

        self.assertEqual(result.status, '200 OK')
    