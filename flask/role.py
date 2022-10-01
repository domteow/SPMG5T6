from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import func, select
from flask_cors import CORS
from os import environ

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

class Role(db.Model):
    __tablename__ = 'role'

    role_id = db.Column(db.Integer, primary_key=True, nullable=False)
    role_name = db.Column(db.String(20), nullable=False)

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

    def get_role_by_id(role_id):
        role = Role.query.filter_by(role_id=role_id).first()
        if role:
            return role.to_dict()
        else:
            return None