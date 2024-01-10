from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid
from datetime import datetime
from flask_login import UserMixin
from flask_marshmallow import Marshmallow
import secrets

db = SQLAlchemy()
ma = Marshmallow()

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    bestScore = db.Column(db.String(100), nullable=True)
    handicap = db.Column(db.String(100), nullable=True)
    favCourse = db.Column(db.String(100), nullable=True)
    token = db.Column(db.String, nullable=False, unique=True)

    def __init__(self, email, username, token):
        self.id = self.set_id()
        self.email = email
        self.username = username
        self.token = token

    def set_id(self):
        return str(uuid.uuid4())
        
    
class Note(db.Model):
    id = db.Column(db.String, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    note = db.Column(db.Text, nullable=False)
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable=False)

    def __init__(self, note, token):
        self.id = self.set_id()
        self.note = note
        self.user_token = token

    def set_id(self):
        return str(uuid.uuid4())

class Friend(db.Model):
    id = db.Column(db.String, primary_key=True)
    user = db.Column(db.String, db.ForeignKey('user.token'), nullable=False)
    friend_id = db.Column(db.String, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, user_token, id):
        self.id = self.set_id()
        self.user = user_token
        self.friend_id = id

    def set_id(self):
        return str(uuid.uuid4())
    
class NoteSchema(ma.Schema):
    class Meta:
        fields = ['id', 'date', 'note', 'user_token']

class FriendSchema(ma.Schema):
    class Meta:
        fields = ['id', 'user', 'friend_id']

class UserSchema(ma.Schema):
    class Meta:
        fields = ['id', 'username', 'email', 'token', 'bestScore', 'handicap', 'favCourse']

note_schema = NoteSchema()
notes_schema = NoteSchema(many=True)

friend_schema = FriendSchema()
friends_schema = FriendSchema(many=True)

user_schema = UserSchema()
users_schema = UserSchema(many=True)

