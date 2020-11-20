from flask import jsonify, send_from_directory, \
    make_response, Blueprint, redirect, request, session
from werkzeug.security import check_password_hash, generate_password_hash

from . import get_db
from .models.models import Card, User, Board, boards_and_users

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

    # return render_template('base.html')
    return make_response(open('Delta3Mini/templates/base.html').read())


@app.route('/register')
@app.route('/login')
def reredirect():
    return make_response(open('Delta3Mini/templates/base.html').read())


@app.route('/api/list-boards')
def list_boards():
    # tasks = Card.query.order_by(Card.date_created).all()
    # param = request.form['p']
    if session.get('logged_in'):
        user = User.query.filter_by(username=session.get('username')).first()
        return jsonify(json_list=[i.serialize for i in user.boards])


@app.route('/api/delete', methods=["POST"])
def delete():
    json_data = request.json
    board_to_delete = Board.query.get_or_404(json_data['id'])

    try:
        db.session.delete(board_to_delete)
        db.session.commit()
    except:
        return 'There was a problem deleting that task'


@app.route('/getlist')
def get_list():
    tasks = Card.query.order_by(Card.date_created).all()
    return jsonify()


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


# @app.route('/update/<int:id>', methods=['GET', 'POST'])
# def update(id):
#     task = Card.query.get_or_404(id)
#
#     if request.method == 'POST':
#         task.content = request.form['content']
#
#         try:
#             db.session.commit()
#             return redirect('/')
#         except:
#             return 'There was an issue updating your task'
#
#     else:
#         return render_template('update.html', task=task)

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
