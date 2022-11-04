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

class TestStaff(TestApp):
    def test_login(self):
        self.s1 = Staff(staff_id = 140001, role_id = 2, staff_fname = "Kelvin", staff_lname = "Yap", dept = "Sales", email = "kelvin.yap.2020@scis.smu.edu.sg")
        db.session.add(self.s1)
        db.session.commit()
        response = self.client.get("login/140001")
        self.assertEqual(response.json, {
            "data" :{  
                'staff_id': 140001,
                'role_id': 2,
                'staff_fname': "Kelvin",
                'staff_lname': "Yap",
                'dept': "Sales",
                'email': "kelvin.yap.2020@scis.smu.edu.sg"
            }
        })
    def test_login_invalid(self):
        response = self.client.get("login/123456")
        self.assertEqual(response.json, {
            "message" : "There is no staff with that ID"
        })
        pass    
    
    
class TestRole(TestApp):
    def test_all_roles(self):
        self.ljpsr1 = Ljps_role(ljpsr_id = 1, role_title = "Engineer", role_desc = "Be an Engineer", active = 1)
        self.r1 = Registration(reg_id = 1, course_id = 'COR002', staff_id = 140001, reg_status = 'Registered', completion_status = "Completed")
        self.as1 = Attached_skill(skill_id = 3,course_id = 'COR002')
        self.rrs1 = Role_required_skill(ljpsr_id = 1, skill_id = 3)
        db.session.add_all([self.ljpsr1, self.r1, self.as1, self.rrs1])
        db.session.commit()
        response = self.client.get("all_roles/140001")
        self.assertEqual(response.json, {
            'data': [{
                'active': 1,
                'attained': 1,
                'ljpsr_id': 1,
                'role_desc': 'Be an Engineer',
                'role_title': 'Engineer'
                }]
        })
        
    def test_all_roles_invalid(self):
        response = self.client.get("all_roles/140001")
        self.assertEqual(response.json, {
            "message" : "There are no roles"
        })
        
    def test_view_role(self):
        self.ljpsr1 = Ljps_role(ljpsr_id = 1, role_title = "Engineer", role_desc = "Be an Engineer", active = 1)
        self.rrs1 = Role_required_skill(ljpsr_id = 1, skill_id = 3)
        self.s1 = Skill(skill_id = 3, skill_name = "Fast hands", skill_desc = "Get your hands moving", active = 1)
        db.session.add_all([self.ljpsr1, self.rrs1, self.s1])
        db.session.commit()
        response = self.client.get("role/1")
        self.assertEqual(response.json, {
            'data': 
                {
                'ljps_role':
                    {'active': 1,
                    'ljpsr_id': 1,
                    'role_desc': 'Be an Engineer',
                    'role_title': 'Engineer'
                    },
                'skills': [{'active': 1,
                            'skill_desc': 'Get your hands moving',
                            'skill_id': 3,
                            'skill_name': 'Fast hands'
                            }]
                }
        })
        
class TestCourse(TestApp):
    def test_find_course(self):
        self.c1 = Course(course_id = "COR002", course_name = "Wiring 101", course_desc = "Handling wiring for engineers", course_status = "Active", course_type = "External", course_category = "Technical")    
        db.session.add(self.c1)
        db.session.commit()
        response = self.client.get("course/COR002")
        self.assertEqual(response.json, {
            'data': 
                {'course_category': 'Technical',
                 'course_desc': 'Handling wiring for engineers',
                 'course_id': 'COR002',
                 'course_name': 'Wiring 101',
                 'course_status': 'Active',
                 'course_type': 'External'}
        })
        
    def test_find_course_invalid(self):
        response = self.client.get("course/COR042")
        self.assertEqual(response.json, {
            "message" : "Course not found"
        })
        
        
class TestSkills(TestApp):
    def test_view_skill_by_id(self):
        self.s1 = Skill(skill_id = 3, skill_name = "Fast hands", skill_desc = "Get your hands moving", active = 1)
        db.session.add(self.s1)
        db.session.commit()
        response = self.client.get("skill/3")
        self.assertEqual(response.json, {
            'data': {
                'skill': {
                    'active': 1,
                    'skill_desc': 'Get your hands moving',
                    'skill_id': 3,
                    'skill_name': 'Fast hands'}
                }
        })
    def test_view_skill_by_id_invalid(self):
        response = self.client.get("skill/10")
        self.assertEqual(response.json, {
            "message" : "Skill not found"
        })        
        
    # def test_view_skills_needed_for_role(self):
    #     ljps1 = Ljps_role(ljpsr_id = 1, role_title = "Technician", role_desc = "On site and off site trouble shooting of printer machines.", active = 1)
    #     self.r1 = Registration(reg_id = 1, course_id = 'COR002', staff_id = 140001, reg_status = 'Registered', completion_status = "Completed")        self.as1 = Attached_skill(skill_id = 3,course_id = 'COR002')
    #     self.rrs1 = Role_required_skill(ljpsr_id = 1, skill_id = 3)
    #     self.s1 = Skill(skill_id = 3, skill_name = "Fast hands", skill_desc = "Get your hands moving", active = 1)
    #     db.session.add(ljps1)
    #     db.session.add(regis1)
    #     db.session.add(attSkill1)
    #     db.session.commit()
    #     response = self.client.get("/view_skills_needed_for_role/130001/1")
    #     self.assertEqual(response.json, {
            
    #     })

class TestLJCourse(TestApp):
    def test_lj_course_by_journey(self):
        self.ljc1 = Lj_course(journey_id = 1, course_id = "COR002")
        db.session.add(self.ljc1)
        db.session.commit()
        response = self.client.get("lj_course_by_journey/1")
        self.assertEqual(response.json, {
            'data': {
                'lj_course': [{
                    'course_id': 'COR002',
                    'journey_id': 1}]
                }
        })
        
    def test_lj_course_by_journey_invalid(self):
        response = self.client.get("lj_course_by_journey/5")
        self.assertEqual(response.json, {
            "message": "Learning Journey contains no courses."
        })

class TestRoleRequireSkill(TestApp):
    def test_role_require_skill_by_ljpsr(self):
        self.rrs1 = Role_required_skill(ljpsr_id = 1, skill_id = 3)
        db.session.add(self.rrs1)
        db.session.commit()
        response = self.client.get("role_require_skill_by_ljpsr/1")
        self.assertEqual(response.json, {
            'data': {
                'role_require_skill': [{
                    'ljpsr_id': 1,
                    'skill_id': 3}]
                }
        })
        
    def test_role_require_skill_by_ljpsr_invalid(self):
        response = self.client.get("role_require_skill_by_ljpsr/7")
        self.assertEqual(response.json, {
            "message": "Role has no skills assigned to it"
        })
        
if __name__ == "__main__":
    unittest.main()  