from flask import Blueprint, render_template, request, jsonify, redirect
from helpers import token_required
from models import db, User, Note, Friend, note_schema, notes_schema, friend_schema, friends_schema, user_schema, users_schema

api = Blueprint('api', __name__, url_prefix="/api")

@api.route("/signin", methods=["POST"])
def signin():
    email = request.json["email"]
    username = request.json["username"]
    user_token = request.json["token"]

    user = User(email, username, user_token)

    db.session.add(user)
    db.session.commit()

    response = user_schema.dump(user)
    return jsonify(response)

@api.route("/update", methods=["PUT"])
@token_required
def update(user_token):
    user = User.query.filter_by(token = user_token.token).first()
    user.username = request.json["username"]
    user.bestScore = request.json["best"]
    user.favCourse = request.json["favorite"]
    user.handicap = request.json["handicap"]

    db.session.commit()

    response = user_schema.dump(user)
    return jsonify(response)

@api.route("/addPic", methods=["PUT"])
@token_required
def updatePic(user_token):
    user = User.query.filter_by(token = user_token.token).first()
    user.profileURL = request.json["profilePic"]

    db.session.commit()

    response = user_schema.dump(user)
    return jsonify(response)

@api.route("/addNote", methods=["POST"])
@token_required
def addNote(user_token):
    message = request.json["message"]
    note = Note(message, user_token.token)

    db.session.add(note)
    db.session.commit()

    response = note_schema.dump(note)
    return jsonify(response)

@api.route("/deleteNote/<id>", methods=["DELETE"])
@token_required
def deleteNote(user_token, id):
    note = Note.query.get(id)

    db.session.delete(note)
    db.session.commit()

    response = note_schema.dump(note)
    return jsonify(response)

@api.route("/getNotes", methods=["GET"])
@token_required
def getNotes(token):
    notes = Note.query.filter_by(user_token = token.token)

    response = notes_schema.dump(notes)
    return jsonify(response)

@api.route("/addFriend/<id>", methods=["POST"])
@token_required
def addFriend(token, id):
    friend = Friend(token.token, id)

    db.session.add(friend)
    db.session.commit()

    response = friend_schema.dump(friend)
    return jsonify(response)

@api.route("/getFriends", methods=["GET"])
@token_required
def getFriends(token):
    friends = Friend.query.filter_by(user = token.token)

    response = friends_schema.dump(friends)
    return jsonify(response)

@api.route("/removeFriend/<id>", methods=["DELETE"])
@token_required
def removeFriend(token, id):
    friend = Friend.query.get(id)

    db.session.delete(friend)
    db.session.commit()

    response = friend_schema.dump(friend)
    return jsonify(response)

@api.route("/getUser/<id>", methods=["GET"])
def getUser(id):
    user = User.query.get(id)

    response = user_schema.dump(user)
    return jsonify(response)

@api.route("/getUser", methods=["GET"])
@token_required
def getUserInfo(user_token):
    user = User.query.filter_by(token = user_token.token).first()

    response = user_schema.dump(user)
    return jsonify(response)

@api.route("/getUser/search", methods=["POST"])
def getUserSearch():
    search = request.json["Username"]
    print(search)
    user = User.query.filter(User.username.like(f"%{search}%")).all()

    response = users_schema.dump(user)
    return jsonify(response)

@api.route("/getUsers", methods=["GET"])
def getUsers():
    users = User.query.all()

    response = users_schema.dump(users)
    return jsonify(response)


