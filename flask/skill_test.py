import unittest
import flask_testing
import json
from skill import Skill
from initdb import db
from app import app


class TestCourse (flask_testing.TestCase):
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {}
    app.config['TESTING'] = True

    def create_app(self):
        return app 

    def setup(self):
        db.create_all()
        self.s1 = Skill(skill_id=200, skill_name= 'Python Programming', skill_desc='Python is often used as a support language for software developers, for build control and management, testing, and in many other ways', active=1)
        self.s2 = Skill(skill_id=201, skill_name='Emotional Intelligence', skill_desc='Emotional intelligence is the ability to recognize, manage, and understand emotions.', active=1)
        self.s3 = Skill(skill_id=202, skill_name='Web Development', skill_desc='Web development, also known as website development, refers to the tasks associated with creating, building, and maintaining websites and web applications that run online on a browser.', active=0)

        db.session.add(self.s1)
        db.session.add(self.s2)
        db.session.add(self.s3)
        db.session.commit()

    def tearDown(self): 
        db.session.remove()
        db.drop_all()

    def test_to_dict(self): 
        self.assertEqual(self.c1.to_dict(), {
            "skill_id": 200, 
            "skill_name": 'Python Programming', 
            "skill_desc": 'Python is often used as a support language for software developers, for build control and management, testing, and in many other ways',
            "active": 1
        })

    def test_get_skill_by_id(self): 
        self.assertEqual(Skill.get_skill_by_id(200), {
            "skill_id": 200, 
            "skill_name": 'Python Programming', 
            "skill_desc": 'Python is often used as a support language for software developers, for build control and management, testing, and in many other ways',
            "active": 1
        })

    def test_get_all_skills(self): 
        self.assertEqual(Skill.get_all_skills(), [
            {
                "skill_id": 200, 
                "skill_name": 'Python Programming', 
                "skill_desc": 'Python is often used as a support language for software developers, for build control and management, testing, and in many other ways',
                "active": 1
            }, 

            {
                "skill_id": 201, 
                "skill_name": 'Emotional Intelligence', 
                "skill_desc": 'Emotional intelligence is the ability to recognize, manage, and understand emotions.',
                "active": 1
            },

            {
                "skill_id": 202, 
                "skill_name": 'Web Development', 
                "skill_desc": 'Web development, also known as website development, refers to the tasks associated with creating, building, and maintaining websites and web applications that run online on a browser.',
                "active": 0 
            }
        ])

    def test_get_all_skills_active(self):
        self.assertEqual(Skill.get_all_skills_active(), [
            {
                "skill_id": 200, 
                "skill_name": 'Python Programming', 
                "skill_desc": 'Python is often used as a support language for software developers, for build control and management, testing, and in many other ways',
                "active": 1
            }, 

            {
                "skill_id": 201, 
                "skill_name": 'Emotional Intelligence', 
                "skill_desc": 'Emotional intelligence is the ability to recognize, manage, and understand emotions.',
                "active": 1
            }
        ])

    def test_get_active_skills_list(self): 
        self.assertEqual(Skill.get_active_skills_list([200, 201]), [200, 201])

    def test_check_skill_exists(self): 
        self.assertEqual(Skill.check_skill_exists('Python Programming'), True)

    def test_create_skill(self): 
        self.assertEqual(Skill.create_skill(skill_id=203, skill_name='Business Consulting', skill_desc='Business consulting includes helping to identify, address, and overcome obstacles to meeting a company’s goals. ', active=1)
        ,True)

    def test_error_create_skill(self): 
        self.assertEqual(Skill.create_skill(skill_id=204, skill_name= 583358, skill_desc='digital marketing is both creative (photography, writing, and design) and analytical (Google Analytics, CRO, marketing automation)', active=1)
        ,False)
    
    def test_toggle_active(self):
        self.assertEqual(Skill.toggle_active(201,0),True)

    def test_edit_skill(self):
        self.assertEqual(Skill.edit_skill(skill_id=200, new_skill_name='Introduction to Python Programming', new_skill_desc='Python can optimise your digital solution development cycle and workflow')
        , True)
    

if __name__ == "__main__": 
    unittest.main()