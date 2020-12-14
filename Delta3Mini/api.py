import sys
from datetime import datetime
from flask import jsonify, Blueprint, request, session, abort
import tzlocal
from tzlocal import get_localzone


from . import get_db
from .jwtMethods import auth_required, auth_fresh_required, refresh_authentication
from Delta3Mini.models.models import Card, User, Board, List, Label

apibp = Blueprint('api', __name__)
db = get_db()


@apibp.route('/api/status')
def status():
    if session.get('logged_in'):
        if session['logged_in']:
            return jsonify({'status': True,
                            'username': session.get('username')})
    else:
        return jsonify({'status': False})


@apibp.route('/api/list-boards')
@auth_required
def list_boards():
    user = User.query.filter_by(username=session.get('username')).first()
    return jsonify(json_list=[i.serialize for i in user.boards])


@apibp.route('/api/list-lists', methods=["GET"])
@auth_required
def list_lists():
    if session.get('logged_in'):
        json_data = request.args.get('board_id')
        board_to_gather_lists = Board.query.filter_by(id=json_data).first()
        return jsonify(json_list=[i.serialize for i in board_to_gather_lists.lists])


@apibp.route('/api/list-public-lists', methods=["GET"])
def list_public_lists():
    json_data = request.args.get('board_id')
    board_to_gather_lists = Board.query.filter_by(id=json_data).first()
    return jsonify(json_list=[i.serialize for i in board_to_gather_lists.lists])


@apibp.route('/api/getBoardInfo', methods=["GET"])
@auth_required
def getBoardInfo():
    json_data = request.args.get('board_id')
    board = Board.query.filter_by(id=json_data).first()
    return jsonify(board=board.serialize)


@apibp.route('/api/getPublicBoardInfo', methods=["GET"])
def getPublicBoardInfo():
    json_data = request.args.get('board_id')
    board = Board.query.filter_by(id=json_data).first()
    if board.public:
        return jsonify(board=board.serialize)
    else:
        return abort(403)


@apibp.route('/api/refresh_token', methods=['POST'])
@auth_fresh_required
def refresh_token():
    old_access_token = request.json['access_token']
    new_access_token = refresh_authentication(old_token=old_access_token)
    return jsonify({'status': True,
                    'access_token': new_access_token})


@apibp.route('/api/delete', methods=["POST"])
@auth_required
def delete():
    json_data = request.json
    board_to_delete = Board.query.get_or_404(json_data['id'])

    user = User.query.filter_by(username=json_data['username']).first()

    if board_to_delete in user.boards:
        try:
            db.session.delete(board_to_delete)
            db.session.commit()
            return jsonify({'result': 'success'})
        except:
            return 'There was a problem deleting that task'
    else:
        return 'There was a problem deleting that task'


@apibp.route('/api/editCard', methods=["POST"])
@auth_required
def editCard():
    json_data = request.json
    card_to_edit = Card.query.filter_by(id=json_data['card_id']).first()
    if json_data['what'] == 'content':
        card_to_edit.content = json_data['content']
    elif json_data['what'] == 'name':
        card_to_edit.name = json_data['content']
    elif json_data['what'] == 'date':
        date = json_data['content']
        print(date)
        date_object = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ")
        help = get_localzone().localize(date_object)

        print(date_object)
        card_to_edit.term = date_object
    elif json_data['what'] == 'done':
        card_to_edit.done = json_data['content']

    try:
        db.session.commit()
        return jsonify({'result': 'True'})
    except:
        return 'There was a problem deleting that task'


@apibp.route('/api/generateBoard', methods=["POST"])
@auth_required
def generateBoard():
    json_data = request.json

    user = User.query.filter_by(username=session.get('username')).first()

    board = Board(name=json_data['name'],
                  background=json_data['background'],
                  team_id=json_data['team_id'],
                  )
    user.boards.append(board)
    try:
        board.labels.append(Label(color="Brown", text=""))
        board.labels.append(Label(color="Coral", text=""))
        board.labels.append(Label(color="DarkSlateGrey", text=""))
        board.labels.append(Label(color="Indigo", text=""))
        db.session.add(board)
        db.session.commit()
        status = 'success'
    except:
        print(sys.exc_info()[0])
        status = 'this board couldn\'t have been added'
    db.session.close()
    return jsonify({'result': status})


@apibp.route('/api/generateList', methods=["POST"])
@auth_required
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
        status = 'this list couldn\'t have been added'
    db.session.close()
    return jsonify({'result': status})


@apibp.route('/api/archive', methods=["POST"])
@auth_required
def archive():
    json_data = request.json
    board_to_archive = Board.query.get_or_404(json_data['id'])

    user = User.query.filter_by(username=json_data['username']).first()

    if board_to_archive in user.boards:
        board_to_archive.archived = True
        try:
            db.session.commit()
            db.session.close()
            return jsonify({'result': 'success'})
        except:
            return 'There was a problem deleting that task'

    else:
        return 'There was a problem deleting that task'


@apibp.route('/api/generateCard', methods=["POST"])
@auth_required
def generateCard():
    json_data = request.json
    card = Card(name=json_data['name'],
                content='',
                list_id=json_data['list_id'])
    try:
        db.session.add(card)
        db.session.commit()
        status = 'success'
    except:
        print(sys.exc_info()[0])
        status = 'this card couldn\'t have been added'
    db.session.close()
    return jsonify({'result': status})


@apibp.route('/api/addOrDeleteLabel', methods=["POST"])
@auth_required
def addLabel():
    json_data = request.json
    card = Card.query.filter_by(id=json_data['cardID']).scalar()
    label = Label.query.filter_by(id=int(json_data['labelID'])).scalar()

    if label not in card.labels:
        try:
            card.labels.append(label)
            db.session.commit()
            status = 'success'
        except:
            print(sys.exc_info()[0])
            status = 'this card couldn\'t have been added'
    else:
        try:
            card.labels.remove(label)
            db.session.commit()
            status = 'success'
        except:
            print(sys.exc_info()[0])
            status = 'this card couldn\'t have been deleted'

    db.session.close()

    return jsonify({'result': status})


@apibp.route('/api/unarchiveBoard', methods=["POST"])
@auth_required
def unarchiveBoard():
    json_data = request.json
    board = Board.query.filter_by(id=json_data['board_id']).first()
    board.archived = False

    try:
        db.session.commit()
        db.session.close()
        return jsonify({'result': 'success'})
    except:
        return 'There was a problem deleting that task'


@apibp.route('/api/editBoard', methods=["POST"])
@auth_required
def editBoard():
    json_data = request.json
    board = Board.query.filter_by(id=json_data['board_id']).first()
    board.name = json_data['name']

    try:
        db.session.commit()
        db.session.close()
        return jsonify({'result': 'success'})
    except:
        return 'There was a problem deleting that task'


@apibp.route('/api/editList', methods=["POST"])
@auth_required
def editList():
    json_data = request.json
    list = List.query.filter_by(id=json_data['list_id']).first()
    list.name = json_data['list_name']

    try:
        db.session.commit()
        db.session.close()
        return jsonify({'result': 'success'})
    except:
        return 'There was a problem deleting that task'


@apibp.route('/api/editLabelText', methods=["POST"])
@auth_required
def editLabelText():
    json_data = request.json
    label = Label.query.filter_by(id=json_data['label_id']).first()
    label.text = json_data['text']

    try:
        db.session.commit()
        db.session.close()
        return jsonify({'result': 'success'})
    except:
        return 'There was a problem deleting that task'
