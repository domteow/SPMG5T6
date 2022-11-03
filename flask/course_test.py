import unittest
import flask_testing
import json
from course import Course
from initdb import db
from app import app


class TestCourse(flask_testing.TestCase):
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {}
    app.config['TESTING'] = True
    def create_app(self):
        return app

    def setUp(self):
        db.create_all()
        self.c1 = Course(course_id = "COR001", course_name = 'Systems Thinking and Design', course_desc = 'This foundation module aims to introduce students to the fundamental concepts and underlying principles of systems thinking', course_status = 'Active', course_type = 'Internal', course_category = 'Core')
        self.c2 = Course(course_id = "FIN001", course_name = 'Data Collection and Analysis', course_desc = 'Data is meaningless unless insights and analysis can be drawn to provide useful information for business decision-making. It is imperative that data quality integrity and security ', course_status = 'Active', course_type = 'External', course_category = 'Finance')
        self.c3 = Course(course_id = "MGT001", course_name = 'People Management', course_desc = 'enable learners to manage team performance and development through effective communication conflict resolution and negotiation skills.', course_status = 'Active', course_type = 'Internal', course_category = 'Management')
        db.session.add(self.c1)
        db.session.add(self.c2)
        db.session.add(self.c3)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_to_dict(self):
        self.assertEqual(self.c1.to_dict(), {
            "course_id": "COR001",
            "course_name": 'Systems Thinking and Design',
            "course_desc": 'This foundation module aims to introduce students to the fundamental concepts and underlying principles of systems thinking',
            "course_status": 'Active',
            "course_type": 'Internal',
            "course_category": "Core"
        })
    
    def test_get_course_by_id(self):
        self.assertEqual(Course.get_course_by_id("COR001"),  {
            "course_id": "COR001",
            "course_name": 'Systems Thinking and Design',
            "course_desc": 'This foundation module aims to introduce students to the fundamental concepts and underlying principles of systems thinking',
            "course_status": 'Active',
            "course_type": 'Internal',
            "course_category": "Core"
        })
    
    def test_get_all_courses(self):
        self.assertEqual(Course.get_all_courses(),[
            {
            "course_id": "COR001",
            "course_name": 'Systems Thinking and Design',
            "course_desc": 'This foundation module aims to introduce students to the fundamental concepts and underlying principles of systems thinking',
            "course_status": 'Active',
            "course_type": 'Internal',
            "course_category": "Core"
        },
        {
            "course_id": "FIN001",
            "course_name": 'Data Collection and Analysis',
            "course_desc": 'Data is meaningless unless insights and analysis can be drawn to provide useful information for business decision-making. It is imperative that data quality integrity and security ',
            "course_status": 'Active',
            "course_type": 'External',
            "course_category": "Finance"
        },
        {
            "course_id": "MGT001",
            "course_name": 'People Management',
            "course_desc": 'enable learners to manage team performance and development through effective communication conflict resolution and negotiation skills.',
            "course_status": 'Active',
            "course_type": 'Internal',
            "course_category": "Management"
        }
        ])

if __name__ == "__main__":
    unittest.main()  