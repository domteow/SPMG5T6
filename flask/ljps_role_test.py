import unittest
import flask_testing
import json
from ljps_role import Ljps_role
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
        self.ljr1 = Ljps_role(ljpsr_id = 1, role_title = 'Technician', role_desc = 'On site and off site trouble shooting of printer machines.', active = 1)
        self.ljr2 = Ljps_role(ljpsr_id = 2, role_title = 'Manager', role_desc = 'Maintains staff by recruiting selecting orienting and training employees. Ensures a safe secure and legal work environment. Develops personal growth opportunities. Accomplishes staff results by communicating job expectations; planning monitoring and appraising job results.', active = 1)
        self.ljr3 = Ljps_role(ljpsr_id = 4, role_title = 'Cybersecurity Administrator', role_desc = "A security administrator installs administers and troubleshoots an organization's security solutions.", active = 1)
        db.session.add(self.ljr1)
        db.session.add(self.ljr2)
        db.session.add(self.ljr3)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_to_dict(self):
        self.assertEqual(self.ljr1.to_dict(), {
            "ljpsr_id": 1,
            "role_title": 'Technician',
            "role_desc": 'On site and off site trouble shooting of printer machines.',
            "active": 1
        })
    
    def test_get_learning_journey_role_by_id(self):
        self.assertEqual(Ljps_role.get_learning_journey_role_by_id(1),  {
            "ljpsr_id": 1,
            "role_title": 'Technician',
            "role_desc": 'On site and off site trouble shooting of printer machines.',
            "active": 1
        })
    
    def test_check_learning_journey_role_exists(self):
        self.assertEqual(Ljps_role.check_learning_journey_role_exists("Technician"),True)
    
    def test_get_all_learning_journey_roles(self):
        self.assertEqual(Ljps_role.get_all_learning_journey_roles(),[
            {
            "ljpsr_id": 1,
            "role_title": 'Technician',
            "role_desc": 'On site and off site trouble shooting of printer machines.',
            "active": 1
        },
        {
            "ljpsr_id": 2,
            "role_title": 'Manager',
            "role_desc": 'Maintains staff by recruiting selecting orienting and training employees. Ensures a safe secure and legal work environment. Develops personal growth opportunities. Accomplishes staff results by communicating job expectations; planning monitoring and appraising job results.',
            "active": 1
        },
        {
            "ljpsr_id": 4,
            "role_title": 'Cybersecurity Administrator',
            "role_desc": "A security administrator installs administers and troubleshoots an organization's security solutions.",
            "active": 1
        }
        ])

    def test_create_learning_journey_role(self):
        self.assertEqual(Ljps_role.create_learning_journey_role(5,"Business Analyst","To ensure business efficiency increases through their knowledge of both IT and business function."),True)
    
    def test_toggle_active(self):
        self.assertEqual(Ljps_role.toggle_active(1,0),True)
    
    def test_get_all_learning_journey_roles(self):
        self.assertEqual(Ljps_role.get_all_learning_journey_roles(),[
        {
            "ljpsr_id": 1,
            "role_title": 'Technician',
            "role_desc": 'On site and off site trouble shooting of printer machines.',
            "active": 1
        },
        {
            "ljpsr_id": 2,
            "role_title": 'Manager',
            "role_desc": 'Maintains staff by recruiting selecting orienting and training employees. Ensures a safe secure and legal work environment. Develops personal growth opportunities. Accomplishes staff results by communicating job expectations; planning monitoring and appraising job results.',
            "active": 1
        },
        {
            "ljpsr_id": 4,
            "role_title": 'Cybersecurity Administrator',
            "role_desc": "A security administrator installs administers and troubleshoots an organization's security solutions.",
            "active": 1
        }
        ])
    
    def test_edit_details(self):
        self.assertEqual(Ljps_role.edit_details(1,"Technician2","On site and off site trouble shooting of printer machines and more."),True)

if __name__ == "__main__":
    unittest.main()  