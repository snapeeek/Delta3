import sys
from datetime import datetime

from dateutil.tz import tz
from flask import jsonify, Blueprint, request, session, abort
from flask_jwt_extended import get_jwt_identity

from Delta3Mini.models.models import Card, User, Board, List, Label
from . import get_db
from .jwtMethods import auth_required, auth_fresh_required, refresh_authentication
from .super_secret import decode

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
    user = User.query.filter_by(id=get_jwt_identity()).first()
    return jsonify(json_list=[i.serialize for i in user.boards])


@apibp.route('/api/list-lists', methods=["GET"])
@auth_required
def list_lists():
    if session.get('logged_in'):
        json_data = request.args.get('board_id')
        json_data = decode(json_data)
        board_to_gather_lists = Board.query.filter_by(id=json_data).first()
        board_to_gather_lists.lists.sort(key=lambda x: x.index, reverse=False)
        if board_to_gather_lists in User.query.filter_by(id=get_jwt_identity()).first().boards:
            return jsonify(json_list=[i.serialize for i in board_to_gather_lists.lists])
    return abort(403)


@apibp.route('/api/list-public-lists', methods=["GET"])
def list_public_lists():
    json_data = request.args.get('board_id')
    json_data = decode(json_data)
    board_to_gather_lists = Board.query.filter_by(id=json_data).first()
    if board_to_gather_lists.public:
        return jsonify(json_list=[i.serialize for i in board_to_gather_lists.lists])
    else:
        return abort(403)


@apibp.route('/api/getBoardInfo', methods=["GET"])
@auth_required
def getBoardInfo():
    json_data = request.args.get('board_id')
    json_data = decode(json_data)
    board = Board.query.filter_by(id=json_data).first()
    if board in User.query.filter_by(id=get_jwt_identity()).first().boards:
        return jsonify(board=board.serialize)
    else:
        abort(403)

@apibp.route('/api/getPublicBoardInfo', methods=["GET"])
def getPublicBoardInfo():
    json_data = request.args.get('board_id')
    json_data = decode(json_data)
    board = Board.query.filter_by(id=json_data).first()
    if board.public:
        return jsonify(board=board.serialize)
    else:
        return abort(403)

@apibp.route('/api/patchListIndex', methods=["PATCH"])
def patchListIndex():
    list_id = request.json['id']
    list_id = decode(list_id)
    list = List.query.filter_by(id=list_id).first()
    board = Board.query.filter_by(id=list.board_id).first()
    for element in board.lists:
        if element.index == request.json['index']:
            list_to_be_swaped = element
            break
    list_to_be_swaped.index = list.index
    list.index = request.json['index']
    try:
        db.session.commit()
        return jsonify({'result': 'True'})
    except:
        return 'There was a problem patching list that task'

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
    id = decode(json_data['id'])
    board_to_delete = Board.query.get_or_404(id)

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
    id_ = decode(json_data['card_id'])
    card_to_edit = Card.query.filter_by(id=id_).first()
    if json_data['what'] == 'content':
        card_to_edit.content = json_data['content']
    elif json_data['what'] == 'name':
        card_to_edit.name = json_data['content']
    elif json_data['what'] == 'date':
        date = json_data['content']
        date_object = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ")
        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()
        help1 = date_object.replace(tzinfo=from_zone)
        help = help1.astimezone(to_zone)
        card_to_edit.term = help
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
    id_ = decode(json_data['board_id'])
    list = List(name=json_data['name'],
                board_id=id_)
    board = Board.query.filter_by(id=id_).first()
    if board not in User.query.filter_by(id=get_jwt_identity()).first().boards:
        return abort(403)

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
    id_ = decode(json_data['id'])
    board_to_archive = Board.query.get_or_404(id_)

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
    id_ = decode(json_data['list_id'])
    card = Card(name=json_data['name'],
                content='',
                list_id=id_)
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
    card_id_ = decode(json_data['cardID'])
    card = Card.query.filter_by(id=card_id_).scalar()
    label_id_ = decode(json_data['labelID'])
    label = Label.query.filter_by(id=int(label_id_)).scalar()

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
    board_id_ = decode(json_data['board_id'])
    board = Board.query.filter_by(id=board_id_).first()
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
    board_id_ = decode(json_data['board_id'])
    board = Board.query.filter_by(id=board_id_).first()
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
    list_id_ = decode(json_data['list_id'])
    list = List.query.filter_by(id=list_id_).first()
    list.name = json_data['list_name']

    try:
        db.session.commit()
        db.session.close()
        return jsonify({'result': 'success'})
    except:
        return 'There was a problem deleting that task'



@apibp.route('/api/changePublicBoard', methods=["POST"])
@auth_required
def changePublicBoard():
    json_data = request.json
    board_id_ = decode(json_data['id'])
    board = Board.query.filter_by(id=board_id_).first()
    try:
        board.public = not board.public
        db.session.commit()
        return jsonify({'result': 'success'})
    except:
        return 'There was a problem deleting that task'
      
@apibp.route('/api/editLabelText', methods=["POST"])
@auth_required
def editLabelText():
    json_data = request.json
    label_id_ = decode(json_data['label_id'])
    label = Label.query.filter_by(id=label_id_).first()
    label.text = json_data['text']

    try:
        db.session.commit()
        db.session.close()
        return jsonify({'result': 'success'})
    except:
        return 'There was a problem deleting that task'


@apibp.route('/api/addNewLabel', methods=["POST"])
@auth_required
def addNewLabel():
    json_data = request.json
    new_label = Label()
    label_color = json_data['color']
    label_text = json_data['text']
    board_id = decode(json_data['board_id'])
    card_id = decode(json_data['card_id'])
    board_to_add_new_label = Board.query.filter_by(id=board_id).first()
    card_to_add_new_label = Card.query.filter_by(id=card_id).first()
    new_label.color = label_color
    new_label.text = label_text
    board_to_add_new_label.labels.append(new_label)
    card_to_add_new_label.labels.append(new_label)

    try:
        db.session.add(new_label)
        db.session.commit()
        db.session.close()
        return jsonify({'result': 'success'})
    except:
        return 'There was a problem deleting that task'

