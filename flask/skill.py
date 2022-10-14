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

class Skill(db.Model):
    __tablename__ = 'skill'

    skill_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    skill_name = db.Column(db.String(50))
    skill_desc = db.Column(db.String(255))
    active = db.Column(db.Integer)

    def __init__(self, skill_id, active, skill_name, skill_desc):
        self.skill_id = skill_id
        self.skill_name = skill_name
        self.skill_desc = skill_desc
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
    
    def get_skill_by_id(skill_id):
        skill = Skill.query.filter_by(skill_id=skill_id).first()
        if skill:
            return skill.to_dict()
        else:
            return None

    #get all skills 
    def get_all_skills():
        skills = Skill.query.all()
        if skills:
            return [skill.to_dict() for skill in skills]
        else:
            return None
