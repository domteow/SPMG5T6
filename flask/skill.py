from initdb import db
from flask import Flask, request, jsonify


class Skill(db.Model):
    __tablename__ = 'skill'

    skill_id = db.Column(db.Integer, primary_key=True, nullable=False)
    skill_name = db.Column(db.String(50))
    skill_desc = db.Column(db.String(255))
    active = db.Column(db.Integer, nullable=False)


    def __init__(self, skill_id, skill_name, skill_desc, active):
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

    def get_all_skills_active():
        skills = Skill.query.filter_by(active=1).all()
        if skills:
            return [skill.to_dict() for skill in skills]
        else:
            return None

    def get_active_skills_list(skills_under_ljpsr):
        active_skills = []

        for skill_id in skills_under_ljpsr: 
            active_skill = Skill.query.filter_by(skill_id=skill_id).first()

            if active_skill.active == 1: 
                active_skills.append(active_skill.skill_id)

        return active_skills

    def check_skill_exists(skill_name):
        check = Skill.query.filter_by(skill_name=skill_name).first()

        return check 

    def create_skill(skill_id, skill_name, skill_desc, active):
        new_skill = Skill(skill_id, skill_name, skill_desc, active)

        try: 
            db.session.add(new_skill)
            db.session.commit()
        
        except:
            return False
        
        return True

    def toggle_active(skill_id, isactive):
        skill = Skill.query.filter_by(skill_id=skill_id).first()
        skill.active = isactive

        try:
            db.session.commit()
        except:
            return False
        return True
