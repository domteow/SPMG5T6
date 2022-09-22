from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root' + \
                                        '@localhost:3306/is212'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_size': 100,
                                           'pool_recycle': 280}

db = SQLAlchemy(app)

CORS(app)

class Staff(db.Model):
    __tablename__ = 'staff'

    staff_id = db.Column(db.Integer, primary_key=True, nullable=False)
    role = db.Column(db.Integer)
    staff_fname = db.Column(db.String(50))
    staff_lname = db.Column(db.String(50))
    dept = db.Column(db.String(50))
    email = db.Column(db.String(50))

    def __init__(self, staff_id, role, staff_fname, staff_lname, dept, email):
        self.staff_id = staff_id
        self.role = role
        self.staff_fname = staff_fname
        self.staff_lname = staff_lname
        self.dept = dept
        self.email = email

    # __mapper_args__ = {
    #     'polymorphic_identity': 'staff'
    # }

    # def to_dict(self):
    #     """
    #     'to_dict' converts the object into a dictionary,
    #     in which the keys correspond to database columns
    #     """
    #     columns = self.__mapper__.column_attrs.keys()
    #     result = {}
    #     for column in columns:
    #         result[column] = getattr(self, column)
    #     return result

