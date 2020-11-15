from flask import Blueprint, g, render_template, request, redirect, url_for
from .models.models import Card
from . import get_db
app = Blueprint('main', __name__)
db = get_db()


@app.route('/', methods=['POST', 'GET'])
def index():
    if g.user == None:
        return redirect(url_for('auth.login'))
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Card(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'

    else:
        tasks = Card.query.order_by(Card.date_created).all()
        return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Card.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Card.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('update.html', task=task)