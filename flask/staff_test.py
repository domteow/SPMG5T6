import unittest
import flask_testing
import json
from staff import Staff, db
from app import app


class TestStaff(flask_testing.TestCase):
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {}
    app.config['TESTING'] = True
    def create_app(self):
        return app

    def setUp(self):
        db.create_all()
        self.s1 = Staff(staff_id = 130001, staff_fname = 'John', staff_lname = 'Sim', dept = 'Chariman', email = 'jack.sim@allinone.com.sg', role_id = 1)
        db.session.add(self.s1)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_to_dict(self):
        # s1 = Staff(staff_id = 130001, staff_fname = 'John', staff_lname = 'Sim', dept = 'Chariman', email = 'jack.sim@allinone.com.sg', role_id = 1)
        self.assertEqual(self.s1.to_dict(), {
            "staff_id": 130001,
            "staff_fname": 'John',
            "staff_lname": 'Sim',
            "dept": 'Chariman',
            "email": 'jack.sim@allinone.com.sg',
            "role_id": 1
        })
    
    def test_get_staff_by_id(self):
        self.assertEqual(Staff.get_staff_by_id(130001),  {
            "staff_id": 130001,
            "staff_fname": 'John',
            "staff_lname": 'Sim',
            "dept": 'Chariman',
            "email": 'jack.sim@allinone.com.sg',
            "role_id": 1
        })
    def test_get_staff_from_department(self):
        pass

if __name__ == "__main__":
    unittest.main()  