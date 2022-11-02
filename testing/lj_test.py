import unittest
import flask_testing
import json
import sys

sys.path.append('./testing')

from app import db, app
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