from datetime import datetime

from .. import db


def dump_datetime(value):
    """Deserialize datetime object into string form for JSON processing."""
    if value is None:
        return None
    return [value.strftime("%Y-%m-%d"), value.strftime("%H:%M:%S")]


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


class Board(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), default="Board")
    background = db.Column(db.String(20))
    labels = db.relationship('Label', backref='Board', lazy=True)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=True)
    lists = db.relationship('List', backref='board', lazy=True)


class List(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    board_id = db.Column(db.Integer, db.ForeignKey('Board.id'), nullable=False)
    name = db.Column(db.String(50))
    cards = db.relationship('Card', backref='card', lazy=True)


class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    list_id = db.Column(db.Integer, db.ForeignKey('List.id'), nullable=False)
    name = db.Column(db.String(50))
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    lists_of_elements = db.relationship('ListOfElements', backref='Card', lazy=True)

    def __repr__(self):
        return '<Task %r>' % self.id

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id': self.id,
            'content': self.content,
            'date_created': dump_datetime(self.date_created),
        }


class Label(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    color = db.Column(db.String(30))
    text = db.Column(db.String(50))


class Element(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    done = db.Column(db.Boolean(False))


class ListOfElements(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    card_id = db.Column(db.Integer, db.ForeignKey('Card.id'), nullable=False)


class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    boards = db.relationship('Board', backref='team', lazy=True)
    Name = db.Column(db.String(50))


teams_and_users = db.Table('TeamsAndUsers',
                           db.Column('user_id', db.Integer, db.ForeignKey('User.id'), primary_key=True),
                           db.Column('team_id', db.Integer, db.ForeignKey('Team.id'), primary_key=True)
                           )

board_and_users = db.Table('BoardAndUsers',
                           db.Column('user_id', db.Integer, db.ForeignKey('User.id'), primary_key=True),
                           db.Column('Board_id', db.Integer, db.ForeignKey('Board.id'), primary_key=True)
                           )
