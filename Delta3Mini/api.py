import sys

from flask import jsonify, Blueprint, request, session

from . import get_db
from .models.models import Card, User, Board, List

apibp = Blueprint('api', __name__)
db = get_db()


@apibp.route('/api/list-boards')
def list_boards():
    if session.get('logged_in'):
        user = User.query.filter_by(username=session.get('username')).first()
        return jsonify(json_list=[i.serialize for i in user.boards])


@apibp.route('/api/list-lists', methods=["GET"])
def list_lists():
    if session.get('logged_in'):
        json_data = request.args.get('board_id')
        board_to_gather_lists = Board.query.filter_by(id=json_data).first()
        return jsonify(json_list=[i.serialize for i in board_to_gather_lists.lists])


@apibp.route('/api/getBoardInfo', methods=["GET"])
def getBoardInfo():
    json_data = request.args.get('board_id')
    board = Board.query.filter_by(id=json_data).first()
    return jsonify(board=board.serialize)


@apibp.route('/api/delete', methods=["POST"])
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
def editCard():
    json_data = request.json
    card_to_edit = Card.query.filter_by(id=json_data['card_id']).first()
    card_to_edit.content = json_data['content']
    try:
        db.session.commit()
        return jsonify({'result': 'success'})
    except:
        return 'There was a problem deleting that task'


@apibp.route('/api/generateBoard', methods=["POST"])
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


@apibp.route('/api/generateList', methods=["POST"])
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


@apibp.route('/api/unarchiveBoard', methods=["POST"])
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
