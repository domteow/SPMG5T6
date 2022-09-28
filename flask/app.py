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
from ljps_role import Ljps_role
from registration import Registration
from role_required_skill import Role_required_skill

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

db.create_all()

# @app.route("/testing/<int:staff_id>")
# def testding(staff_id):
#     testing = Registration.get_completed_courses_by_staff_id(staff_id)

#     return testing

#First page with all roles + attained status
@app.route("/all_roles/<int:staff_id>")
def testing(staff_id):
    all_roles = Ljps_role.get_all_learning_journey_roles()
    completed_courses = Registration.get_completed_courses_by_staff_id(staff_id)
    #looping through all available roles
    for role in all_roles:
        #find the required skills in the role
        required_skills = Role_required_skill.get_role_require_skill_by_ljpsr(role["ljpsr_id"])
        #check if staff has role by comparing num of completed_skills
        print(required_skills)
        num_skills = len(required_skills)
        completed_skills = 0
        for required_skill in required_skills:
            attached_courses = Attached_skill.get_attached_skill_by_skill_id(required_skill["skill_id"])
            for attached_course in attached_courses:
                if attached_course["course_id"] in completed_courses:
                    completed_skills += 1
                    break
        #adding field "attained" to each role
        if num_skills == completed_skills:
            role["attained"] = "True"
        else:
            role["attained"] = "False"
    if all_roles:
        return jsonify({
            'data': all_roles
            }), 200
    else:
        return jsonify({
            "message": "There are no roles"
        }), 404

#View a role after selecting
@app.route("/role/<int:ljpsr_id>")
def view_role(ljpsr_id):
    role = Ljps_role.get_learning_journey_role_by_id(ljpsr_id)
    skills = Role_required_skill.get_role_require_skill_by_ljpsr(ljpsr_id)
    skill_list = []
    for skill in skills:
        skill_info = Skill.get_skill_by_id(skill["skill_id"])
        skill_list.append(skill_info)
    if role:
        return jsonify({
            "data": {
                "role": role,
                "skills": skill_list
            }
        })

# Find COURSE by course_id
@app.route("/course/<string:course_id>")
def course_by_id(course_id):
    course = Course.get_course_by_id(course_id)
    if course:
        return jsonify({
            "data": course
        }), 200
    else:
        return jsonify({
            "message": "course not found."
        }), 404



# Find learning journeys by staff_id
@app.route("/lj/<int:staff_id>")
def learning_journey_by_staff(staff_id):
    learning_journey = Learning_journey.get_learning_journey_by_staff_id(staff_id)
    if len(learning_journey):
        return jsonify({
            "data": {
                    "learning_journey": learning_journey
                }
        }), 200
    else:
        return jsonify({
            "message": "Staff does not have any learning journeys."
        }), 404


# Find learning journey role from ljpsr_id
@app.route("/ljpsr/<int:ljpsr_id>")
def learning_journey_role_by_id(ljpsr_id):
    ljpsr = Ljps_role.get_learning_journey_role_by_id(ljpsr_id)
    if ljpsr:
        return jsonify({
            "data": {
                    "ljpsr": ljpsr
                }
        }), 200
    else:
        return jsonify({
            "message": "Learning Journey Role does not exist."
        }), 404

# Find skill by skill_id
@app.route("/skill/<int:skill_id>")
def skill_by_id(skill_id):
    skill = Skill.get_skill_by_id(skill_id)
    if skill:
        return jsonify({
            "data": {
                    "skill": skill
                }
        }), 200
    else:
        return jsonify({
            "message": "Skill not found."
        }), 404

# Find attached_skill by skill_id
@app.route("/attached_skill_by_skill/<int:skill_id>")
def attached_skill_by_skill(skill_id):
    attached_skill = Attached_skill.get_attached_skill_by_skill_id(skill_id)
    if len(attached_skill):
        return jsonify({
            "data": {
                    "attached_skill": attached_skill
                }
        }), 200
    else:
        return jsonify({
            "message": "Skill not attached to any courses."
        }), 404


# Find lj_course by journey_id (need dummy data to retrieve the courses for learning journey)
@app.route("/lj_course_by_journey/<int:journey_id>")
def lj_course_by_journey(journey_id):
    lj_course = Lj_course.get_lj_course_by_journey(journey_id)
    if len(lj_course):
        return jsonify({
            "data": {
                    "lj_course": lj_course
                }
        }), 200
    else:
        return jsonify({
            "message": "Learning Journey contains no courses."
        }), 404

# Find role_require_skill by ljpsr_id
@app.route("/role_require_skill_by_ljpsr/<int:ljpsr_id>")
def role_require_skill_by_ljpsr(ljpsr_id):
    role_require_skill = Role_required_skill.get_role_require_skill_by_ljpsr(ljpsr_id)
    if len(role_require_skill):
        return jsonify({
            "data": {
                    "role_require_skill": role_require_skill
                }
        }), 200
    else:
        return jsonify({
            "message": "Role has no skills assigned to it."
        }), 404

# Viewing skills needed for a role, according to which staff wants it
# (acceptance criteria is that staff who queries this should not which skill he/she already possesses)
@app.route("/view_skills_needed_for_role/<int:staff_id>")
def view_skills_needed_for_role(staff_id, ljpsr_id):
    # 1. from staff ID passed in, get the skills this staff has already acquired

    # 2. from LJPS role ID, get all the skills related to it

    # 3. separate them out into skills_already_acquired and skills_not_yet_acquired for this LJPS role.
    pass

# @app.route("/path/<int:id>", methods = ['POST'])
# def addCourseToLJ(id):
#     course = Course.getCourseByID(id)
#     #to json
#     return #json


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
