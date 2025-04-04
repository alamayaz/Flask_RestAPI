# Flask_RestAPISimple REST Full API With Flask and SQLAlchemy (Python 3)
Tutorial for building Create, Read, Update and Delete using REST Full API with Flask and SQLAlchemy

Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

Prerequisites
Make sure you have installed Python 3 on your device

Project structure
* flask-rest-api/
  |--- app/
  |    |--- module/
  |    |    |--- __init__.py
  |    |    |--- const.py
  |    |    |--- controller.py
  |    |    |--- models.py
  |    |--- __init__.py
  |--- venv/
  |--- run.py
Step to create flask rest api
A step by step series of examples that tell you how to get a development env running

Install virtual environment
pip install virtualenv
Create virtual environment and activate inside your flask-rest-api directory according the above structure
virtualenv venv
> On windows -> venv\Scripts\activate
> On linux -> . env/bin/activate
Install some third party librares on your virtual environment with pip
pip install flask sqlalchemy flask-sqlalchemy flask-migrate
Create run.py directory inside flask-project according the above structure
from app import app
app.run(debug=True, host='127.0.0.1', port=5000)
Create controller.py according the abpove structure flask-rest-api/app/module/
from flask import request, jsonify
from app import app

@app.route('/')
def index():
    return "<h1>Welcome to Flask Restful API</h1><p>Created By: Alvinditya Saputra</p>"
Create __init__.py inside app directory according the above structure flask-rest-api/app/
from flask import Flask

app = Flask(__name__)

from app.module.controller import *
Run first this application to make sure can running with terminal or command promt
python run.py
Access localhost:5000 according port that created in run.py
Sample 1

Configure the database with SQLAlchemy, you should create directory db/ inside app/ directory and modify __init__.py and it will be created flask-api.db inside app directory
* flask-rest-api/
  |--- app/
  |    |--- db/
  |    |--- module/
  |    |    |--- __init__.py
  |    |    |--- controller.py
  |    |    |--- models.py
  |    |--- __init__.py
  |--- venv/
  |--- run.py
import os
from flask import Flask
project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "db/flask-api.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

from app.module.controller import *
Define model to application and create database migration, you should create models.py file inside module directory according the above structure.
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app import app

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Mahasiswa(db.Model):
    __tablename__ = 'mahasiswa' #Must be defined the table name

    id = db.Column(db.Integer, unique=True, primary_key=True, nullable=False)
    nim = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)

    def __init__(self, nim, name):
        self.nim = nim
        self.name = name

    def __repr__(self):
        return "<Name: {}, Nim: {}>".format(self.name, self.nim)

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def getAll():
        students = Mahasiswa.query.all()
        result = []
        for student in students:
            obj = {
                'id': student.id,
                'nim': student.nim,
                'name': student.name
            }
            result.append(obj)
        return result

    def delete(self):
        db.session.delete(self)
        db.session.commit()
Run migration with flask-migrate, type in terminal as below
flask db init
flask db migrate
flask db upgrade
The structure of database should like as follows
Mahasiswa
id (Integer, PK, Autoincrement, NOT NULL)
name (String, NOT NULL)
nim (String, NOT NULL)
Create constant class to define constant variable for example variable to HTTP status, you should create file const.py inside app/module/ according the above structure
class HttpStatus:
    OK = 200
    CREATED = 201
    NOT_FOUND = 404
    BAD_REQUEST = 400
The structure project will be look as follows
* flask-rest-api/
  |--- app/
  |    |--- db/
  |    |--- module/
  |    |    |--- __init__.py
  |    |    |--- const.py
  |    |    |--- controller.py
  |    |    |--- models.py
  |    |--- __init__.py
  |--- venv/
  |--- run.py
Import database from models.py and constant class const.py add this line from .models import * and from .const import * to the controller.py, it's mean import all class, function or variables from models.py and const.py
Create function to get data from Http Request GET to retrieve all data from database with endpoint /mahasiswa
@app.route('/api/v1/mahasiswa', methods=['GET', 'POST'])
def mahasiswa():
    if request.method == 'GET':
        construct = {
            'error': [],
            'success': True,
            'mahasiswa': Mahasiswa.getAll()
        }
        response = jsonify(construct)
        response.status_code = HttpStatus.OK
    return response
Sample 2

How to insert data to database with Http Request POST? Okay, lets do it with create function input data from request, add this code to function mahasiswa as def mahasiswa()
    elif request.method == 'POST':
        nim = None if request.form['nim'] is "" else request.form['nim']
        name = None if request.form['name'] is "" else request.form['name']
        construct = {}
        try:
            mhs = Mahasiswa(nim=nim, name=name)
            mhs.save()
            construct['success'] = True
            construct['message'] = 'Data saved'
            response = jsonify(construct)
            response.status_code = HttpStatus.CREATED
        except Exception as e:
            construct['success'] = False
            construct['error'] = str(e)
            response = jsonify(construct)
            response.status_code = HttpStatus.BAD_REQUEST
Sample 3

Sample 4

Sample 5

Then create function to filter or get data by id for which will use to PUT and DELETE request, that mean this function can update and delete data from database
@app.route('/api/v1/mahasiswa/<int:id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def mahasiswaId(id):
    mhs = Mahasiswa.query.filter_by(id=id).first()
    if request.method == 'GET':
        construct = {
            'error': [],
            'success': True,
            'mahasiswa': {
                'id': mhs.id,
                'nim': mhs.nim,
                'name': mhs.name
            }
        }
        response = jsonify(construct)
        response.status_code = HttpStatus.OK
    elif request.method == 'PUT':
        nim = None if request.form['nim'] is "" else request.form['nim']
        name = None if request.form['name'] is "" else request.form['name']
        construct = {}
        try:
            mhs.nim = nim
            mhs.name = name
            db.session.commit()
            construct['success'] = True
            construct['message'] = 'Data saved'
            response = jsonify(construct)
            response.status_code = HttpStatus.OK
        except Exception as e:
            construct['success'] = False
            construct['error'] = str(e)
            response = jsonify(construct)
            response.status_code = HttpStatus.BAD_REQUEST
    elif request.method == 'DELETE':
        construct = {}
        try:
            mhs.delete()
            construct['success'] = True
            construct['message'] = 'Data has been delete.'
            response = jsonify(construct)
            response.status_code = HttpStatus.OK
        except Exception as e:
            construct['success'] = False
            construct['error'] = str(e)
            response = jsonify(construct)
            response.status_code = HttpStatus.BAD_REQUEST
    return response
Sample 6

Sample 7

Sample 8

Sample 9

Sample 10

After change structure of flask project
* flask-rest-api/
  |--- app/
  |    |--- db/
  |    |    |--- flask-api.db
  |    |--- module/
  |    |    |--- __init__.py
  |    |    |--- const.py
  |    |    |--- controller.py
  |    |    |--- models.py
  |    |--- __init__.py
  |--- migrations/
  |--- venv/
  |--- run.py
Want to demo online?
Backend Flask REST API
Built With
Python 3 - The language programming used
Flask - The web framework used
Flask Migrate - The database migration
Virtualenv - The virtual environment used
SQL Alchemy - The database library
Flask-SQLAlchemy - Flask and SQL Alchemy connector
