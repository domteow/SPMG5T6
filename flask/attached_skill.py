from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from skill import Skill
from course import Course


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

class Attached_skill(db.Model):
    __tablename__ = 'attached_skill'

    course_id = db.Column(db.String(20), db.ForeignKey('Course.course_id'), primary_key=True,
    nullable = False)
    skill_id = db.Column(db.Integer, db.ForeignKey('Skill.skill_id'), primary_key=True,
    nullable = False)

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

    def get_attached_skill_by_skill_id(skill_id):
        attached_skill = Attached_skill.query.filter_by(skill_id=skill_id).all()
        if len(attached_skill):
            return [atts.to_dict() for atts in attached_skill]
        else:
            return []