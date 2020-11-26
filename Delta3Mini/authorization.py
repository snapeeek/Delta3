from flask import (
    Blueprint, request, session, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash

from . import get_db

db = get_db()

authbp = Blueprint('auth', __name__)
from .models.models import User


@authbp.route('/api/logout')
def logout():
    session.pop('logged_in', None)
    return jsonify({'result': 'success'})


@authbp.route('/api/status')
def status():
    if session.get('logged_in'):
        if session['logged_in']:
            return jsonify({'status': True,
                            'username': session.get('username')})
    else:
        return jsonify({'status': False})


@authbp.route('/api/register', methods=["POST"])
def register():
    json_data = request.json

    user = User(username=json_data['username'], email=json_data['email'],
                password=generate_password_hash(json_data['password']))

    try:
        db.session.add(user)
        db.session.commit()
        status = 'success'
    except:
        status = 'this user is already registred'
    db.session.close()
    return jsonify({'result': status})


@authbp.route('/api/login', methods=["GET", "POST"])
def login():
    json_data = request.json

    user = User.query.filter_by(username=json_data['username']).first()
    if user and check_password_hash(user.password, json_data['password']):
        session['logged_in'] = True
        session['username'] = json_data['username']
        status = True
    else:
        status = False

    ret = jsonify({'result': status})
    return ret
