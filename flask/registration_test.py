import unittest
import flask_testing
import json
from registration import Registration
from initdb import db
from app import app


class TestStaff(flask_testing.TestCase):
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {}
    app.config['TESTING'] = True
    def create_app(self):
        return app

    def setUp(self):
        db.create_all()
        self.r1 = Registration(reg_id = 3, course_id = 'COR002', staff_id = 140001, reg_status = 'Registered', completion_status = 'Completed')
        self.r2 = Registration(reg_id = 111, course_id = 'SAL004', staff_id = 140001, reg_status = 'Registered', completion_status = 'Completed')
        self.r3 = Registration(reg_id = 200, course_id = 'MGT001', staff_id = 140001, reg_status = 'Registered', completion_status = 'Completed')

        self.r4 = Registration(reg_id = 114, course_id = 'SAL003', staff_id = 140004, reg_status = 'Registered', completion_status = 'OnGoing')

        self.r5 = Registration(reg_id = 203, course_id = 'COR002', staff_id = 140004, reg_status = 'Registered', completion_status = 'Completed')

        self.r6 = Registration(reg_id = 249, course_id = 'FIN003', staff_id = 140004, reg_status = 'Registered', completion_status = 'OnGoing')
        db.session.add(self.r1)
        db.session.add(self.r2)
        db.session.add(self.r3)
        db.session.add(self.r4)
        db.session.add(self.r5)
        db.session.add(self.r6)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_to_dict(self):
        self.assertEqual(self.r1.to_dict(), {
            "reg_id": 3,
            "course_id": "COR002",
            "staff_id": 140001,
            "reg_status": "Registered",
            "completion_status": "Completed"
        })
    
    def test_get_completed_courses_by_staff_id(self):
        self.assertEqual(Registration.get_completed_courses_by_staff_id(140001),  [
            "COR002",
            "SAL004",
            "MGT001"
        ])

    def test_get_ongoing_courses_by_staff_id(self):
        self.assertEqual(Registration.get_ongoing_courses_by_staff_id(140004),  [
            "SAL003",
            "FIN003"
        ])
    
    
    
    

if __name__ == "__main__":
    unittest.main()  