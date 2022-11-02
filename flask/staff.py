from initdb import db
from flask import Flask, request, jsonify
from role import Role



class Staff(db.Model):
    __tablename__ = 'staff'

    staff_id = db.Column(db.Integer, primary_key=True, nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey(Role.role_id))
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
    
    def get_staff_from_department(dept):
        staffs = Staff.query.filter_by(dept=dept).all()
        if len(staffs):
            return [staff.to_dict() for staff in staffs]
        else:
            return None
    
    def get_all_staff():
        staffs = Staff.query.all()
        if len(staffs):
            return [staff.to_dict() for staff in staffs]
        else:
            return None