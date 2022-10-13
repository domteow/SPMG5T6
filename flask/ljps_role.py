from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

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

class Ljps_role(db.Model):
    __tablename__ = 'ljps_role'

    ljpsr_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role_title = db.Column(db.String(50), nullable = False)
    role_desc = db.Column(db.String(255))
    active = db.Column(db.Integer, nullable=False)

    def __init__(self, ljpsr_id, role_title, role_desc, active):
        self.ljpsr_id = ljpsr_id
        self.role_title = role_title
        self.role_desc = role_desc
        self.active = active

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

    def get_learning_journey_role_by_id(ljpsr_id):
        ljpsr = Ljps_role.query.filter_by(ljpsr_id=ljpsr_id).first()
        if ljpsr:
            return ljpsr.to_dict()
        else:
            return None

    def check_learning_journey_role_exists(role_title):
        check = Ljps_role.query.filter_by(role_title=role_title).first()
        
        return check

    def get_all_learning_journey_roles():
        roles = Ljps_role.query.all()
        if roles:
            return [role.to_dict() for role in roles]
        else:
            return []

    #Create new active learning journey role and add to database
    def create_learning_journey_role(ljpsr_id, role_title, role_desc):
        new_ljps_role = Ljps_role(ljpsr_id, role_title, role_desc, 1)
        try:
            db.session.add(new_ljps_role)
            db.session.commit()

        except:
            return False

        return True
        