from flask import request, jsonify
from app import app
from .models import *
from .const import HttpStatus

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        print("<Request: {}>".format(request.json))
    return "<h1>Welcome to Flask Restful API</h1><p>Created By: Ayaz Alam</p>"

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

    elif request.method == 'POST':
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form

        nim = data.get('nim') or None
        name = data.get('name') or None

        construct = {}
        try:
            mhs = Mahasiswa(nim=nim, name=name)
            mhs.save()
            construct['success'] = True
            construct['message'] = 'Data saved'
            response = jsonify(construct)
            response.status_code = HttpStatus.CREATED
            print("<Nama: {}, Nim: {}>".format(name, nim))
        except Exception as e:
            construct['success'] = False
            construct['error'] = str(e)
            response = jsonify(construct)
            response.status_code = HttpStatus.BAD_REQUEST
    return response

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
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form

        nim = data.get('nim') or None
        name = data.get('name') or None

        construct = {}
        try:
            mhs.nim = nim
            mhs.name = name
            db.session.commit()
            construct['success'] = True
            construct['message'] = 'Data updated'
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
            construct['message'] = 'Data has been deleted.'
            response = jsonify(construct)
            response.status_code = HttpStatus.OK
        except Exception as e:
            construct['success'] = False
            construct['error'] = str(e)
            response = jsonify(construct)
            response.status_code = HttpStatus.BAD_REQUEST
    return response
