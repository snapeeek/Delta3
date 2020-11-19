from datetime import datetime

from Delta3Mini import db


def dump_datetime(value):
    """Deserialize datetime object into string form for JSON processing."""
    if value is None:
        return None
    return [value.strftime("%Y-%m-%d"), value.strftime("%H:%M:%S")]


teams_and_users = db.Table('TeamsAndUsers',
                           db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                           db.Column('team_id', db.Integer, db.ForeignKey('team.id'), primary_key=True)
                           )

boards_and_users = db.Table('BoardAndUsers',
                            db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                            db.Column('board_id', db.Integer, db.ForeignKey('board.id'), primary_key=True)
                            )

cards_and_labels = db.Table('CardsAndLabels',
                            db.Column('card_id', db.Integer, db.ForeignKey('card.id'), primary_key=True),
                            db.Column('label_id', db.Integer, db.ForeignKey('label.id'), primary_key=True)
                            )

boards_and_labels = db.Table('Boardsandlabels',
                            db.Column('board_id', db.Integer, db.ForeignKey('board.id'), primary_key=True),
                            db.Column('label_id', db.Integer, db.ForeignKey('label.id'), primary_key=True)
                            )


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    teams = db.relationship('Team', secondary=teams_and_users, lazy='subquery', backref=db.backref('users', lazy=True))
    boards = db.relationship('Board', secondary=boards_and_users, lazy='subquery',
                             backref=db.backref('users', lazy=True))

    def __repr__(self):
        return '<User %r>' % self.username

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

class Board(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), default="Board")
    background = db.Column(db.String(20))
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=True)
    labels = db.relationship('Label', secondary=boards_and_labels, lazy='subquery',
                             backref=db.backref('boards', lazy=True))
    lists = db.relationship('List', backref='board', lazy=True)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id': self.id,
            'name': self.name,
            'team_id': self.team_id,
        }

class Label(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    color = db.Column(db.String(30))
    text = db.Column(db.String(50))

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)



class List(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    board_id = db.Column(db.Integer, db.ForeignKey('board.id'), nullable=False)
    name = db.Column(db.String(50))
    cards = db.relationship('Card', backref='card', lazy=True)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)


class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    list_id = db.Column(db.Integer, db.ForeignKey('list.id'), nullable=False)
    lists_of_elements = db.relationship('Listofelements', backref='card', lazy=True)
    labels = db.relationship('Label', secondary=cards_and_labels, lazy='subquery',
                             backref=db.backref('cards', lazy=True))

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

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


class Listofelements(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    card_id = db.Column(db.Integer, db.ForeignKey('card.id'), nullable=False)
    name = db.Column(db.String(50))
    done = db.Column(db.Integer, default=0)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)


class Element(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    done = db.Column(db.Boolean(False))
    list_of_elemets_id = db.Column(db.Integer, db.ForeignKey('listofelements.id'), nullable=False)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)


class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    boards = db.relationship('Board', backref='team', lazy=True)
    Name = db.Column(db.String(50))

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

