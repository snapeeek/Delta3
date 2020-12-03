from flask import send_from_directory, \
    make_response, Blueprint, redirect, request

from .__init__ import get_db
from .models.models import Card

mainbp = Blueprint('main', __name__)
db = get_db()


@mainbp.route('/', methods=["POST", "GET"])
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


@mainbp.route('/register')
@mainbp.route('/login')
@mainbp.route('/board/<id>')
@mainbp.route('/publicBoard/<id>')
def reredirect(id=0):
    return make_response(open('Delta3Mini/templates/base.html').read())


@mainbp.route('/favicon.ico')
def favicon():
    return send_from_directory('static/img/', 'favicon.ico')
