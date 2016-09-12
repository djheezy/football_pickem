
from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    wager = db.relationship('Wager', lazy='dynamic')

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)
        except NameError:
            return str(self.id)

    def __repr__(self):
        return '<User %r>' % (self.nickname)


class Wager(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    week_num = db.Column(db.Integer)
    over_under = db.Column(db.Float)
    spread = db.Column(db.Float)
    favorite = db.Column(db.String(100))

    wager_type = db.Column(db.String(40))
    wager_team = db.Column(db.String(100))
    wager_amount = db.Column(db.Float)
    winnings = db.Column(db.Float)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post %r>' % (self.body)
