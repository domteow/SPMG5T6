from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from ljps_role import Ljps_role
from skill import Skill

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


class Role_required_skill(db.Model):
    __tablename__ = 'role_required_skill'

    ljpsr_id = db.Column(db.Integer, db.ForeignKey(Ljps_role.ljpsr_id), primary_key=True)
    skill_id = db.Column(db.Integer,  db.ForeignKey(Skill.skill_id),primary_key=True)
    
    def __init__(self, ljpsr_id, skill_id):
        self.ljpsr_id = ljpsr_id
        self.skill_id = skill_id
    
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

    def get_role_require_skill_by_ljpsr(ljpsr_id):
        role_require_skill = Role_required_skill.query.filter_by(ljpsr_id=ljpsr_id).all()
        if len(role_require_skill):
            return [rrs.to_dict() for rrs in role_require_skill]
        else:
            return []

    def get_role_require_skill_by_ljpsr_list(ljpsr_id):
        skills = []
        role_require_skill = Role_required_skill.query.filter_by(ljpsr_id=ljpsr_id).all()

        if len(role_require_skill):
            for skill in role_require_skill:
                if skill.skill_id not in skills:
                    skills.append(skill.skill_id)

        return skills
    
    def create_ljps_skill(ljpsr_id, skill_id):
        new_ljps_skill = Role_required_skill(ljpsr_id,skill_id)
        try:
            db.session.add(new_ljps_skill)
            db.session.commit()
            return jsonify(new_ljps_skill.to_dict()), 201
        except Exception:
            # db.session.rollback()
            return jsonify({
                "message": "Unable to commit to database."
            }), 500
