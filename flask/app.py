from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from course import Course
from attached_skill import Attached_skill
from learning_journey import Learning_journey
from lj_course import Lj_course
from LJPS_role import Ljps_role
from registration import Registration
from role_required_skill import Role_required_skill
from role import Role
from skill import Skill
from staff import Staff

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



# @app.route("/path/<int:id>", methods = ['POST'])
# def addCourseToLJ(id):
#     course = Course.getCourseByID(id)
#     #to json
#     return #json


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
