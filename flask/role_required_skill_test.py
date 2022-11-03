import unittest
import flask_testing
import json
from role_required_skill import Role_required_skill
from initdb import db
from app import app


class TestLjps_role(flask_testing.TestCase):
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {}
    app.config['TESTING'] = True
    def create_app(self):
        return app

    def setUp(self):
        db.create_all()
        self.rrs1 = Role_required_skill(skill_id = 1, ljpsr_id = 1)
        self.rrs2 = Role_required_skill(skill_id = 2, ljpsr_id = 1)
        self.rrs3 = Role_required_skill(skill_id = 22, ljpsr_id = 1)
        self.rrs4 = Role_required_skill(skill_id = 23, ljpsr_id = 1)
        self.rrs5 = Role_required_skill(skill_id = 24, ljpsr_id = 1)
        self.rrs6 = Role_required_skill(skill_id = 25, ljpsr_id = 1)
        self.rrs7 = Role_required_skill(skill_id = 4, ljpsr_id = 2)
        self.rrs8 = Role_required_skill(skill_id = 5, ljpsr_id = 2)
        self.rrs9 = Role_required_skill(skill_id = 12, ljpsr_id = 2)
        self.rrs10 = Role_required_skill(skill_id = 14, ljpsr_id = 2)
        self.rrs11 = Role_required_skill(skill_id = 15, ljpsr_id = 2)
        self.rrs12 = Role_required_skill(skill_id = 16, ljpsr_id = 2)
        self.rrs13 = Role_required_skill(skill_id = 20, ljpsr_id = 2)
        self.rrs14 = Role_required_skill(skill_id = 1, ljpsr_id = 4)
        self.rrs15 = Role_required_skill(skill_id = 2, ljpsr_id = 4)
        self.rrs16 = Role_required_skill(skill_id = 10, ljpsr_id = 4)
        self.rrs17 = Role_required_skill(skill_id = 33, ljpsr_id = 4)
        self.rrs18 = Role_required_skill(skill_id = 34, ljpsr_id = 4)
        db.session.add(self.rrs1)
        db.session.add(self.rrs2)
        db.session.add(self.rrs3)
        db.session.add(self.rrs4)
        db.session.add(self.rrs5)
        db.session.add(self.rrs6)
        db.session.add(self.rrs7)
        db.session.add(self.rrs8)
        db.session.add(self.rrs9)
        db.session.add(self.rrs10)
        db.session.add(self.rrs11)
        db.session.add(self.rrs12)
        db.session.add(self.rrs13)
        db.session.add(self.rrs14)
        db.session.add(self.rrs15)
        db.session.add(self.rrs16)
        db.session.add(self.rrs17)
        db.session.add(self.rrs18)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_to_dict(self):
        self.assertEqual(self.rrs1.to_dict(), {
            "skill_id": 1,
            "ljpsr_id": 1
        })
    
    def test_get_role_require_skill_by_ljpsr(self):
        self.assertEqual(Role_required_skill.get_role_require_skill_by_ljpsr(1),  [
        {
            "skill_id": 1,
            "ljpsr_id": 1
        },
        {
            "skill_id": 2,
            "ljpsr_id": 1
        },
        {
            "skill_id": 22,
            "ljpsr_id": 1
        },
        {
            "skill_id": 23,
            "ljpsr_id": 1
        },
        {
            "skill_id": 24,
            "ljpsr_id": 1
        },
        {
            "skill_id": 25,
            "ljpsr_id": 1
        }
        ])
    
    def test_get_role_require_skill_by_ljpsr_list(self):
        self.assertEqual(Role_required_skill.get_role_require_skill_by_ljpsr_list(1), [1,2,22,23,24,25])

    def test_delete_ljps_skill(self):
        self.assertEqual(Role_required_skill.delete_ljps_skill(1,1),True)
    
    def test_create_new_role_required_skill(self):
        self.assertEqual(Role_required_skill.create_new_role_required_skill(3,1),True)

if __name__ == "__main__":
    unittest.main()  