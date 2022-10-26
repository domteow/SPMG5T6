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
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_size': 1000,
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
    all_roles = Ljps_role.get_all_learning_journey_roles_active()
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

##################### Start of User story SA-20 (DOM) #####################
@app.route("/edit_LJ_courses/", methods = ['POST'])
def edit_LJ():
    data = request.get_json()
    journey_id = data['journey_id']
    course_arr = data['course_arr']
    print(data)
    Lj_course.edit_lj_course(journey_id, course_arr)
    return data



##################### End of User story SA-20 (DOM) #####################

@app.route("/get_team_members/<int:staff_id><string:course_arr>")
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
##################### Bug-fix view course in learning journey (Kelvin) #####################
@app.route("/get_courses_of_lj/<string:staff_id>&<int:lj_id>")
def get_courses_of_lj(staff_id ,lj_id):
    courses_in_lj = Lj_course.get_lj_course_by_journey(lj_id)
    completed_courses = Registration.get_completed_courses_by_staff_id(staff_id)
    for course in courses_in_lj:
        course["course_name"] = Course.get_course_by_id(course["course_id"])["course_name"]
        if course["course_id"] in completed_courses:
            course["course_status"] = 1
        else:
            course["course_status"] = 0
    if courses_in_lj:
        return jsonify({
            "data" : courses_in_lj
            }), 200
    else:
        return jsonify({
            "data" : {
                "message" : "Error retrieving courses"
                }
            })
#################################### End of bug fix #######################################

##################### Start of User Story SA-3 (Kelvin) #####################
@app.route("/edit_role_details", methods=["POST"])
def edit_role_details():
    data = request.get_json()
    ljpsr_id = data['ljpsr_id']
    new_role_name = data['new_role_name']
    new_role_desc = data['new_role_desc']   
    # Edit role title and desc
    if new_role_desc and new_role_name:
        result = Ljps_role.edit_details(ljpsr_id, new_role_name, new_role_desc)

    if result:
        return jsonify({
            "data": {
                "message": "Role name and description has been updated successfully"
                }
            }), 200
    else:
        return jsonify({
            "data": {
                "message": "There was an error updating the role name and description."
                }
        }), 404

# Edit LJPS role details
# def edit_role_details(ljpsr_id, new_role_name, new_role_desc):
#     Ljps_role.edit_details(ljpsr_id, new_role_name, new_role_desc)
        
##################### End of User Story SA-3 (Kelvin) #####################


##################### Start of User story SA-9 & SA-13 (BRYAN) #####################

# Edit Skills in existing LJPS role
@app.route("/edit_skills_in_ljps_role", methods=['POST'])
def edit_skills_in_ljps_role():
    # retrieve data from POST call
    data = request.get_json()
    ljpsr_id = data['ljpsr_id']
    added_skills = data['added_skills']
    deleted_skills = data['deleted_skills']
    # Compare and add the skills to the LJPS role
    if len(added_skills) > 0:
        add_skill_to_ljps_role(ljpsr_id,added_skills)
    # Compare and delete the skills
    if len(deleted_skills) > 0:
        delete_skill_to_ljps_role(ljpsr_id,deleted_skills)
    # After updating, get the retrieve all the current skills to send back out
    newly_added_skills = Role_required_skill.get_role_require_skill_by_ljpsr_list(ljpsr_id)
    return jsonify({"data":newly_added_skills})


# Add Skill(s) to existing LJPS role
def add_skill_to_ljps_role(ljpsr_id,added_skills):
    for skill in added_skills:
        # add skill if not in the current skill list
        Role_required_skill.create_ljps_skill(ljpsr_id, skill)

# Delete Skill(s) to existing LJPS role
def delete_skill_to_ljps_role(ljpsr_id,deleted_skills):
    for skill in deleted_skills:
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
                if skill_result["active"] == 1:
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
##################### End of User story SA-2 (KELVIN) #######################

##################### Start of User story SA-7 (KELVIN) #####################
@app.route("/delete_role/<int:role_id>&<int:is_active>&<string:role_name>")
def delete_role(role_id, is_active, role_name):
    result = Ljps_role.toggle_active(role_id, is_active)
    print(role_name)
    if result:
        if is_active == 1:
            message = role_name + " is now active"
        else:
            message = role_name + " is now inactive"
            
        return jsonify({
            "data": {
                    "message": message
                }
            }), 200
    else:
        return jsonify({
            "data": {
                "message": "There was an issue toggling the role active/inactive state"
                }
        }), 404

##################### End of User story SA-7 (KELVIN) ########################

##################### Start of User story SA-15 (BRUNO) #####################
# USER STORY SA-15 CHILD ISSUE SA-37(bruno)
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
# Get all skills, and course details related to each skill 
@app.route("/get_all_skills_and_courses")
def get_all_skills_and_courses():
    # Refer to helper function get_skill_and_course_details
    all_skills_and_courses = get_skill_and_course_details()

    if len(all_skills_and_courses):
        return jsonify({
            "data": {
                    "skills": all_skills_and_courses
                }
        }), 200
    else:
        return jsonify({
            "message": "There are no skills."
        }), 400


# USER STORY SA-15 CHILD ISSUE SA-36(bruno)
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
                }), 400

    # Step 4: If no duplicates, add the skill_id, course_id for each course in courses_to_add into the attached_skill table. 
    return Attached_skill.add_courses_to_skill(skill_id, courses_to_add)
##################### END of User story SA-15 (BRUNO) #####################


##################### START of User story SA-8 (JANN) #####################
@app.route("/delete_skill/<int:skill_id>&<int:isactive>&<string:skill_name>")
def delete_skill(skill_id, isactive, skill_name):
    result = Skill.toggle_active(skill_id, isactive)
    if result:
        if isactive == 1:
            message = skill_name + " has been toggled to active."

        else:
            message = skill_name + " has been toggled to inactive." 
            

        return jsonify({
            "code": 200, 
            "message": message 
        }), 200  
    
    else: 
        return jsonify({
            "code": 404, 
            "message": "There is an issue with changing the skill's activation status."
        }), 404

# For HR view in skills_page.js
@app.route("/get_all_skills_and_courses_hr")
def get_all_skills_and_courses_hr():
    # Refer to helper function get_skill_and_course_details
    all_skills_and_courses = get_skill_and_course_details_hr()

    if len(all_skills_and_courses):
        return jsonify({
            "data": {
                    "skills": all_skills_and_courses
                }
        }), 200
    else:
        return jsonify({
            "message": "There are no skills."
        }), 400

##################### END of User story SA-8 (JANN) #####################

##################### Start of User story SA-17 (BRUNO) #####################
# Remove one or more courses related to the skill
@app.route("/remove_course_from_skill", methods=['POST'])
def remove_course_from_skill():
    # Step 1: Read the data passed over, and get the skill ID and array of courses to be removed (courses_to_remove)
    data = request.get_json()
    skill_id = data['skill_id']
    courses_to_remove = data['course_arr']
    # Step 2: Get all the course IDs of the courses that are ALREADY in the skill. (existing_course_array)
    existing_course_array = Attached_skill.get_attached_course_by_skill_id_list(skill_id)

    # Step 3: Compare the length of both arrays, if same length means user is trying to delete all courses related to that skill, which is not allowed. 
    if len(courses_to_remove) == len(existing_course_array):
        return jsonify({
                    "code": 400,
                    "message": "You are removing all courses from the skill."
                }), 400
     # Step 4: If user not removing all courses, remove the skill_id, course_id for each course in courses_to_remove in the attached_skill table. 
    return Attached_skill.remove_course_from_skill(skill_id, courses_to_remove)


##################### END of User story SA-17 (BRUNO) #####################

##################### Start of User story SA-10(BRUNO) #####################
# USER STORY SA-15 CHILD ISSUE SA-57(bruno)
# View ongoing course of team member
@app.route("/get_ongoing_course_of_staff/<int:staff_id>")
def get_ongoing_course_of_staff(staff_id):
    # Step 1: Get details of staff from staff table (Name, deparment)
    staff_details = Staff.get_staff_by_id(staff_id)
    # Raising error if staff_id does not exist
    if not staff_details:
        return jsonify({
        "error_code": 400,
        "error_message": "Staff ID does not exist"
    }), 400
    # Step 2: From registration table, get all courses IDs that is "Registered" and 
    # "OnGoing" under the staff
    ongoing_course_ids = Registration.get_ongoing_courses_by_staff_id(staff_id)
    ongoing_courses = []
    # Step 3:For each course ID, get the name and status of it
    for course_id in ongoing_course_ids:
        ongoing_courses.append(Course.get_course_by_id(course_id))
    # Step 4: Return the data in json format
    return jsonify({
        "staff_details": staff_details,
        "ongoing_courses": ongoing_courses
    })
    
##################### END of User story SA-10 (BRUNO) #####################

##################### Start of User story SA-18 (BRYAN) #####################
# USER STORY SA-18 CHILD ISSUE SA-64 (BRYAN)
# View acquired skills of team member
@app.route("/get_attained_skills_of_staff/<int:staff_id>")
def get_attained_skills_of_staff(staff_id):
    # Step 1: Get details of staff from staff table (Name, deparment)
    staff_details = Staff.get_staff_by_id(staff_id)
    # Raising error if staff_id does not exist
    if not staff_details:
        return jsonify({
        "error_code": 400,
        "error_message": "Staff ID does not exist"
    }), 400
    # Step 2: From registration table, get all courses IDs that is "Registered" and 
    # "Completed" under the staff
    completed_course_ids = Registration.get_completed_courses_by_staff_id(staff_id)
    # Step 3: From attached_skill table, get all skill IDs attached to the courses
    attained_skill_ids = Attached_skill.get_attached_skill_by_course_ids(completed_course_ids)
    attained_skills = []
    # Step 4:For each skill ID, get the name and status of it
    for skill_id in attained_skill_ids:
        attained_skills.append(Skill.get_skill_by_id(skill_id))
    # Step 5: Return the data in json format
    return jsonify({
        "staff_details": staff_details,
        "attained_skills": attained_skills
    })
    
##################### END of User story SA-18 (BRYAN) #####################

######################################################################
# HELPER FUNCTIONS BELOW
######################################################################

# This helper function will return a list of all skill details. In each skill object, there will be the courses under the skill and its details too. 
def get_skill_and_course_details():
    # Array of skill objects
    skills = Skill.get_all_skills_active()
    # loop through the array, and for each skill, get the courses (+ details) and append the courses relevant to the skill object
    for skill in skills:
        # array to hold all the courses related to the skill
        all_courses = []
        course_ids = Attached_skill.get_attached_course_by_skill_id_list(skill['skill_id'])
        for course in course_ids:
            course_details = Course.get_course_by_id(course)
            all_courses.append(course_details)
        # Append all_courses array to the skill objects
        skill['courses'] = all_courses
    return skills

# (FOR HR) This helper function will return a list of all skill details for both INACTIVE & ACTIVE skills. 
# In each skill object, there will be the courses under the skill and its details too. 
def get_skill_and_course_details_hr():
    # Array of skill objects
    skills = Skill.get_all_skills()
    # loop through the array, and for each skill, get the courses (+ details) and append the courses relevant to the skill object
    for skill in skills:
        # array to hold all the courses related to the skill
        all_courses = []
        course_ids = Attached_skill.get_attached_course_by_skill_id_list(skill['skill_id'])
        for course in course_ids:
            course_details = Course.get_course_by_id(course)
            all_courses.append(course_details)
        # Append all_courses array to the skill objects
        skill['courses'] = all_courses
    return skills


# This helper function will get details of each skill under the LJPS Role passed in
def get_skill_detail_under_ljpsr(ljpsr_id):

    #from LJPS role ID, get all the skills related to it from role_required_skill (Array of skill IDs)
    skills_under_ljpsr = Role_required_skill.get_role_require_skill_by_ljpsr_list(ljpsr_id)

    # get active skills 
    active_skills_under_ljpsr = Skill.get_active_skills_list(skills_under_ljpsr)

    skills_under_ljpsr_details = []
    for skill in active_skills_under_ljpsr:
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

