import unittest
import flask_testing
import json
from initdb import db
from app import app
from course import Course
from role import Role
from skill import Skill
from staff import Staff
from attached_skill import Attached_skill
from learning_journey import Learning_journey
from lj_course import Lj_course
from ljps_role import Ljps_role
from registration import Registration
from role_required_skill import Role_required_skill

class TestApp(flask_testing.TestCase):
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {}
    app.config['TESTING'] = True
    def create_app(self):
        return app

    def setUp(self):
        db.create_all()
        

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class TestViewSkills(TestApp):
    def test_view_skills_needed_for_role(self):
        ljps1 = Ljps_role(ljpsr_id = 1, role_title = "Technician", role_desc = "On site and off site trouble shooting of printer machines.", active = 1)
        regis1 = Registration(reg_id = 1, course_id = 'COR002', staff_id = 130001, reg_status = 'Registered', completion_status = "Completed")
        attSkill1 = Attached_skill(skill_id = 3,course_id = 'COR002')
        db.session.add(ljps1)
        db.session.add(regis1)
        db.session.add(attSkill1)
        db.session.commit()
        # response = self.client.get("/view_skills_needed_for_role/130001/1")
        # self.assertEqual(response.json,)
        # Not done yet....




if __name__ == "__main__":
    unittest.main()  