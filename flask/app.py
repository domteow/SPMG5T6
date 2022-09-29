from turtle import st
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

# @app.route("/testing")
# def testding():
#     courses = ["COURSE1","COURSE2"]
#     testing = Attached_skill.get_attached_skill_by_course_ids(courses)

#     return jsonify({"data": testing})

#First page with all roles + attained status
@app.route("/all_roles/<int:staff_id>")
def get_all_roles(staff_id):
    #get all roles in dictionary format
    all_roles = Ljps_role.get_all_learning_journey_roles()
    #get courses completed by staff in list format
    completed_courses = Registration.get_completed_courses_by_staff_id(staff_id)
    #get skills completed by staff in list format
    completed_skills = Attached_skill.get_attached_skill_by_course_ids(completed_courses)
    #looping through all available roles
    for role in all_roles:
        #find the required skills in the role
        required_skills = Role_required_skill.get_role_require_skill_by_ljpsr_list(role["ljpsr_id"])
        #check if staff has role by completed_skills to required_skills
        result =  all(elem in completed_skills for elem in required_skills)
        #adding field "attained" to each role
        if result:
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
                "ljps_role": role,
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

@app.route("/view_skills_needed_for_role/<int:staff_id>/<int:ljpsr_id>")
def view_skills_needed_for_role(staff_id, ljpsr_id):
    # Get LJPS role Details
    role = Ljps_role.get_learning_journey_role_by_id(ljpsr_id)
    # 1. from staff ID passed in, get the skills this staff has already acquired
    # a. get all rows in registration table with this staff_id, then get the course_id for those which are marked completed under completion_status column
    completed_courses = Registration.get_completed_courses_by_staff_id(staff_id)
    # above is an array of COURSE_IDs

    # b. get all rows in attached_skill table with those course IDs, to get the skill IDs
    skills_completed = []
    for completed_course in completed_courses:
        attached_skills = Attached_skill.get_attached_skill_by_course_id(completed_course)
        for skill in attached_skills:
            skills_completed.append(skill['skill_id'])
        # skills_completed.extend(attached_skills)  
    
    # 2. from LJPS role ID, get all the skills related to it from role_required_skill
    skills_under_ljpsr = Role_required_skill.get_role_require_skill_by_ljpsr(ljpsr_id)
    
    # 3. separate them out into skills_completed and skills_not_yet_completed for this LJPS role.
    skills_under_ljpsr_details = []
    # Loop below is to get all details of the skills under that role
    for skill in skills_under_ljpsr:
        details = Skill.get_skill_by_id(skill['skill_id'])
        skills_under_ljpsr_details.append(details)

    # Loop below is to add in an additional field 'completed' , if user has completed that skill it will be set to 1, else 0.
    for skill in skills_under_ljpsr_details:
        if skill['skill_id'] in skills_completed:
            skill['completed'] = 1
        else:
            skill['completed'] = 0
    
    if len(skills_under_ljpsr_details):
        return jsonify({
            "data": {
                    "ljps_role": role,
                    "skills": skills_under_ljpsr_details
                }
        }), 200
    else:
        return jsonify({
            "message": "Role has no skills assigned to it."
        }), 404
   
    
    

# @app.route("/path/<int:id>", methods = ['POST'])
# def addCourseToLJ(id):
#     course = Course.getCourseByID(id)
#     #to json
#     return #json

# Creating a Learning Journey (dom)
@app.route("/createlj/<int:ljpsr_id>&<int:staff_id>", methods=['POST'])
def new_learning_journey(ljpsr_id, staff_id):
    # call create lj function in Learning Journey class 
    createLJ_result = Learning_journey.create_learning_journey(ljpsr_id, staff_id)
    print('function called to create LJ')
    print(createLJ_result)
    return createLJ_result

# Add Course(s) to existing Learning Journey (jann)
@app.route("/add_course/<int:journey_id>", methods=['POST'])
def add_course_to_existing_learning_journey(journey_id):
    # once inside Learning Journey, click "add course" 

    # get the courses ALR in the learning journey. 
    added_courses = Lj_course.get_lj_course_by_journey(journey_id)


    # using the learning journey id, get the role_id attached to the learning journey. 
    lj_role = Learning_journey.get_learning_journey_role_by_id(journey_id)

    # using the role_id, get the skills attached to the role. 
    role_related_skills = Role_required_skill.get_role_require_skill_by_ljpsr(lj_role)

    # get all courses related to role_related_skills

    for skill in role_related_skills:
        all_courses = Attached_skill.get_attached_skill_by_skill_id(skill)

    # with the list of skill_id, display all the courses that the user can choose from. 
    
        # however, use a IF function to indicate a status next to courses 
        # that are alr in the LJ ("This course has alr been added"). 
        # next to each course, show the course desc. 


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
