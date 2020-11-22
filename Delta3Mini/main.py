import sys

from flask import jsonify, send_from_directory, \
    make_response, Blueprint, redirect, request, session
from werkzeug.security import check_password_hash, generate_password_hash

from . import get_db
from .models.models import Card, User, Board, boards_and_users, List

app = Blueprint('main', __name__)
db = get_db()


@app.route('/', methods=["POST", "GET"])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Card(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'
    return make_response(open('Delta3Mini/templates/base.html').read())


@app.route('/register')
@app.route('/login')
@app.route('/board/<id>')
def reredirect(id=0):
    return make_response(open('Delta3Mini/templates/base.html').read())


@app.route('/api/list-boards')
def list_boards():
    if session.get('logged_in'):
        user = User.query.filter_by(username=session.get('username')).first()
        return jsonify(json_list=[i.serialize for i in user.boards])


@app.route('/api/list-lists', methods=["GET"])
def list_lists():
    if session.get('logged_in'):
        json_data = request.args.get('board_id')
        board_to_gather_lists = Board.query.filter_by(id=json_data).first()
        return jsonify(json_list=[i.serialize for i in board_to_gather_lists.lists])

@app.route('/api/delete', methods=["POST"])
def delete():
    json_data = request.json
    board_to_delete = Board.query.get_or_404(json_data['id'])

    try:
        db.session.delete(board_to_delete)
        db.session.commit()
    except:
        return 'There was a problem deleting that task'


@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static/img/', 'favicon.ico')


@app.route('/generate_board', methods=['GET'])
def generate_board():
    try:
        db.session.add()
        db.session.commit()
        return redirect('/')
    except:
        return 'There was an issue adding your task'

@app.route('/api/register', methods=["POST"])
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


@app.route('/api/generateBoard', methods=["POST"])
def generateBoard():
    json_data = request.json

    user = User.query.filter_by(username=session.get('username')).first()

    board = Board(name=json_data['name'],
                  background=json_data['background'],
                  team_id=json_data['team_id'],
                  )
    user.boards.append(board)
    try:
        db.session.add(board)
        db.session.commit()
        status = 'success'
    except:
        print(sys.exc_info()[0])
        status = 'this board couldn\'t have been added'
    db.session.close()
    return jsonify({'result': status})


@app.route('/api/generateList', methods=["POST"])
def generateList():
    json_data = request.json
    list = List(name=json_data['name'],
                board_id=json_data['board_id'])
    try:
        db.session.add(list)
        db.session.commit()
        status = 'success'
    except:
        print(sys.exc_info()[0])
        status = 'this board couldn\'t have been added'
    db.session.close()

    return jsonify({'result': status})
@app.route('/api/login', methods=["GET", "POST"])
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


@app.route('/api/logout')
def logout():
    session.pop('logged_in', None)
    return jsonify({'result': 'success'})


@app.route('/api/status')
def status():
    if session.get('logged_in'):
        if session['logged_in']:
            return jsonify({'status': True,
                            'username': session.get('username')})
    else:
        return jsonify({'status': False})
