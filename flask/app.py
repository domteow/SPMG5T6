from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from course import Course
from role import Role
from skill import Skill
from staff import Staff
from attached_skill import Attached_skill
from learning_journey import Learning_journey
from lj_course import Lj_course
from LJPS_role import Ljps_role
from registration import Registration
from role_required_skill import Role_required_skill


app = Flask(__name__)
#MAC OS
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root' + '@localhost:3306/all_in_one_db'
#Windows OS
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root' + '@localhost:3306/all_in_one_db'
                                        
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_size': 100,
                                           'pool_recycle': 280}

db = SQLAlchemy(app)

CORS(app)

db.create_all()

# Find COURSE by course_id
@app.route("/course/<string:course_id>")
def course_by_id(course_id):
    course = Course.query.filter_by(course_id=course_id).first()
    if course:
        return jsonify({
            "data": course.to_dict()
        }), 200
    else:
        return jsonify({
            "message": "course not found."
        }), 404



# Find learning journeys by staff_id
@app.route("/lj/<int:staff_id>")
def learning_journey_by_staff(staff_id):
    learning_journey = Learning_journey.query.filter_by(staff_id=staff_id).all()
    if len(learning_journey):
        return jsonify({
            "data": {
                    "learning_journey": [lj.to_dict() for lj in learning_journey]
                }
        }), 200
    else:
        return jsonify({
            "message": "Staff does not have any learning journeys."
        }), 404


# Find learning journey role from ljpsr_id
@app.route("/ljpsr/<int:ljpsr_id>")
def learning_journey_role_by_id(ljpsr_id):
    ljpsr = Ljps_role.query.filter_by(ljpsr_id=ljpsr_id).first()
    if ljpsr:
        return jsonify({
            "data": {
                    "ljpsr": ljpsr.to_dict()
                }
        }), 200
    else:
        return jsonify({
            "message": "Learning Journey Role does not exist."
        }), 404

# Find skill by skill_id
@app.route("/skill/<int:skill_id>")
def skill_by_id(skill_id):
    skill = Skill.query.filter_by(skill_id=skill_id).first()
    if skill:
        return jsonify({
            "data": {
                    "skill": skill.to_dict()
                }
        }), 200
    else:
        return jsonify({
            "message": "Skill not found."
        }), 404

# Find attached_skill by skill_id
@app.route("/attached_skill_by_skill/<int:skill_id>")
def attached_skill_by_skill(skill_id):
    attached_skill = Attached_skill.query.filter_by(skill_id=skill_id).all()
    if len(attached_skill):
        return jsonify({
            "data": {
                    "attached_skill": [atts.to_dict() for atts in attached_skill]
                }
        }), 200
    else:
        return jsonify({
            "message": "Skill not attached to any courses."
        }), 404


# Find lj_course by journey_id (need dummy data to retrieve the courses for learning journey)
@app.route("/lj_course_by_journey/<int:journey_id>")
def lj_course_by_journey(journey_id):
    lj_course = Lj_course.query.filter_by(journey_id=journey_id).all()
    if len(lj_course):
        return jsonify({
            "data": {
                    "lj_course": [ljc.to_dict() for ljc in lj_course]
                }
        }), 200
    else:
        return jsonify({
            "message": "Learning Journey contains no courses."
        }), 404

# @app.route("/path/<int:id>", methods = ['POST'])
# def addCourseToLJ(id):
#     course = Course.getCourseByID(id)
#     #to json
#     return #json


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
