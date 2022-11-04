import unittest
import flask_testing
import json
from sqlalchemy import JSON
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
        self.ljc3 = Lj_course(journey_id=1, course_id="COR004")
        self.ljc4 = Lj_course(journey_id=1, course_id="COR006")
        to_add = [self.ljc1,self.ljc2,self.ljc3,self.ljc4]
        db.session.bulk_save_objects(to_add)
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
        ,["COR001","COR004","COR006","FIN001"])

    def test_create_lj_course(self):
        
        result = Lj_course.create_lj_course(journey_id=2, course_arr='{"Problem Solving ":[{"course_id":"COR001","course_name":"Systems Thinking and Design"},{"course_id":"FIN001","course_name":"Data Collection and Analysis"}],"Critical Thinking":[{"course_id":"COR001","course_name":"Systems Thinking and Design"},{"course_id":"FIN001","course_name":"Data Collection and Analysis"}]}')
        result = result.json
        self.assertEqual(result['code'], 201)

    def test_fail_create_lj_course(self):
        result = Lj_course.create_lj_course(journey_id=1, course_arr='{"Problem Solving ":[{"course_id":"COR001","course_name":"Systems Thinking and Design"},{"course_id":"FIN001","course_name":"Data Collection and Analysis"}],"Critical Thinking":[{"course_id":"COR001","course_name":"Systems Thinking and Design"},{"course_id":"FIN001","course_name":"Data Collection and Analysis"}]}')
        result = result.json
        self.assertEqual(result['code'], 500)
        self.assertEqual(result['message'],"Failed to create LJ course")

    def test_delete_lj_course(self):

        result = Lj_course.delete_lj_course(journey_id=1, course_id="FIN001")

        result = result.json
        self.assertEqual(result['code'], 200)

    def test_fail_delete_lj_course(self):

        result = Lj_course.delete_lj_course(journey_id=2, course_id="FIN001")

        result = result.json
        self.assertEqual(result['code'], 404)
        self.assertEqual(result['message'],"Course not found in learning journey.")


    def test_edit_lj_course(self):
        
        result = json.loads(Lj_course.edit_lj_course(journey_id=1, course_arr='{"Helpdesk Basics":[{"course_id":"tch003","course_name":"Canon MFC Mainteance and Troubleshooting"}],"Problem Solving ":[{"course_id":"COR001","course_name":"Systems Thinking and Design"}],"Critical Thinking":[{"course_id":"COR001","course_name":"Systems Thinking and Design"}]}'))

        self.assertEqual(result['courses_added'],['tch003'])
        self.assertEqual(result['courses_removed'],['COR004','COR006','FIN001'])
    
    def test_delete_learning_journey(self):
        self.assertEqual(Lj_course.delete_learning_journey(1)
        ,True)  

    def test_error_delete_learning_journey(self):
        # Should not be able to delete LJ that does not exist
        self.assertEqual(Lj_course.delete_learning_journey(3)
        ,"Course not found in learning journey.")
if __name__ == "__main__":
    unittest.main()  