import unittest
import flask_testing
import json
from initdb import db
from app import app
from attached_skill import Attached_skill

class Test_Attached_Skill(flask_testing.TestCase):
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {}
    app.config['TESTING'] = True

    def create_app(self):
        return app

    def setUp(self): 
        db.create_all()

        self.as1 = Attached_skill(skill_id=1, course_id='COR001')
        self.as2 = Attached_skill(skill_id=1, course_id='COR004')
        self.as3 = Attached_skill(skill_id=1, course_id='COR006')
        self.as4 = Attached_skill(skill_id=1, course_id='FIN001')
        self.as4 = Attached_skill(skill_id=2, course_id='COR001')
        self.as5 = Attached_skill(skill_id=2, course_id='FIN001')
        self.as6 = Attached_skill(skill_id=2, course_id='tch006')

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_to_dict(self):
        self.assertEqual(self.as1.to_dict(), {
            "skill_id" : 1,
            "course_id" : 'COR001'
        })    

    def test_get_attached_course_by_skill_id(self):
        self.assertEqual(Attached_skill.get_attached_course_by_skill_id(skill_id=1), [
            {
                'skill_id': 1, 
                'course_id': 'COR001'
            }, 
            {
                'skill_id': 1, 
                'course_id': 'COR004'
            }, 
            {
                'skill_id': 1, 
                'course_id': 'COR006'
            }, 
            {
                'skill_id': 1, 
                'course_id': 'FIN001'
            }
        ])

    def test_get_attached_course_by_skill_id_list(self):
        self.assertEqual(Attached_skill.get_attached_course_by_skill_id_list(skill_id=1), 
        ['COR001', 'COR004', 'COR006', 'FIN001'])

    def test_get_attached_skill_by_course_id(self):
        self.assertEqual(Attached_skill.get_attached_skill_by_course_id(course_id='COR001'), {
            'skill_id': 1, 
            'course_id': 'COR001'
        })

    def test_get_attached_skill_by_course_ids(self):
        self.assertEqual(Attached_skill.get_attached_skill_by_course_ids(course_ids=['COR001', 'FIN001']), 
        [1, 2])

    def test_create_attached_skill(self):
        self.assertEqual(Attached_skill.create_attached_skill(course_id='tch007', skill_id=2), True)

    def test_add_courses_to_skill(self): 
        self.assertEqual(Attached_skill.add_courses_to_skill(skill_id=1, courses=['COR007', 'COR008', 'COR009']), {
            "code": 201,
            "data": {
                "skill_id" : 1,
                "courses" : ['COR007', 'COR008', 'COR009']
            },
            "message": "Courses added successfully"
        })

    def test_remove_course_from_skill(self):
        self.assertEqual(Attached_skill.remove_course_from_skill(skill_id=2, courses=['COR001', 'FIN001', 'tch006']), {
            "code": 201, 
            "data": {
                "skill_id": 2, 
                "courses": ['COR001', 'FIN001', 'tch006']
            }, 
            "message": "Courses removed successfully"
        })

    def test_get_num_attached_skill_by_course_id_list(self):
        self.assertEqual(Attached_skill.get_num_attached_skill_by_course_id_list(course_id_list=['COR001']), 2)


        