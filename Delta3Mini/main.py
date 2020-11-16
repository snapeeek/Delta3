from flask import Blueprint, g, render_template, request, redirect, url_for, jsonify, send_from_directory, make_response, session, flash, Blueprint, flash, g, redirect, render_template, request, session, url_for
from .models.models import Card, User
from werkzeug.security import check_password_hash, generate_password_hash
from . import get_db

app = Blueprint('main', __name__)
db = get_db()



@app.route('/', methods=['POST', 'GET'])
def index():
    # if g.user == None:
    #     return redirect(url_for('auth.login'))
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Card(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'

    return render_template('base.html')

@app.route('/page/list-records')
def list_records():
    tasks = Card.query.order_by(Card.date_created).all()
    return jsonify(json_list=[i.serialize for i in tasks])

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Card.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

@app.route('/getlist')
def get_list():
    tasks = Card.query.order_by(Card.date_created).all()
    return jsonify()

@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static/img/', 'favicon.ico')

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

@app.route('/register/', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        print(username, email, password)
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif User.query.filter_by(username=username).first() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            db.session.add(User(username=username, email=email, password=generate_password_hash(password=password)))
            db.session.commit()

            return redirect('/')

        flash(error)

    return render_template("base.html")

@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()

        error = None
        user = User.query.filter_by(username=username).first()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user.password, password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user.id
            session['logged_in'] = True
            return redirect('/')

        flash(error)

    return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')