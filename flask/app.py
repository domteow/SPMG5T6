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
            role["attained"] = 1
        else:
            role["attained"] = 0
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

#USER STORY SA-1
# Viewing skills needed for a role, according to which staff wants it
# (acceptance criteria is that staff who queries this should know which skill he/she already possesses)
@app.route("/view_skills_needed_for_role/<int:staff_id>/<int:ljpsr_id>")
def view_skills_needed_for_role(staff_id, ljpsr_id):
    # Get LJPS role Details
    role = Ljps_role.get_learning_journey_role_by_id(ljpsr_id)
    # 1. from staff ID passed in, get the skills this staff has already acquired
    # a. get all rows in registration table with this staff_id, then get the course_id for those which are marked completed under completion_status column
    completed_courses = Registration.get_completed_courses_by_staff_id(staff_id)
    # above is an array of COURSE_IDs

    # b. get all rows in attached_skill table with those course IDs, to get the skill IDs
    skills_completed = Attached_skill.get_attached_skill_by_course_ids(completed_courses)
    # for completed_course in completed_courses:
    #     attached_skills = Attached_skill.get_attached_skill_by_course_id(completed_course)
    #     for skill in attached_skills:
    #         skills_completed.append(skill['skill_id'])
        # skills_completed.extend(attached_skills)  
    
    # 2. get all skills + their details under this LJPS role with the helper function
    skills_under_ljpsr_details = get_skill_detail_under_ljpsr(ljpsr_id)

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

# USER STORY SA-6
# View courses under the skills in that role by user 
# IMPT: only relevant courses that are active should be displayed
@app.route("/view_courses_under_skill/<int:staff_id>/<int:ljpsr_id>")
def view_courses_under_skill(staff_id, ljpsr_id):

    # # Get LJPS role Details
    role = Ljps_role.get_learning_journey_role_by_id(ljpsr_id)

    skills_under_ljpsr_details = get_skill_detail_under_ljpsr(ljpsr_id)

    # for each skill in skills_under_ljpsr_details, query the attached_skill table to get the course, then query the course table to get the course details, and insert these courses as key (courses) value (array of course objects) pairs back into skills_under_ljpsr_details
    for skill in skills_under_ljpsr_details:
        # array below is to store all  courses objects (+ their details) of each skill
        all_course_details = []
        courses_attached = Attached_skill.get_attached_course_by_skill_id_list(skill['skill_id'])
        for course in courses_attached:
            course_detail = Course.get_course_by_id(course)
            if course_detail["course_status"] == 'Active':
                all_course_details.append(course_detail)
        skill['courses'] = all_course_details
    
    if len(skills_under_ljpsr_details):
        return jsonify({
            "data": {
                    "ljps_role": role,
                    "skills_with_courses": skills_under_ljpsr_details
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

# Creating a LJ in learning_journey table (dom)
@app.route("/createlj/<int:ljpsr_id>&<int:staff_id>&<string:course_arr>", methods=['POST'])
def new_learning_journey(ljpsr_id, staff_id, course_arr):
    journey_id = db.session.query(Learning_journey.journey_id).count() + 1

    # call create lj function in Learning Journey class 
    createLJ_result = Learning_journey.create_learning_journey(journey_id, ljpsr_id, staff_id)
    # call create lj course function in Lj_course class
    createLJ_course_result = Lj_course.create_lj_course(journey_id,course_arr)
    print('function called to create LJ')
    print(createLJ_result)
    return createLJ_result



# Reading a Learning Journey
@app.route("/readlj/<int:staff_id>")
def read_learning_journeys(staff_id):
    # call read lj function in Learning Journey class 
    read_result = Learning_journey.get_learning_journey_by_staff_id(staff_id)
    if len(read_result):
        for lj in read_result:
            ljps_result = Ljps_role.get_learning_journey_role_by_id(lj['ljpsr_id'])
            lj['role_title'] = ljps_result['role_title']
            lj['role_desc'] = ljps_result['role_desc']
            role_skill_result = Role_required_skill.get_role_require_skill_by_ljpsr(lj['ljpsr_id'])
            all_skills = []
            for skill in role_skill_result:
                skill_result = Skill.get_skill_by_id(skill['skill_id'])
                all_skills.append({"skill_id":skill['skill_id'],"skill_name":skill_result['skill_name'],"skill_desc":skill_result['skill_desc'],"status":0})
            lj['skills'] = all_skills
            lj_course_result = Lj_course.get_lj_course_by_journey(lj['journey_id'])
            all_courses = []
            for lj_course in lj_course_result:
                course = Course.get_course_by_id(lj_course['course_id'])
                all_courses.append({"course_id":course['course_id'],"course_name":course['course_name'],"course_desc":course['course_desc'],"course_status":course['course_status'],"course_type":course['course_type'],"course_category":course['course_category']})
            lj['courses'] = all_courses
    return jsonify({"learning_journeys":read_result})

# Add Course(s) to existing Learning Journey (jann)
@app.route("/add_course/<int:journey_id>", methods=['POST'])
def add_course_to_existing_learning_journey(journey_id):
    # once inside Learning Journey, click "add course" 
    data = request.get_json()
    added_courses = Lj_course.get_lj_course_by_journey_list(journey_id)
    for course_id in data['courses']:
        if course_id not in added_courses:
            Lj_course.create_lj_course(journey_id, course_id)
    newly_added_courses = Lj_course.get_lj_course_by_journey_list(journey_id)
    return jsonify({"courses":newly_added_courses})
    # for course_id in data['courses']:
    #     Lj_course.create_lj_course(journey_id, course_id)
    # # get the courses ALR in the learning journey. 
    # added_courses = Lj_course.get_lj_course_by_journey_list(journey_id) # data type: list 

    # # using the learning journey id, get the role_id attached to the learning journey. 
    # lj_role = Learning_journey.get_learning_journey_role_by_id(journey_id) # data type: str (i hope)

    # # using the role_id, get the skills attached to the role. 
    # role_related_skills = Role_required_skill.get_role_require_skill_by_ljpsr_list(lj_role)  # data type: list 

    # # get all courses related to role_related_skills 
    # all_courses = Attached_skill.get_attached_skill_by_course_ids(role_related_skills) # data type: list
    # all_courses_with_description = [] # data type: list of tuples e.g. [(is101, stupid mod, TRUE)] where index 0 is course, index 1 is desc, index 2 is TRUE (can take) 

    # # show description 
    # for course in all_courses: 
    #     course_info = Course.get_course_by_id(course)
    #     course_desc = course_info['course_desc']
    #     can_take = True

    #     # however, use a IF function to indicate a status next to courses 
    #     # TRUE = can take, FALSE = take alr 
    #     if course in added_courses:
    #         can_take = False 

    #     all_courses_with_description.append((course, course_desc, can_take)) 
    
    # return all_courses_with_description

@app.route("/delete_course/<int:journey_id>", methods=['DELETE'])
def delete_drug(journey_id):
    data = request.get_json()
    for course_id in data['courses']:
        Lj_course.delete_lj_course(journey_id, course_id)
    newly_added_courses = Lj_course.get_lj_course_by_journey_list(journey_id)
    return jsonify({"courses":newly_added_courses})

######################################################################
# HELPER FUNCTIONS BELOW
######################################################################

# This helper function will get details of each skill under the LJPS Role passed in
def get_skill_detail_under_ljpsr(ljpsr_id):

    #from LJPS role ID, get all the skills related to it from role_required_skill (Array of skill IDs)
    skills_under_ljpsr = Role_required_skill.get_role_require_skill_by_ljpsr_list(ljpsr_id)

    skills_under_ljpsr_details = []
    for skill in skills_under_ljpsr:
        details = Skill.get_skill_by_id(skill)
        skills_under_ljpsr_details.append(details)
    return skills_under_ljpsr_details

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)

