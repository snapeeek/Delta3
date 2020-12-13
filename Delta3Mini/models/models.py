from datetime import datetime, timedelta

import jwt
# from Delta3Mini import db
from Delta3Mini import db

SUPER_SECRET_KEY = "skurczybonk"


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

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Validates the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, SUPER_SECRET_KEY, algorithms=['HS256'])
            is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
            if is_blacklisted_token:
                return 'Token blacklisted. Please log in again.'
            else:
                return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'


class BlacklistToken(db.Model):
    """
    Token Model for storing JWT tokens
    """
    __tablename__ = 'blacklist_tokens'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, token):
        self.token = token
        self.blacklisted_on = datetime.now()

    def __repr__(self):
        return '<id: token: {}'.format(self.token)

    @staticmethod
    def check_blacklist(auth_token):
        # check whether auth token has been blacklisted
        res = BlacklistToken.query.filter_by(token=str(auth_token)).first()
        if res:
            return True
        else:
            return False

    @staticmethod
    def delete_from_db():
        BlacklistToken.query.filter(BlacklistToken.blacklisted_on <= datetime.now() - timedelta(minutes=30)).delete()
        db.session.commit()

    @staticmethod
    def add_to_db(auth_token):
        # mark the token as blacklisted
        BlacklistToken.delete_from_db()
        blacklist_token = BlacklistToken(token=auth_token)
        if BlacklistToken.query.filter_by(token=blacklist_token.token).scalar() is None:
            # insert the token
            db.session.add(blacklist_token)
            db.session.commit()
        else:
            pass


class Board(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), default="Board")
    background = db.Column(db.String(20))
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=True)
    archived = db.Column(db.Boolean, default=False)
    public = db.Column(db.Boolean, default=False)
    labels = db.relationship('Label', secondary=boards_and_labels, lazy='subquery',
                             backref=db.backref('boards', lazy=True),
                             cascade="all,delete")
    lists = db.relationship('List', backref='board', lazy=True,
                            cascade="all,delete")

    def __init__(self, **kwargs):
        super(Board, self).__init__(**kwargs)

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        json_list = [i.serialize for i in self.labels]
        return {
            'id': self.id,
            'name': self.name,
            'team_id': self.team_id,
            'archived': self.archived,
            'labels': json_list
        }


class Label(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    color = db.Column(db.String(30))
    text = db.Column(db.String(50))

    def __init__(self, **kwargs):
        super(Label, self).__init__(**kwargs)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'color': self.color,
            'text': self.text,
        }


class List(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    board_id = db.Column(db.Integer, db.ForeignKey('board.id'), nullable=False)
    name = db.Column(db.String(50))
    cards = db.relationship('Card', backref='card', lazy=True,cascade="all,delete")

    def __init__(self, **kwargs):
        super(List, self).__init__(**kwargs)

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id': self.id,
            'name': self.name,
            'cards': [i.serialize for i in self.cards]
        }


class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    term = db.Column(db.DateTime, nullable=True)
    done = db.Column(db.Boolean, default=False)
    list_id = db.Column(db.Integer, db.ForeignKey('list.id'), nullable=False)
    lists_of_elements = db.relationship('Listofelements', backref='card', lazy=True)
    labels = db.relationship('Label', secondary=cards_and_labels, lazy='subquery',
                             backref=db.backref('cards', lazy=True))


    def __init__(self, **kwargs):
        super(Card, self).__init__(**kwargs)

    def __repr__(self):
        return '<Card %r>' % self.id

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id': self.id,
            'name': self.name,
            'content': self.content,
            'date_created': dump_datetime(self.date_created),
            'labels': [i.serialize for i in self.labels],
        }


class Listofelements(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    card_id = db.Column(db.Integer, db.ForeignKey('card.id'), nullable=False)
    name = db.Column(db.String(50))
    done = db.Column(db.Integer, default=0)

    def __init__(self, **kwargs):
        super(Listofelements, self).__init__(**kwargs)


class Element(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    done = db.Column(db.Boolean(False))
    list_of_elemets_id = db.Column(db.Integer, db.ForeignKey('listofelements.id'), nullable=False)

    def __init__(self, **kwargs):
        super(Element, self).__init__(**kwargs)


class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    boards = db.relationship('Board', backref='team', lazy=True)
    Name = db.Column(db.String(50))

    def __init__(self, **kwargs):
        super(Team, self).__init__(**kwargs)
