from initdb import db

from ljps_role import Ljps_role
from skill import Skill
from flask import Flask, request, jsonify




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

    def delete_ljps_skill(ljpsr_id, skill_id):
        role_link_skill = Role_required_skill.query.filter_by(ljpsr_id=ljpsr_id,skill_id=skill_id).first()
        if role_link_skill:
            try:
                db.session.delete(role_link_skill)
                db.session.commit()
                return True
            except Exception:
                return False
        return False


    #Add skill to role
    def create_new_role_required_skill(skill_id, ljpsr_id):
        new_role_required_skill = Role_required_skill(ljpsr_id, skill_id)
        try:
            db.session.add(new_role_required_skill)
            db.session.commit()
        except:
            return False
        
        return True


