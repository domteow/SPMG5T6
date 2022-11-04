import unittest
import flask_testing
import json
from initdb import db
from app import app
from learning_journey import Learning_journey

class TestLearning_journey(flask_testing.TestCase):
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {}
    app.config['TESTING'] = True
    def create_app(self):
        return app

    def setUp(self):
        db.create_all()
        self.lj1 = Learning_journey(journey_id = 1, ljpsr_id = 1, staff_id = 140001, status = 0)
        db.session.add(self.lj1)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()    
    

    def test_to_dict(self):

        self.assertEqual(self.lj1.to_dict(), {
            "journey_id" : 1,
            "ljpsr_id" : 1,
            "staff_id" : 140001,
            "status" : 0
        })

    def test_get_learning_journey_by_staff_id(self):
        self.assertEqual(Learning_journey.get_learning_journey_by_staff_id(staff_id=140001),
        [self.lj1.to_dict()])

    def test_get_learning_journey_role_by_id(self):
        self.assertEqual(Learning_journey.query.filter_by(journey_id=1).first().ljpsr_id
        , 1)

    def test_create_learning_journey(self):
        self.assertEqual(Learning_journey.create_learning_journey(journey_id = 2, ljpsr_id = 2, staff_id = 140002)
        ,True)

    def test_error_create_learning_journey(self):
        # Should not be able to create LJ with already existing journey_id
        self.assertEqual(Learning_journey.create_learning_journey(journey_id = 1, ljpsr_id = 8, staff_id = 140001)
        ,"Failed to create LJ")    

    def test_delete_learning_journey(self):
        self.assertEqual(Learning_journey.delete_learning_journey(1)
        ,True)

    def test_error_delete_learning_journey(self):
        # Should not be able to delete LJ that does not exist
        self.assertEqual(Learning_journey.delete_learning_journey(2)
        ,"Failed to delete LJ")

if __name__ == "__main__":
    unittest.main()  