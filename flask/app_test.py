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
    
    def test_get_team_members(self):
        self.s1 = Staff(staff_id = 140001, role_id = 2, staff_fname = "Kelvin", staff_lname = "Yap", dept = "Sales", email = "kelvin.yap.2020@scis.smu.edu.sg")

        self.s2 = Staff(staff_id = 140002, role_id = 3, staff_fname = "Dom", staff_lname = "Teow", dept = "Sales", email = "dom.teow.2020@scis.smu.edu.sg")        

        self.ro3 = Role(role_id = 3, role_name = "Manager")
        db.session.add_all([self.s1, self.s2, self.ro3])
        db.session.commit()
        response = self.client.get("get_team_members/140002")
        self.assertEqual(response.json, {
            'manager': {
                'dept': 'Sales',
                'email': 'dom.teow.2020@scis.smu.edu.sg',
                'role_id': 3,
                'staff_fname': 'Dom',
                'staff_id': 140002,
                'staff_lname': 'Teow'},
            'team_members': [{
                'dept': 'Sales',
                'email': 'kelvin.yap.2020@scis.smu.edu.sg',
                'role_id': 2,
                'staff_fname': 'Kelvin',
                'staff_id': 140001,
                'staff_lname': 'Yap'}]
        })
        
    def test_get_team_members_invalid(self):
        self.s1 = Staff(staff_id = 140001, role_id = 2, staff_fname = "Kelvin", staff_lname = "Yap", dept = "Sales", email = "kelvin.yap.2020@scis.smu.edu.sg")

        self.ro2 = Role(role_id = 2, role_name = "User")
        
        self.ro3 = Role(role_id = 3, role_name = "Manager")
        
        db.session.add_all([self.s1, self.ro2, self.ro3])
        db.session.commit()
        response = self.client.get("get_team_members/140001")
        self.assertEqual(response.json, {
            "Error" : "You are not a manager."
        })    
        
    def test_get_all_staff(self):
        self.ro1 = Role(role_id = 1, role_name = "Admin")
        
        self.s3 = Staff(staff_id = 140003, role_id = 1, staff_fname = "Bruno", staff_lname = "Goh", dept = "HR", email = "bruno.goh.2020@scis.smu.edu.sg")
        
        self.s1 = Staff(staff_id = 140001, role_id = 2, staff_fname = "Kelvin", staff_lname = "Yap", dept = "Sales", email = "kelvin.yap.2020@scis.smu.edu.sg")

        self.s2 = Staff(staff_id = 140002, role_id = 3, staff_fname = "Dom", staff_lname = "Teow", dept = "Sales", email = "dom.teow.2020@scis.smu.edu.sg")
        
        db.session.add_all([self.s1, self.s2, self.s3, self.ro1])
        db.session.commit()
        self.maxDiff = None
        response = self.client.get("get_all_staff/140003")
        self.assertEqual(response.json, {
            'all_staff': [{
                'dept': 'Sales',
                'email': 'kelvin.yap.2020@scis.smu.edu.sg',
                'role_id': 2,
                'staff_fname': 'Kelvin',
                'staff_id': 140001,
                'staff_lname': 'Yap'},
                {'dept': 'Sales',
                 'email': 'dom.teow.2020@scis.smu.edu.sg',
                 'role_id': 3,
                 'staff_fname': 'Dom',
                 'staff_id': 140002,
                 'staff_lname': 'Teow'}],
            'hr': {
                'dept': 'HR',
                'email': 'bruno.goh.2020@scis.smu.edu.sg',
                'role_id': 1,
                'staff_fname': 'Bruno',
                'staff_id': 140003,
                'staff_lname': 'Goh'}
        })    
    
    
    
    
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
        
    def test_view_courses_under_skill(self):
        self.ljpsr1 = Ljps_role(ljpsr_id = 1, role_title = "Engineer", role_desc = "Be an Engineer", active = 1)
        self.rrs1 = Role_required_skill(ljpsr_id = 1, skill_id = 3)
        self.s1 = Skill(skill_id = 3, skill_name = "Fast hands", skill_desc = "Get your hands moving", active = 1)
        self.as1 = Attached_skill(skill_id = 3,course_id = 'COR002')
        self.c1 = Course(course_id = "COR002", course_name = "Wiring 101", course_desc = "Handling wiring for engineers", course_status = "Active", course_type = "External", course_category = "Technical")    
        db.session.add_all([self.ljpsr1, self.as1, self.rrs1, self.s1, self.c1])
        db.session.commit()
        response = self.client.get("view_courses_under_skill/140001/1")
        self.maxDiff = None
        self.assertEqual(response.json, {
            'data': {'ljps_role': {
                        'active': 1,
                        'ljpsr_id': 1,
                        'role_desc': 'Be an Engineer',
                        'role_title': 'Engineer'},
                     'skills_with_courses': [{
                         'active': 1,
                         'courses': [{
                             'course_category': 'Technical',
                             'course_desc': 'Handling wiring for engineers',
                             'course_id': 'COR002',
                             'course_name': 'Wiring 101',
                             'course_status': 'Active',
                             'course_type': 'External'}],
                         'skill_desc': 'Get your hands moving',
                         'skill_id': 3,
                         'skill_name': 'Fast hands'}]
                     }
        })
        
    def test_view_courses_under_skill_invalid(self):
        self.ljpsr1 = Ljps_role(ljpsr_id = 1, role_title = "Engineer", role_desc = "Be an Engineer", active = 1)
        # self.rrs1 = Role_required_skill(ljpsr_id = 1, skill_id = 3)
        self.s1 = Skill(skill_id = 3, skill_name = "Fast hands", skill_desc = "Get your hands moving", active = 1)
        self.as1 = Attached_skill(skill_id = 3,course_id = 'COR002')
        self.c1 = Course(course_id = "COR002", course_name = "Wiring 101", course_desc = "Handling wiring for engineers", course_status = "Active", course_type = "External", course_category = "Technical")    
        db.session.add_all([self.ljpsr1, self.as1, self.s1, self.c1])
        db.session.commit()
        response = self.client.get("view_courses_under_skill/140001/1")
        self.assertEqual(response.json, {
            "message": "Skill has no courses assigned to it"
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
        
    def test_view_skills_needed_for_role(self):
        self.ljpsr1 = Ljps_role(ljpsr_id = 1, role_title = "Engineer", role_desc = "Be an Engineer", active = 1)        
        self.r1 = Registration(reg_id = 1, course_id = 'COR002', staff_id = 140001, reg_status = 'Registered', completion_status = "Completed")        
        self.as1 = Attached_skill(skill_id = 3,course_id = 'COR002')
        self.rrs1 = Role_required_skill(ljpsr_id = 1, skill_id = 3)
        self.s1 = Skill(skill_id = 3, skill_name = "Fast hands", skill_desc = "Get your hands moving", active = 1)
        db.session.add_all([self.ljpsr1, self.r1, self.as1, self.rrs1, self.s1])
        db.session.commit()
        response = self.client.get("/view_skills_needed_for_role/140001/1")
        self.assertEqual(response.json, {
            'data': {'ljps_role': {'active': 1,
                                   'ljpsr_id': 1,
                                   'role_desc': 'Be an Engineer',
                                   'role_title': 'Engineer'},
                     'skills': [{'active': 1,
                                 'completed': 1,
                                 'skill_desc': 'Get your hands moving',
                                 'skill_id': 3,
                                 'skill_name': 'Fast hands'}]
                     }
        })
        
    def test_view_skills_needed_for_role_invalid(self):
        self.ljpsr1 = Ljps_role(ljpsr_id = 1, role_title = "Engineer", role_desc = "Be an Engineer", active = 1)        
        self.r1 = Registration(reg_id = 1, course_id = 'COR002', staff_id = 140001, reg_status = 'Registered', completion_status = "Completed")        
        self.as1 = Attached_skill(skill_id = 3,course_id = 'COR002')
        # self.rrs1 = Role_required_skill(ljpsr_id = 1, skill_id = 3)
        self.s1 = Skill(skill_id = 3, skill_name = "Fast hands", skill_desc = "Get your hands moving", active = 1)
        db.session.add_all([self.ljpsr1, self.r1, self.as1, self.s1])
        db.session.commit()
        response = self.client.get("/view_skills_needed_for_role/140001/1")
        self.assertEqual(response.json, {
            "message": "Role has no skills assigned to it"
        })
        
class TestLearningJourney(TestApp):
    def test_create_lj(self):
        self.lj1 = Learning_journey(journey_id = 1, ljpsr_id = 1, staff_id= 140001, status = 1)
        self.s1 = Staff(staff_id = 140001, role_id = 2, staff_fname = "Kelvin", staff_lname = "Yap", dept = "Sales", email = "kelvin.yap.2020@scis.smu.edu.sg")
        self.ljpsr1 = Ljps_role(ljpsr_id = 1, role_title = "Engineer", role_desc = "Be an Engineer", active = 1)
        self.c1 = Course(course_id = "COR002", course_name = "Wiring 101", course_desc = "Handling wiring for engineers", course_status = "Active", course_type = "External", course_category = "Technical")   
        self.s1 = Skill(skill_id = 3, skill_name = "Fast hands", skill_desc = "Get your hands moving", active = 1)
        db.session.add_all([self.lj1, self.ljpsr1, self.s1, self.c1, self.s1])
        db.session.commit()
                
        request_body = {
            'Fast Hands':[{
                'course_id':'COR002',
                'course_name':'Wiring 101'}]
            }

        response = self.client.post("/createlj/1&140001&" + json.dumps(request_body),
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.json, {
            'code': 201,
            'data': {
                'course_id': 'COR002',
                'journey_id': 2
                }
        })
            
        
        
    def test_readlj(self):
        self.lj1 = Learning_journey(journey_id = 1, ljpsr_id = 1, staff_id= 140001, status = 1)
        self.r1 = Registration(reg_id = 1, course_id = 'COR002', staff_id = 140001, reg_status = 'Registered', completion_status = "Completed")
        self.ljpsr1 = Ljps_role(ljpsr_id = 1, role_title = "Engineer", role_desc = "Be an Engineer", active = 1)
        self.rrs1 = Role_required_skill(ljpsr_id = 1, skill_id = 3)
        self.s1 = Skill(skill_id = 3, skill_name = "Fast hands", skill_desc = "Get your hands moving", active = 1)
        self.ljc1 = Lj_course(journey_id = 1, course_id = "COR002")
        self.c1 = Course(course_id = "COR002", course_name = "Wiring 101", course_desc = "Handling wiring for engineers", course_status = "Active", course_type = "External", course_category = "Technical")    
        db.session.add_all([self.lj1, self.ljpsr1, self.r1, self.rrs1, self.s1, self.c1, self.ljc1])
        db.session.commit()
        response = self.client.get("readlj/140001")
        self.assertEqual(response.json, {
            'data': [{'courses': [{
                'course_category': 'Technical',
                'course_desc': 'Handling wiring for engineers',
                'course_id': 'COR002',
                'course_name': 'Wiring 101',
                'course_status': 1,
                'course_type': 'External'
                }],
            'journey_id': 1,
            'ljpsr_id': 1,
            'role_desc': 'Be an Engineer',
            'role_title': 'Engineer',
            'skills': [{
                'skill_desc': 'Get your hands moving',
                'skill_id': 3,'skill_name': 'Fast hands',
                'status': 0}],
            'staff_id': 140001,
            'status': 1}]
        })
        
    # def test_add_course(self):
    #     self.lj1 = Learning_journey(journey_id = 1, ljpsr_id = 1, staff_id= 140001, status = 1)
    #     self.ljc1 = Lj_course(journey_id = 1, course_id = "COR002")
    #     db.session.add_all([self.ljc1, self.lj1])
    #     db.session.commit()
    #     response = self.client.post("add_course/1")
    #     self.assertEqual(response.json, {
    #     })
    #     pass
    
    # def test_edit_LJ_courses(self):
    #     self.lj1 = Learning_journey(journey_id = 1, ljpsr_id = 1, staff_id= 140001, status = 1)
    #     self.ljc1 = Lj_course(journey_id = 1, course_id = "COR002")
    #     self.c1 = Course(course_id = "COR002", course_name = "Wiring 101", course_desc = "Handling wiring for engineers", course_status = "Active", course_type = "External", course_category = "Technical")    
    #     db.session.add_all([self.lj1, self.ljc1, self.c1])
    #     db.session.commit()
        
    #     request_body = {
    #         "journey_id": 1,
    #         "course_arr": json.dumps({'Fast Hands':[{'course_id':'COR002','course_name':'Wiring 101'}]})
    #     }

    #     response = self.client.post("/edit_LJ_courses/",
    #                                 data=json.dumps(request_body),
    #                                 content_type='application/json')
    #     self.assertEqual(response.json, request_body)
    #     pass
    
    # def test_delete_LJ(self):
    #     pass
    
    
    pass

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