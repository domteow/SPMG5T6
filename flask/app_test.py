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
        self.st1 = Staff(staff_id = 140001, role_id = 2, staff_fname = "Kelvin", staff_lname = "Yap", dept = "Sales", email = "kelvin.yap.2020@scis.smu.edu.sg")
        db.session.add(self.st1)
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
    
    def test_get_team_members_deprecated(self):
        self.st1 = Staff(staff_id = 140001, role_id = 2, staff_fname = "Kelvin", staff_lname = "Yap", dept = "Sales", email = "kelvin.yap.2020@scis.smu.edu.sg")

        self.st2 = Staff(staff_id = 140002, role_id = 3, staff_fname = "Dom", staff_lname = "Teow", dept = "Sales", email = "dom.teow.2020@scis.smu.edu.sg")        

        self.ro3 = Role(role_id = 3, role_name = "Manager")
        db.session.add_all([self.st1, self.st2, self.ro3])
        db.session.commit()
        response = self.client.get("get_team_members_deprecated/140002")
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
        
    def test_get_team_members_deprecated_invalid(self):
        self.st1 = Staff(staff_id = 140001, role_id = 2, staff_fname = "Kelvin", staff_lname = "Yap", dept = "Sales", email = "kelvin.yap.2020@scis.smu.edu.sg")

        self.ro2 = Role(role_id = 2, role_name = "User")
        
        self.ro3 = Role(role_id = 3, role_name = "Manager")
        
        db.session.add_all([self.st1, self.ro2, self.ro3])
        db.session.commit()
        response = self.client.get("get_team_members_deprecated/140001")
        self.assertEqual(response.json, {
            "Error" : "You are not a manager"
        })    
        
    def test_get_all_staff(self):
        self.ro1 = Role(role_id = 1, role_name = "Admin")
        
        self.st3 = Staff(staff_id = 140003, role_id = 1, staff_fname = "Bruno", staff_lname = "Goh", dept = "HR", email = "bruno.goh.2020@scis.smu.edu.sg")
        
        self.st1 = Staff(staff_id = 140001, role_id = 2, staff_fname = "Kelvin", staff_lname = "Yap", dept = "Sales", email = "kelvin.yap.2020@scis.smu.edu.sg")

        self.st2 = Staff(staff_id = 140002, role_id = 3, staff_fname = "Dom", staff_lname = "Teow", dept = "Sales", email = "dom.teow.2020@scis.smu.edu.sg")
        
        db.session.add_all([self.st1, self.st2, self.st3, self.ro1])
        db.session.commit()
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
    
    def test_get_all_staff_invalid(self):
        self.ro1 = Role(role_id = 1, role_name = "Admin")
        
        self.ro2 = Role(role_id = 2, role_name = "User")
        
        self.st3 = Staff(staff_id = 140003, role_id = 1, staff_fname = "Bruno", staff_lname = "Goh", dept = "HR", email = "bruno.goh.2020@scis.smu.edu.sg")
        
        self.st1 = Staff(staff_id = 140001, role_id = 2, staff_fname = "Kelvin", staff_lname = "Yap", dept = "Sales", email = "kelvin.yap.2020@scis.smu.edu.sg")

        self.st2 = Staff(staff_id = 140002, role_id = 3, staff_fname = "Dom", staff_lname = "Teow", dept = "Sales", email = "dom.teow.2020@scis.smu.edu.sg")
        
        db.session.add_all([self.st1, self.st2, self.st3, self.ro1, self.ro2])
        db.session.commit()
        response = self.client.get("get_all_staff/140001")
        self.assertEqual(response.json, {
            "Error" : "You are not a HR"
        })  
        
    def test_get_team_members(self):
        self.st1 = Staff(staff_id = 140001, role_id = 2, staff_fname = "Kelvin", staff_lname = "Yap", dept = "Sales", email = "kelvin.yap.2020@scis.smu.edu.sg")
        self.st2 = Staff(staff_id = 140002, role_id = 3, staff_fname = "Dom", staff_lname = "Teow", dept = "Sales", email = "dom.teow.2020@scis.smu.edu.sg")
        self.st3 = Staff(staff_id = 140003, role_id = 1, staff_fname = "Bruno", staff_lname = "Goh", dept = "HR", email = "bruno.goh.2020@scis.smu.edu.sg")
        self.r1 = Registration(reg_id = 1, course_id = 'COR002', staff_id = 140001, reg_status = 'Registered', completion_status = "Completed")
        self.as1 = Attached_skill(skill_id = 3,course_id = 'COR002')
        
        db.session.add_all([self.st1, self.st2, self.st3, self.r1, self.as1])
        db.session.commit()
        self.maxDiff = None
        response = self.client.get("/get_team_members/140002&Sales")
        self.assertEqual(response.json, {
            'data': {
                'team': [{
                        'courses_completed_count': 1,
                        'courses_ongoing_count': 0,
                        'role_id': 2,
                        'skill_acquired_count': 1,
                        'skill_ongoing_count': 0,
                        'staff_id': 140001,
                        'staff_name': 'Kelvin Yap'
                    }]
                }
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
        
    def test_edit_role_details(self):
        self.ljpsr1 = Ljps_role(ljpsr_id = 1, role_title = "Engineer", role_desc = "Be an Engineer", active = 1)
        db.session.add(self.ljpsr1)
        db.session.commit()
        request_body = {
                "ljpsr_id": 1,
                "new_role_name": "A good Engineer",
                "new_role_desc": "Be a very good Engineer"
            }

        response = self.client.post("/edit_role_details",
                                data=json.dumps(request_body),
                                content_type='application/json')
        self.assertEqual(response.json, {
            'data': {
                'message': 'Role name and description has been updated successfully'
                }
        })
        
    def test_read_all_roles(self):
        self.ljpsr1 = Ljps_role(ljpsr_id = 1, role_title = "Engineer", role_desc = "Be an Engineer", active = 1)
        self.s1 = Skill(skill_id = 3, skill_name = "Fast hands", skill_desc = "Get your hands moving", active = 1)
        self.s2 = Skill(skill_id = 4, skill_name = "Quick Thinking", skill_desc = "Think fast", active = 1)
        self.rrs1 = Role_required_skill(ljpsr_id = 1, skill_id = 3)
        self.rrs2 = Role_required_skill(ljpsr_id = 1, skill_id = 4)
        db.session.add_all([self.ljpsr1, self.s1, self.s2, self.rrs1, self.rrs2])
        db.session.commit()
        response = self.client.get("read_all_roles")
        self.assertEqual(response.json, {
            'data': [{'active': 1,
                      'ljpsr_id': 1,
                      'role_desc': 'Be an Engineer',
                      'role_title': 'Engineer',
                    'skills': [{'active': 1,
                                'skill_desc': 'Get your hands moving',
                                'skill_id': 3,
                                'skill_name': 'Fast hands'},
                               {'active': 1,
                                'skill_desc': 'Think fast',
                                'skill_id': 4,
                                'skill_name': 'Quick Thinking'}]}]
        })
 
    def test_create_role(self):
        
        self.s1 = Skill(skill_id = 3, skill_name = "Fast hands", skill_desc = "Get your hands moving", active = 1)
        db.session.add(self.s1)
        db.session.commit()
        
        request_body = {
            "newRoleName" : "CEO",
            "newRoleDesc" : "Be the boss",
            "newRoleSkills" : json.dumps([3])
            }
        response = self.client.post("/create_role",
                                data=json.dumps(request_body),
                                content_type='application/json')
        self.assertEqual(response.json, {
            "message": "The role was successfully created"
        })
        
    def test_create_role_exists(self):
        self.ljpsr1 = Ljps_role(ljpsr_id = 1, role_title = "Engineer", role_desc = "Be an Engineer", active = 1)
        self.s1 = Skill(skill_id = 3, skill_name = "Fast hands", skill_desc = "Get your hands moving", active = 1)
        db.session.add_all([self.ljpsr1, self.s1])
        db.session.commit()
        
        request_body = {
            "newRoleName" : "Engineer",
            "newRoleDesc" : "Be an Engineer",
            "newRoleSkills" : json.dumps([3])
            }
        response = self.client.post("/create_role",
                                data=json.dumps(request_body),
                                content_type='application/json')
        self.assertEqual(response.json, {
                "message": "The role name already exists"
        })
    
    def test_delete_role_active(self):
        self.ljpsr1 = Ljps_role(ljpsr_id = 1, role_title = "Engineer", role_desc = "Be an Engineer", active = 0)
        db.session.add(self.ljpsr1)
        db.session.commit()
        
        response = self.client.get("/delete_role/1&1&Engineer")
        self.assertEqual(response.json, {
            'data': {'message': 'Engineer is now active'}
        })

    def test_delete_role_inactive(self):
        self.ljpsr1 = Ljps_role(ljpsr_id = 1, role_title = "Engineer", role_desc = "Be an Engineer", active = 1)
        db.session.add(self.ljpsr1)
        db.session.commit()
        
        response = self.client.get("/delete_role/1&0&Engineer")
        self.assertEqual(response.json, {
            'data': {'message': 'Engineer is now inactive'}
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
        
    def test_get_courses_of_lj(self):
        self.ljc1 = Lj_course(journey_id = 1, course_id = "COR002")
        self.r1 = Registration(reg_id = 1, course_id = 'COR002', staff_id = 140001, reg_status = 'Registered', completion_status = "Completed")
        self.c1 = Course(course_id = "COR002", course_name = "Wiring 101", course_desc = "Handling wiring for engineers", course_status = "Active", course_type = "External", course_category = "Technical")    
        db.session.add_all([self.ljc1, self.r1, self.c1])
        db.session.commit()
        response = self.client.get("get_courses_of_lj/140001&1")
        self.assertEqual(response.json, {
            'data': [{'course_id': 'COR002',
                      'course_name': 'Wiring 101',
                      'course_status': 1,
                      'journey_id': 1}]
        })
        
    def test_get_courses_of_lj_invalid(self):
        self.ljc1 = Lj_course(journey_id = 2, course_id = "COR002")
        self.r1 = Registration(reg_id = 1, course_id = 'COR002', staff_id = 140001, reg_status = 'Registered', completion_status = "Completed")
        self.c1 = Course(course_id = "COR002", course_name = "Wiring 101", course_desc = "Handling wiring for engineers", course_status = "Active", course_type = "External", course_category = "Technical")    
        db.session.add_all([self.ljc1, self.r1, self.c1])
        db.session.commit()
        response = self.client.get("get_courses_of_lj/140001&1")
        self.assertEqual(response.json, {
            "data" : {
                "message" : "Error retrieving courses"
                }
        })
    
    def test_get_all_courses(self):
        self.c1 = Course(course_id = "COR002", course_name = "Wiring 101", course_desc = "Handling wiring for engineers", course_status = "Active", course_type = "External", course_category = "Technical")   
        db.session.add(self.c1)
        db.session.commit()
        response = self.client.get("courses")
        self.assertEqual(response.json, {
            'data': [{'course_category': 'Technical',
                      'course_desc': 'Handling wiring for engineers',
                      'course_id': 'COR002',
                      'course_name': 'Wiring 101',
                      'course_status': 'Active',
                      'course_type': 'External'}]
        })

    def test_get_all_courses_invalid(self):
        response = self.client.get("courses")
        self.assertEqual(response.json, {
            "message": "There are no courses."
        })
        
    def test_get_courses_by_skill(self):
        self.s1 = Skill(skill_id = 3, skill_name = "Fast hands", skill_desc = "Get your hands moving", active = 1)
        self.c1 = Course(course_id = "COR002", course_name = "Wiring 101", course_desc = "Handling wiring for engineers", course_status = "Active", course_type = "External", course_category = "Technical")    
        self.as1 = Attached_skill(skill_id = 3,course_id = 'COR002')
        db.session.add_all([self.s1, self.c1, self.as1])
        db.session.commit()
        
        response = self.client.get("/get_courses_by_skill/3")
        self.assertEqual(response.json, {
            'data': {
                'courses': [{
                    'course_category': 'Technical',
                    'course_desc': 'Handling wiring for engineers',
                    'course_id': 'COR002',
                    'course_name': 'Wiring 101',
                    'course_status': 'Active',
                    'course_type': 'External'}]}
        })  
    
    def test_get_courses_by_skill_invalid(self):
        self.s1 = Skill(skill_id = 3, skill_name = "Fast hands", skill_desc = "Get your hands moving", active = 1)
        self.c1 = Course(course_id = "COR002", course_name = "Wiring 101", course_desc = "Handling wiring for engineers", course_status = "Active", course_type = "External", course_category = "Technical")    
        db.session.add_all([self.s1, self.c1])
        db.session.commit()
        
        response = self.client.get("/get_courses_by_skill/3")
        self.assertEqual(response.json, {
            "message": "There are no attached courses"
        })  
        
        
class TestSkill(TestApp):
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
        
    def test_edit_skills_in_ljps_role(self):
        self.ljpsr1 = Ljps_role(ljpsr_id = 1, role_title = "Engineer", role_desc = "Be an Engineer", active = 1)
        self.rrs1 = Role_required_skill(ljpsr_id = 1, skill_id = 3)
        db.session.add_all([self.ljpsr1, self.rrs1])
        db.session.commit()        
        request_body = {
            "ljpsr_id" : 1,
            "added_skills" : [1,2],
            "deleted_skills" : [3]
            }

        response = self.client.post("/edit_skills_in_ljps_role",
                                data=json.dumps(request_body),
                                content_type='application/json')
        self.assertEqual(response.json, {
            'data': [1, 2]
        })
        
    def test_create_skill(self):
        self.c1 = Course(course_id = "COR002", course_name = "Wiring 101", course_desc = "Handling wiring for engineers", course_status = "Active", course_type = "External", course_category = "Technical")    
        db.session.add(self.c1)
        db.session.commit()
        
        request_body = {
            "newSkillName" : "Fast hands",
            "newSkillDesc" : "Get your hands moving",
            "newSkillCourses" : json.dumps(["COR002"])
            }

        response = self.client.post("/create_skill",
                                data=json.dumps(request_body),
                                content_type='application/json')
        self.assertEqual(response.json, {
            'message': 'The role was successfully created.'
        })
        
    def test_create_skill_exists(self):
        self.c1 = Course(course_id = "COR002", course_name = "Wiring 101", course_desc = "Handling wiring for engineers", course_status = "Active", course_type = "External", course_category = "Technical")  
        self.s1 = Skill(skill_id = 3, skill_name = "Fast hands", skill_desc = "Get your hands moving", active = 1)  
        db.session.add_all([self.c1, self.s1])
        db.session.commit()
        
        request_body = {
            "newSkillName" : "Fast hands",
            "newSkillDesc" : "Get your hands moving",
            "newSkillCourses" : json.dumps(["COR002"])
            }

        response = self.client.post("/create_skill",
                                data=json.dumps(request_body),
                                content_type='application/json')
        self.assertEqual(response.json, {
            'code': 401,
            'data': {'skill_name': 'Fast hands'},
            'message': 'The skill name already exists'
        })    
    
    def test_get_all_skills(self):
        self.s1 = Skill(skill_id = 3, skill_name = "Fast hands", skill_desc = "Get your hands moving", active = 1)  
        db.session.add(self.s1)
        db.session.commit()
        response = self.client.get("/skills")
        self.assertEqual(response.json, {
            'data': {
                'skills': [{'active': 1,
                            'skill_desc': 'Get your hands moving',
                            'skill_id': 3,
                            'skill_name': 'Fast hands'}]}
        })
        
    def test_get_all_skills_invalid(self):
        response = self.client.get("/skills")
        self.assertEqual(response.json, {
            "message": "There are no skills"
        })
    
    def test_get_all_skills_and_courses(self):
        self.s1 = Skill(skill_id = 3, skill_name = "Fast hands", skill_desc = "Get your hands moving", active = 1)
        self.c1 = Course(course_id = "COR002", course_name = "Wiring 101", course_desc = "Handling wiring for engineers", course_status = "Active", course_type = "External", course_category = "Technical")    
        self.as1 = Attached_skill(skill_id = 3,course_id = 'COR002')
        db.session.add_all([self.s1, self.c1, self.as1])
        db.session.commit()
        response = self.client.get("/get_all_skills_and_courses")
        self.assertEqual(response.json, {
            'data': {
                'skills': [{
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
            
    def test_get_all_skills_and_courses_invalid(self):
        self.s1 = Skill(skill_id = 3, skill_name = "Fast hands", skill_desc = "Get your hands moving", active = 0)
        self.c1 = Course(course_id = "COR002", course_name = "Wiring 101", course_desc = "Handling wiring for engineers", course_status = "Active", course_type = "External", course_category = "Technical")    
        self.as1 = Attached_skill(skill_id = 3,course_id = 'COR002')
        db.session.add_all([self.s1, self.c1, self.as1])
        db.session.commit()
        
        response = self.client.get("/get_all_skills_and_courses")
        self.assertEqual(response.json, {
            'message': 'There are no skills.'
        })
        
    def test_delete_skill_active(self):
        self.s1 = Skill(skill_id = 3, skill_name = "Fast hands", skill_desc = "Get your hands moving", active = 0)
        db.session.add(self.s1)
        db.session.commit()
        
        response = self.client.get("/delete_skill/3&1&Fast hands")
        self.assertEqual(response.json, {
            'code': 200,
            'message': 'Fast hands has been toggled to active'
            })
        pass
    
    def test_delete_skill_inactive(self):
        self.s1 = Skill(skill_id = 3, skill_name = "Fast hands", skill_desc = "Get your hands moving", active = 1)
        db.session.add(self.s1)
        db.session.commit()
        
        response = self.client.get("/delete_skill/3&0&Fast hands")
        self.assertEqual(response.json, {
            'code': 200,
            'message': 'Fast hands has been toggled to inactive'
            })
        pass
    
    def test_get_all_skills_and_courses_hr_active(self):
        self.s1 = Skill(skill_id = 3, skill_name = "Fast hands", skill_desc = "Get your hands moving", active = 1)
        self.c1 = Course(course_id = "COR002", course_name = "Wiring 101", course_desc = "Handling wiring for engineers", course_status = "Active", course_type = "External", course_category = "Technical")    
        self.as1 = Attached_skill(skill_id = 3,course_id = 'COR002')
        db.session.add_all([self.s1, self.c1, self.as1])
        db.session.commit()
        self.maxDiff = None
        response = self.client.get("get_all_skills_and_courses_hr")
        self.assertEqual(response.json, {
            'data': {
                'skills': [{
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
                    'skill_name': 'Fast hands'}]}
        })
        
    def test_get_all_skills_and_courses_hr_inactive(self):
        self.s1 = Skill(skill_id = 3, skill_name = "Fast hands", skill_desc = "Get your hands moving", active = 0)
        self.c1 = Course(course_id = "COR002", course_name = "Wiring 101", course_desc = "Handling wiring for engineers", course_status = "Active", course_type = "External", course_category = "Technical")    
        self.as1 = Attached_skill(skill_id = 3,course_id = 'COR002')
        db.session.add_all([self.s1, self.c1, self.as1])
        db.session.commit()
        self.maxDiff = None
        response = self.client.get("get_all_skills_and_courses_hr")
        self.assertEqual(response.json, {
            'data': {
                'skills': [{
                    'active': 0,
                    'courses': [{
                        'course_category': 'Technical',
                        'course_desc': 'Handling wiring for engineers',
                        'course_id': 'COR002',
                        'course_name': 'Wiring 101',
                        'course_status': 'Active',
                        'course_type': 'External'}],
                    'skill_desc': 'Get your hands moving',
                    'skill_id': 3,
                    'skill_name': 'Fast hands'}]}
        })
        
    def test_edit_skill_details(self):
        self.s1 = Skill(skill_id = 3, skill_name = "Fast hands", skill_desc = "Get your hands moving", active = 1)
        db.session.add(self.s1)
        db.session.commit()
        request_body = {
                "skill_id": 3,
                "new_skill_name": "Quickest hands",
                "new_skill_desc": "Have the most fasty fast hands"
            }

        response = self.client.post("/edit_skill_details",
                                data=json.dumps(request_body),
                                content_type='application/json')
        self.assertEqual(response.json, {
            "data": {
                "message": "Skill name and description has been updated successfully"
                }
        })
        pass
        
class TestLearningJourney(TestApp):
    def test_create_lj(self):
        self.lj1 = Learning_journey(journey_id = 1, ljpsr_id = 1, staff_id= 140001, status = 1)
        self.st1 = Staff(staff_id = 140001, role_id = 2, staff_fname = "Kelvin", staff_lname = "Yap", dept = "Sales", email = "kelvin.yap.2020@scis.smu.edu.sg")
        self.ljpsr1 = Ljps_role(ljpsr_id = 1, role_title = "Engineer", role_desc = "Be an Engineer", active = 1)
        self.c1 = Course(course_id = "COR002", course_name = "Wiring 101", course_desc = "Handling wiring for engineers", course_status = "Active", course_type = "External", course_category = "Technical")   
        self.s1 = Skill(skill_id = 3, skill_name = "Fast hands", skill_desc = "Get your hands moving", active = 1)
        db.session.add_all([self.lj1, self.ljpsr1, self.st1, self.c1, self.s1])
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
    
    # ROUTE NOT IN USE
    
    # def test_add_course(self):
    #     self.lj1 = Learning_journey(journey_id = 1, ljpsr_id = 1, staff_id= 140001, status = 1)
    #     self.c1 = Course(course_id = "COR002", course_name = "Wiring 101", course_desc = "Handling wiring for engineers", course_status = "Active", course_type = "External", course_category = "Technical")    
    #     self.c2 = Course(course_id = "COR003", course_name = "Motherboards 101", course_desc = "Learn how to fix motherboards", course_status = "Active", course_type = "External", course_category = "Technical")    
    #     self.ljc1 = Lj_course(journey_id = 1, course_id = "COR002")
    #     db.session.add_all([self.ljc1, self.c1, self.c2, self.lj1])
    #     db.session.commit()
    #     request_body = {
    #             "courses": ["COR003"]
    #         }
    #     response = self.client.post("/add_course/1",
    #                             data=json.dumps(request_body),
    #                             content_type='application/json')
    #     self.assertEqual(response.json, {

    #     })
    #     pass
    
    def test_edit_LJ_courses(self):
        self.lj1 = Learning_journey(journey_id = 1, ljpsr_id = 1, staff_id= 140001, status = 1)
        self.ljc1 = Lj_course(journey_id = 1, course_id = "COR002")
        self.c1 = Course(course_id = "COR002", course_name = "Wiring 101", course_desc = "Handling wiring for engineers", course_status = "Active", course_type = "External", course_category = "Technical")    
        db.session.add_all([self.lj1, self.ljc1, self.c1])
        db.session.commit()
        
        request_body = {
            "journey_id": 1,
            "course_arr": json.dumps({'Fast Hands':[{'course_id':'COR002','course_name':'Wiring 101'}]})
        }

        response = self.client.post("/edit_LJ_courses/",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.json, request_body)
        pass
    
    def test_delete_LJ(self):
        self.lj1 = Learning_journey(journey_id = 1, ljpsr_id = 1, staff_id= 140001, status = 1)
        self.ljc1 = Lj_course(journey_id = 1, course_id = "COR002")
        self.c1 = Course(course_id = "COR002", course_name = "Wiring 101", course_desc = "Handling wiring for engineers", course_status = "Active", course_type = "External", course_category = "Technical")
            
        db.session.add_all([self.lj1, self.ljc1, self.c1])
        db.session.commit()

        request_body = {
            "journey_id": 1,
        }
        
        response = self.client.delete("/delete_LJ/",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.json, {
            "message": "Learning Journey deleted successfully"
        }) 
        
    
    
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

class TestAttachedSkill(TestApp):
    def test_add_course_to_skill(self):
        self.s1 = Skill(skill_id = 3, skill_name = "Fast hands", skill_desc = "Get your hands moving", active = 1)
        self.c1 = Course(course_id = "COR002", course_name = "Wiring 101", course_desc = "Handling wiring for engineers", course_status = "Active", course_type = "External", course_category = "Technical")    
        db.session.add_all([self.s1, self.c1])
        db.session.commit()
        
        request_body = {
            "skill_id": 3,
            "course_arr": ["COR002"]
            }

        response = self.client.post("/add_course_to_skill",
                                data=json.dumps(request_body),
                                content_type='application/json')
        self.assertEqual(response.json, {
            'code': 201,
            'data': {
                'courses': ['COR002'],
                'skill_id': 3
                },
            'message': 'Courses added successfully'
        })
        
    def test_add_course_to_skill_existing(self):
        self.s1 = Skill(skill_id = 3, skill_name = "Fast hands", skill_desc = "Get your hands moving", active = 1)
        self.c1 = Course(course_id = "COR002", course_name = "Wiring 101", course_desc = "Handling wiring for engineers", course_status = "Active", course_type = "External", course_category = "Technical")    
        self.as1 = Attached_skill(skill_id = 3,course_id = 'COR002')
        db.session.add_all([self.s1, self.c1, self.as1])
        db.session.commit()
        
        request_body = {
            "skill_id": 3,
            "course_arr": ["COR002"]
            }

        response = self.client.post("/add_course_to_skill",
                                data=json.dumps(request_body),
                                content_type='application/json')
        self.assertEqual(response.json, {
            'code': 400,
            'message': 'You are adding 1 or more duplicate course(s)'
        })

    def test_remove_course_from_skill(self):
        self.s1 = Skill(skill_id = 3, skill_name = "Fast hands", skill_desc = "Get your hands moving", active = 1)
        self.c1 = Course(course_id = "COR002", course_name = "Wiring 101", course_desc = "Handling wiring for engineers", course_status = "Active", course_type = "External", course_category = "Technical")    
        self.c2 = Course(course_id = "COR003", course_name = "Motherboards 101", course_desc = "Learn how to fix motherboards", course_status = "Active", course_type = "External", course_category = "Technical")    
        self.as1 = Attached_skill(skill_id = 3,course_id = 'COR002')
        self.as2 = Attached_skill(skill_id = 3,course_id = 'COR003')
        db.session.add_all([self.s1, self.c1, self.c2, self.as1, self.as2])
        db.session.commit()
        request_body = {
            "skill_id": 3,
            "course_arr": ["COR002"]
            }

        response = self.client.post("/remove_course_from_skill",
                                data=json.dumps(request_body),
                                content_type='application/json')
        self.assertEqual(response.json, {
            'code': 201,
            'data': {
                'courses': ['COR002'],
                'skill_id': 3},
            'message': 'Courses removed successfully'
        })
        
    def test_remove_course_from_skill_invalid(self):
        self.s1 = Skill(skill_id = 3, skill_name = "Fast hands", skill_desc = "Get your hands moving", active = 1)
        self.c1 = Course(course_id = "COR002", course_name = "Wiring 101", course_desc = "Handling wiring for engineers", course_status = "Active", course_type = "External", course_category = "Technical")    
        self.c2 = Course(course_id = "COR003", course_name = "Motherboards 101", course_desc = "Learn how to fix motherboards", course_status = "Active", course_type = "External", course_category = "Technical")    
        self.as1 = Attached_skill(skill_id = 3,course_id = 'COR002')
        self.as2 = Attached_skill(skill_id = 3,course_id = 'COR003')
        db.session.add_all([self.s1, self.c1, self.c2, self.as1, self.as2])
        db.session.commit()
        request_body = {
            "skill_id": 3,
            "course_arr": ["COR002", "COR003"]
            }

        response = self.client.post("/remove_course_from_skill",
                                data=json.dumps(request_body),
                                content_type='application/json')
        self.assertEqual(response.json, {
            'code': 400,
            'message': 'You are removing all courses from the skill'
        })
        
    def test_get_attained_skills(self):
        self.st1 = Staff(staff_id = 140001, role_id = 2, staff_fname = "Kelvin", staff_lname = "Yap", dept = "Sales", email = "kelvin.yap.2020@scis.smu.edu.sg")
        self.r1 = Registration(reg_id = 1, course_id = 'COR002', staff_id = 140001, reg_status = 'Registered', completion_status = "Completed")
        self.as1 = Attached_skill(skill_id = 3,course_id = 'COR002')
        self.s1 = Skill(skill_id = 3, skill_name = "Fast hands", skill_desc = "Get your hands moving", active = 1)
        
        db.session.add_all([self.st1, self.r1, self.as1, self.s1])
        db.session.commit()
        
        response = self.client.get("/get_attained_skills_of_staff/140001")
        self.assertEqual(response.json, {
            'data': {
                'attained_skills': [{
                    'active': 1,
                    'skill_desc': 'Get your hands moving',
                    'skill_id': 3,
                    'skill_name': 'Fast hands'}],
                'staff_details': {
                    'dept': 'Sales',
                    'email': 'kelvin.yap.2020@scis.smu.edu.sg',
                    'role_id': 2,
                    'staff_fname': 'Kelvin',
                    'staff_id': 140001,
                    'staff_lname': 'Yap'}}
        })

    def test_get_attained_skills_invalid(self):
        self.as1 = Attached_skill(skill_id = 3,course_id = 'COR002')
        self.s1 = Skill(skill_id = 3, skill_name = "Fast hands", skill_desc = "Get your hands moving", active = 1)
        
        db.session.add_all([self.as1, self.s1])
        db.session.commit()
        
        response = self.client.get("/get_attained_skills_of_staff/140001")
        self.assertEqual(response.json, {
            "error_code": 400,
            "error_message": "Staff ID does not exist"
        })
    
class TestRegistration(TestApp):
    def test_get_ongoing_course_of_staff(self):
        self.st1 = Staff(staff_id = 140001, role_id = 2, staff_fname = "Kelvin", staff_lname = "Yap", dept = "Sales", email = "kelvin.yap.2020@scis.smu.edu.sg")
        self.r1 = Registration(reg_id = 1, course_id = 'COR002', staff_id = 140001, reg_status = 'Registered', completion_status = "OnGoing")
        self.c1 = Course(course_id = "COR002", course_name = "Wiring 101", course_desc = "Handling wiring for engineers", course_status = "Active", course_type = "External", course_category = "Technical")    
        db.session.add_all([self.st1, self.r1, self.c1])
        db.session.commit()
        
        response = self.client.get("get_ongoing_course_of_staff/140001")
        self.assertEqual(response.json, {
            'ongoing_courses': [{
                'course_category': 'Technical',
                'course_desc': 'Handling wiring for engineers',
                'course_id': 'COR002',
                'course_name': 'Wiring 101',
                'course_status': 'Active',
                'course_type': 'External'}],
            'staff_details': {
                'dept': 'Sales',
                'email': 'kelvin.yap.2020@scis.smu.edu.sg',
                'role_id': 2,
                'staff_fname': 'Kelvin',
                'staff_id': 140001,
                'staff_lname': 'Yap'}
        })
        
    def test_get_ongoing_course_of_staff_invalid(self):
        self.c1 = Course(course_id = "COR002", course_name = "Wiring 101", course_desc = "Handling wiring for engineers", course_status = "Active", course_type = "External", course_category = "Technical")    
        db.session.add_all([self.c1])
        db.session.commit()
        
        response = self.client.get("get_ongoing_course_of_staff/140001")
        self.assertEqual(response.json, {
            'error_code': 400,
            'error_message': 'Staff ID does not exist'
        })
        
    def test_in_progress_skills_of_staff(self):
        self.st1 = Staff(staff_id = 140001, role_id = 2, staff_fname = "Kelvin", staff_lname = "Yap", dept = "Sales", email = "kelvin.yap.2020@scis.smu.edu.sg")
        self.r1 = Registration(reg_id = 1, course_id = 'COR002', staff_id = 140001, reg_status = 'Registered', completion_status = "OnGoing")
        self.as1 = Attached_skill(skill_id = 3,course_id = 'COR002')
        self.s1 = Skill(skill_id = 3, skill_name = "Fast hands", skill_desc = "Get your hands moving", active = 1)

        db.session.add_all([self.st1, self.r1, self.as1, self.s1])
        db.session.commit()
        
        response = self.client.get("/get_in_progress_skills_of_staff/140001")
        self.assertEqual(response.json, {
            'data': {
                'in_progress_skills': [{
                    'active': 1,
                    'skill_desc': 'Get your hands moving',
                    'skill_id': 3,
                    'skill_name': 'Fast hands'}],
                'staff_details': {
                    'dept': 'Sales',
                    'email': 'kelvin.yap.2020@scis.smu.edu.sg',
                    'role_id': 2,
                    'staff_fname': 'Kelvin',
                    'staff_id': 140001,
                    'staff_lname': 'Yap'}}
        })
    
    def test_in_progress_skills_of_staff_invalid(self):
        self.as1 = Attached_skill(skill_id = 3,course_id = 'COR002')
        self.s1 = Skill(skill_id = 3, skill_name = "Fast hands", skill_desc = "Get your hands moving", active = 1)

        db.session.add_all([self.as1, self.s1])
        db.session.commit()
        
        response = self.client.get("/get_in_progress_skills_of_staff/140001")
        self.assertEqual(response.json, {
            "error_code": 400,
            "error_message": "Staff ID does not exist"
        })
        
    def test_get_personal_attained_skills_completed(self):
        self.st1 = Staff(staff_id = 140001, role_id = 2, staff_fname = "Kelvin", staff_lname = "Yap", dept = "Sales", email = "kelvin.yap.2020@scis.smu.edu.sg")
        self.r1 = Registration(reg_id = 1, course_id = 'COR002', staff_id = 140001, reg_status = 'Registered', completion_status = "Completed")
        self.as1 = Attached_skill(skill_id = 3,course_id = 'COR002')
        self.s1 = Skill(skill_id = 3, skill_name = "Fast hands", skill_desc = "Get your hands moving", active = 1)
        
        db.session.add_all([self.st1, self.r1, self.as1, self.s1])
        db.session.commit()
        
        response = self.client.get("/get_personal_attained_skills/140001")
        self.assertEqual(response.json, {
            'data': {
                'completed_skills': [{
                    'active': 1,
                    'skill_desc': 'Get your hands moving',
                    'skill_id': 3,
                    'skill_name': 'Fast hands'}],
                'staff_details': {
                    'dept': 'Sales',
                    'email': 'kelvin.yap.2020@scis.smu.edu.sg',
                    'role_id': 2,
                    'staff_fname': 'Kelvin',
                    'staff_id': 140001,
                    'staff_lname': 'Yap'}}
        })
    
    def test_get_personal_attained_skills_ongoing(self):
        self.st1 = Staff(staff_id = 140001, role_id = 2, staff_fname = "Kelvin", staff_lname = "Yap", dept = "Sales", email = "kelvin.yap.2020@scis.smu.edu.sg")
        self.r1 = Registration(reg_id = 1, course_id = 'COR002', staff_id = 140001, reg_status = 'Registered', completion_status = "OnGoing")
        self.as1 = Attached_skill(skill_id = 3,course_id = 'COR002')
        self.s1 = Skill(skill_id = 3, skill_name = "Fast hands", skill_desc = "Get your hands moving", active = 1)
        
        db.session.add_all([self.st1, self.r1, self.as1, self.s1])
        db.session.commit()
        
        response = self.client.get("/get_personal_attained_skills/140001")
        self.assertEqual(response.json, {
            'data': {
                'completed_skills': [],
                'staff_details': {
                    'dept': 'Sales',
                    'email': 'kelvin.yap.2020@scis.smu.edu.sg',
                    'role_id': 2,
                    'staff_fname': 'Kelvin',
                    'staff_id': 140001,
                    'staff_lname': 'Yap'}}
        })
        
    def test_get_personal_attained_skills_none(self):
        self.st1 = Staff(staff_id = 140001, role_id = 2, staff_fname = "Kelvin", staff_lname = "Yap", dept = "Sales", email = "kelvin.yap.2020@scis.smu.edu.sg")
        self.as1 = Attached_skill(skill_id = 3,course_id = 'COR002')
        self.s1 = Skill(skill_id = 3, skill_name = "Fast hands", skill_desc = "Get your hands moving", active = 1)
        
        db.session.add_all([self.st1, self.as1, self.s1])
        db.session.commit()
        
        response = self.client.get("/get_personal_attained_skills/140001")
        self.assertEqual(response.json, {
            'data': {
                'completed_skills': [],
                'staff_details': {
                    'dept': 'Sales',
                    'email': 'kelvin.yap.2020@scis.smu.edu.sg',
                    'role_id': 2,
                    'staff_fname': 'Kelvin',
                    'staff_id': 140001,
                    'staff_lname': 'Yap'}}
        })
        
    def test_get_personal_attained_skills_invalid(self):
        self.as1 = Attached_skill(skill_id = 3,course_id = 'COR002')
        self.s1 = Skill(skill_id = 3, skill_name = "Fast hands", skill_desc = "Get your hands moving", active = 1)
        
        db.session.add_all([self.as1, self.s1])
        db.session.commit()
        
        response = self.client.get("/get_personal_attained_skills/140001")
        self.assertEqual(response.json, {
            "code": 400, 
            "message": 'Staff ID does not exists.'
        })
        
    def test_get_completed_course_of_staff_completed(self):
        self.st1 = Staff(staff_id = 140001, role_id = 2, staff_fname = "Kelvin", staff_lname = "Yap", dept = "Sales", email = "kelvin.yap.2020@scis.smu.edu.sg")
        self.r1 = Registration(reg_id = 1, course_id = 'COR002', staff_id = 140001, reg_status = 'Registered', completion_status = "Completed")
        self.c1 = Course(course_id = "COR002", course_name = "Wiring 101", course_desc = "Handling wiring for engineers", course_status = "Active", course_type = "External", course_category = "Technical")
        
        db.session.add_all([self.st1, self.r1, self.c1])
        db.session.commit()
        
        response = self.client.get("/get_completed_course_of_staff/140001")
        self.assertEqual(response.json, {
            'completed_courses': [{
                'course_category': 'Technical',
                'course_desc': 'Handling wiring for engineers',
                'course_id': 'COR002',
                'course_name': 'Wiring 101',
                'course_status': 'Active',
                'course_type': 'External'}],
            'staff_details': {
                'dept': 'Sales',
                'email': 'kelvin.yap.2020@scis.smu.edu.sg',
                'role_id': 2,
                'staff_fname': 'Kelvin',
                'staff_id': 140001,
                'staff_lname': 'Yap'}
        })
    
    def test_get_completed_course_of_staff_ongoing(self):
        self.st1 = Staff(staff_id = 140001, role_id = 2, staff_fname = "Kelvin", staff_lname = "Yap", dept = "Sales", email = "kelvin.yap.2020@scis.smu.edu.sg")
        self.r1 = Registration(reg_id = 1, course_id = 'COR002', staff_id = 140001, reg_status = 'Registered', completion_status = "OnGoing")
        self.c1 = Course(course_id = "COR002", course_name = "Wiring 101", course_desc = "Handling wiring for engineers", course_status = "Active", course_type = "External", course_category = "Technical")
        
        db.session.add_all([self.st1, self.r1, self.c1])
        db.session.commit()
        
        response = self.client.get("/get_completed_course_of_staff/140001")
        self.assertEqual(response.json, {
            'completed_courses': [],
            'staff_details': {
                'dept': 'Sales',
                'email': 'kelvin.yap.2020@scis.smu.edu.sg',
                'role_id': 2,
                'staff_fname': 'Kelvin',
                'staff_id': 140001,
                'staff_lname': 'Yap'}
        })
    
    def test_get_completed_course_of_staff_invalid(self):
        self.c1 = Course(course_id = "COR002", course_name = "Wiring 101", course_desc = "Handling wiring for engineers", course_status = "Active", course_type = "External", course_category = "Technical")
        
        db.session.add_all([self.c1])
        db.session.commit()
        
        response = self.client.get("/get_completed_course_of_staff/140001")
        self.assertEqual(response.json, {
            "error_code": 400,
            "error_message": "Staff ID does not exist"
        })
    
if __name__ == "__main__":
    unittest.main()  