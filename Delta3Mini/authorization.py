from flask import (
    Blueprint, request, session, jsonify, make_response
)
from werkzeug.security import check_password_hash, generate_password_hash

from . import get_db

db = get_db()

authbp = Blueprint('auth', __name__)
from .models.models import User, BlacklistToken


@authbp.route('/api/logout')
def logout():
    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_token = auth_header.split(" ")[1]
    else:
        auth_token = ''
    if auth_token:
        resp = User.decode_auth_token(auth_token)
        if not isinstance(resp, str):
            # mark the token as blacklisted
            blacklist_token = BlacklistToken(token=auth_token)
            try:
                # insert the token
                db.session.add(blacklist_token)
                db.session.commit()
                responseObject = {
                    'status': 'success',
                    'message': 'Successfully logged out.'
                }
                return make_response(jsonify(responseObject)), 200
            except Exception as e:
                responseObject = {
                    'status': 'fail',
                    'message': e
                }
                return make_response(jsonify(responseObject)), 200
        else:
            responseObject = {
                'status': 'fail',
                'message': resp
            }
            return make_response(jsonify(responseObject)), 401
    else:
        responseObject = {
            'status': 'fail',
            'message': 'Provide a valid auth token.'
        }
        return make_response(jsonify(responseObject)), 403


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
    try:
        status = False
        ret = jsonify({'result': status})

        if user and check_password_hash(user.password, json_data['password']):
            session['logged_in'] = True
            session['username'] = json_data['username']
            status = True
            auth_token = user.encode_auth_token(user.id)
            auth_token = str(auth_token)
            print(auth_token)
            ret = jsonify({'result': status, 'message': 'i aint no snitch', 'auth_token': auth_token})
        return ret
    except Exception as e:
        print(e)
        ret = {
            'result': False,
            'message': 'Try again'
        }
        return ret
