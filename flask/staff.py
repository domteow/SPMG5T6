from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from role import Role

app = Flask(__name__)
import platform
my_os = platform.system()
if my_os == "Windows":
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root' + '@localhost:3306/all_in_one_db'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root' + '@localhost:3306/all_in_one_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_size': 100,
                                           'pool_recycle': 280}

db = SQLAlchemy(app)

CORS(app)

class Staff(db.Model):
    __tablename__ = 'staff'

    staff_id = db.Column(db.Integer, primary_key=True, nullable=False)
    role = db.Column(db.Integer, db.ForeignKey(Role.role_id))
    staff_fname = db.Column(db.String(50))
    staff_lname = db.Column(db.String(50))
    dept = db.Column(db.String(50))
    email = db.Column(db.String(50))

    # __mapper_args__ = {
    #     'polymorphic_identity': 'staff'
    # }

    def to_dict(self):
        """
        'to_dict' converts the object into a dictionary,
        in which the keys correspond to database columns
        """
        columns = self.__mapper__.column_attrs.keys()
        result = {}
        for column in columns:
            result[column] = getattr(self, column)
        return result

    def get_staff_by_id(staff_id):
        staff = Staff.query.filter_by(staff_id=staff_id).first()
        if staff:
            return staff.to_dict()
        else:
            return None