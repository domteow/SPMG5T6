import unittest
import flask_testing
import json
from role import Role
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
        self.r1 = Role(role_id = 2, role_name = "User")
        db.session.add(self.r1)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_to_dict(self):
        self.assertEqual(self.r1.to_dict(), {
            "role_id": 2,
            "role_name": "User"
        })
    
    def test_get_role_by_id(self):
        self.assertEqual(Role.get_role_by_id(2),  {
            "role_id": 2,
            "role_name": "User"
        })
    
    

if __name__ == "__main__":
    unittest.main()  