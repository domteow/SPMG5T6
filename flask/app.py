import json
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

#login
@app.route("/login/<int:staff_id>")
def login(staff_id):
    staff = Staff.get_staff_by_id(staff_id)
    if staff:
        return jsonify({
            'data': staff
            }), 200
    else:
        return jsonify({
            "message": "There is no staff with that ID"
        }), 404
        
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
    # print(createLJ_result)
    # return createLJ_result
    return createLJ_course_result


# Reading a Learning Journey
@app.route("/readlj/<int:staff_id>")
def read_learning_journeys(staff_id):
    # call read lj function in Learning Journey class 
    read_result = Learning_journey.get_learning_journey_by_staff_id(staff_id)
    attained_skills = get_skills_attained(staff_id)
    completed_courses = Registration.get_completed_courses_by_staff_id(staff_id)
    if len(read_result):
        for lj in read_result:
            ljps_result = Ljps_role.get_learning_journey_role_by_id(lj['ljpsr_id'])
            lj['role_title'] = ljps_result['role_title']
            lj['role_desc'] = ljps_result['role_desc']
            role_skill_result = Role_required_skill.get_role_require_skill_by_ljpsr(lj['ljpsr_id'])
            all_skills = []
            for skill in role_skill_result:
                skill_result = Skill.get_skill_by_id(skill['skill_id'])
                curr_skill_status = 0
                if skill_result['skill_id'] in attained_skills:
                    curr_skill_status = 1
                all_skills.append({"skill_id":skill['skill_id'],"skill_name":skill_result['skill_name'],"skill_desc":skill_result['skill_desc'],"status":curr_skill_status})
            lj['skills'] = all_skills
            lj_course_result = Lj_course.get_lj_course_by_journey(lj['journey_id'])
            all_courses = []
            for lj_course in lj_course_result:
                course = Course.get_course_by_id(lj_course['course_id'])
                course_status = 0
                if course['course_id'] in completed_courses:
                    course_status = 1
                all_courses.append({"course_id":course['course_id'],"course_name":course['course_name'],"course_desc":course['course_desc'],"course_status":course_status,"course_type":course['course_type'],"course_category":course['course_category']})
            lj['courses'] = all_courses
    return jsonify({"data":read_result})

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

# Delete courses from Learning Journey
@app.route("/delete_course/<int:journey_id>", methods=['DELETE'])
def delete_drug(journey_id):
    data = request.get_json()
    for course_id in data['courses']:
        Lj_course.delete_lj_course(journey_id, course_id)
    newly_added_courses = Lj_course.get_lj_course_by_journey_list(journey_id)
    return jsonify({"courses":newly_added_courses})

@app.route("/get_team_members/<int:staff_id>")
def get_team_members(staff_id):
    manager_info = Staff.get_staff_by_id(staff_id)
    role_info = Role.get_role_by_id(manager_info['role_id'])

    if role_info['role_name'] != "manager":
        return jsonify({
            "Error" : "You are not a manager."
        })
    all_team = Staff.get_staff_from_department(manager_info['dept'])
    team_members = []
    for staff in all_team:
        if staff['staff_id'] != manager_info['staff_id']:
            team_members.append(staff)
    return jsonify({
        "manager" : manager_info,
        "team_members" : team_members
    })

@app.route("/get_all_staff/<int:staff_id>")
def get_all_staff(staff_id):
    hr_info = Staff.get_staff_by_id(staff_id)
    role_info = Role.get_role_by_id(hr_info['role_id'])

    if role_info['role_name'] != "hr":
        return jsonify({
            "Error" : "You are not a HR."
        })
    all_team = Staff.get_all_staff()
    all_staff = []
    for staff in all_team:
        if staff['staff_id'] != hr_info['staff_id']:
            all_staff.append(staff)
    return jsonify({
        "hr" : hr_info,
        "all_staff" : all_staff
    })

##################### Start of User story SA-9 & SA-13 (BRYAN) #####################

# Edit Skills in existing LJPS role
@app.route("/edit_skills_in_ljps_role", methods=['POST'])
def edit_skills_in_ljps_role():
    # retrieve data from POST call
    data = request.get_json()
    ljpsr_id = data['ljpsr_id']
    updated_skills = data['skills']
    # Get the current skills which this particular LJPS role contains
    current_skills = Role_required_skill.get_role_require_skill_by_ljpsr_list(ljpsr_id)
    # Compare and add the skills to the LJPS role
    add_skill_to_ljps_role(ljpsr_id,updated_skills,current_skills)
    # Compare and delete the skills
    delete_skill_to_ljps_role(ljpsr_id,updated_skills,current_skills)
    # After updating, get the retrieve all the current skills to send back out
    newly_added_skills = Role_required_skill.get_role_require_skill_by_ljpsr_list(ljpsr_id)
    return jsonify({"skills":newly_added_skills})


# Add Skill(s) to existing LJPS role
def add_skill_to_ljps_role(ljpsr_id,updated_skills,current_skills):
    for skill in updated_skills:
        if skill not in current_skills:
            # add skill if not in the current skill list
            Role_required_skill.create_ljps_skill(ljpsr_id, skill)

# Delete Skill(s) to existing LJPS role
def delete_skill_to_ljps_role(ljpsr_id,updated_skills,current_skills):
    for skill in current_skills:
        if skill not in updated_skills:
            # delete skill if not in the updated skill list
            Role_required_skill.delete_ljps_skill(ljpsr_id, skill)


# Find all existing roles with skills
@app.route("/read_all_roles")
def read_all_roles():
    # Find all LJPS roles in the db
    all_roles = Ljps_role.get_all_learning_journey_roles()
    if len(all_roles):
        for role in all_roles:
            # get all the skills of that particular LJPS role
            role_skill_result = Role_required_skill.get_role_require_skill_by_ljpsr_list(role['ljpsr_id'])
            all_skills = []
            for skill in role_skill_result:
                # find each skill details
                skill_result = Skill.get_skill_by_id(skill)
                all_skills.append({"skill_id":skill,"skill_name":skill_result['skill_name'],"skill_desc":skill_result['skill_desc'],"active":skill_result['active']})
            role['skills'] = all_skills

    return jsonify({"data":all_roles})

##################### End  of User story SA-9 & SA-13 (BRYAN) #####################

##################### Start of User story SA-19 (JANN) #####################

# To retrieve all skills 
@app.route("/courses", methods=['GET'])
def get_all_courses():
    all_courses = Course.get_all_courses()

    if all_courses:
        return jsonify({
            'data': all_courses
            }), 200
    else:
        return jsonify({
            "message": "There are no courses."
        }), 404

# Create a skill & assign courses to newly-created skill (HR)
@app.route("/create_skill", methods=['POST'])
def createSkill():
    data = request.get_json()

    skill_id = db.session.query(Skill.skill_id).count() + 1 
    skill_name = data["newSkillName"]
    skill_desc = data["newSkillDesc"]
    active = 1 
    attached_courses_str = data["newSkillCourses"]
    attached_courses = json.loads(attached_courses_str)

    # check if skill name exists 
    if Skill.check_skill_exists(skill_name):
        return jsonify(
            {
                "code": 401, 
                "data": {
                    "skill_name": skill_name
                }, 
                "message": "The skill name already exists. "
            }
        )

    # call create_skill method in Skill class to add skill to db
    create_skill_result = Skill.create_skill(skill_id, skill_name, skill_desc, active)

    # for each course in selected courses, add course to newly-created skill
    for course in attached_courses:
        create_attached_course_result = Attached_skill.create_attached_skill(course, skill_id)

        if not create_attached_course_result:
            break 
    
    # check if creation pass/fail 
    if not create_skill_result or not create_attached_course_result:
        if not create_skill_result and not create_attached_course_result:
            return jsonify({
                "message": "There was an error creating the skill and assigning it to relevant courses."
            }), 404 

        elif not create_skill_result:
            return jsonify({
                "message": "There was an error creating the skill."
            }), 404 
        
        else:
            return jsonify({
                "message": "There was an error assigning relevant courses to this skill."
            }), 404 
    
    else: 
        return jsonify({
            "message": "The role was successfully created."
        }), 201 

##################### End  of User story SA-19 (JANN) #####################

##################### Start of User story SA-2 (KELVIN) #####################
#To retrieve all skills and details
@app.route("/skills")
def get_all_skills():
    skills = Skill.get_all_skills()

    if len(skills):
        return jsonify({
            "data": {
                    "skills": skills
                }
        }), 200
    else:
        return jsonify({
            "message": "There are no skills."
        }), 404

#Create a role and add its relevant skills
#Takes in role_title, role_desc, and a list of skill_id to add to role
@app.route("/create_role", methods=['POST'])
def new_role():
    data = request.get_json()
    ljpsr_id = db.session.query(Ljps_role.ljpsr_id).count() + 1
    role_title = data["newRoleName"]
    role_desc = data["newRoleDesc"]
    skills_str = data["newRoleSkills"]
    skills = json.loads(skills_str)

    #check if the role name already exists
    if Ljps_role.check_learning_journey_role_exists(role_title):
        return jsonify({
                "message": "The role name already exists",
            }), 401

    # call create role function to add new role to DB
    create_role_result = Ljps_role.create_learning_journey_role(ljpsr_id, role_title, role_desc)
    
    #for skill_id in skills, add the skill to the role
    for skill_id in skills:
        create_role_skill_result = Role_required_skill.create_new_role_required_skill(skill_id, ljpsr_id)
        if not create_role_skill_result:
            break
    
    #check if either creation fails
    if not create_role_result or not create_role_skill_result:
        if not create_role_skill_result and not create_role_result:
            return jsonify({
                "message": "There was an error creating the role and its skills."
            }), 404
        elif not create_role_skill_result:
            return jsonify({
                "message": "There was an error adding the skill(s) to the role"
            }), 404
        else:
             return jsonify({
                "message": "There was an error adding the role"
            }), 404
    else:
        return jsonify({
            "message": "The role was successfully created"
        }), 201
################### End of User story SA-2 (KELVIN) ##########################


# USER STORY SA-15 CHILD ISSUE SA-36(bruno)
# For front-end, get all courses + course details related to the skill selected
@app.route("/get_courses_by_skill/<int:skill_id>")
def get_courses_by_skill(skill_id):
    # Get a list of the course IDs related to the skill
    course_ids = Attached_skill.get_attached_course_by_skill_id_list(skill_id)
    all_course_details = []
    for course in course_ids:
        all_course_details.append(Course.get_course_by_id(course))

    return jsonify({
            "data": {
                    
                    "courses": all_course_details
                }
        }), 200

# Add course to skill
@app.route("/add_course_to_skill", methods=['POST'])
def add_course_to_skill():
    # Step 1: Read the data passed over, and get the skill ID and array of courses to be added (courses_to_add)
    data = request.get_json()
    skill_id = data['skill_id']
    courses_to_add = data['course_arr']
    print(skill_id,courses_to_add)
    # Step 2: Get all the course IDs of the courses that are ALREADY in the skill. (existing_course_array)
    existing_course_array = Attached_skill.get_attached_course_by_skill_id_list(skill_id)
    print(existing_course_array)
    # Step 3: Compare existing_course_array with courses_to_add. If duplicates found, return error code 400
    for addCourse in courses_to_add:
        for existCourse in existing_course_array:
            if existCourse == addCourse:
                return jsonify({
                    "code": 400,
                    "message": "You are adding 1 or more duplicate course(s)"
                })

    # Step 4: If no duplicates, add the skill_id, course_id for each course in courses_to_add into the attached_skill table. 
    return Attached_skill.add_courses_to_skill(skill_id, courses_to_add)

 

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

# Find skills attatined by staff
def get_skills_attained(staff_id):
    completed_courses = Registration.get_completed_courses_by_staff_id(staff_id)
    attained_skills = Attached_skill.get_attached_skill_by_course_ids(completed_courses)
    return attained_skills

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)

