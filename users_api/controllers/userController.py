from flask import (
    Blueprint, flash, redirect, render_template, request, url_for
)
from users_api import db, cache
from sqlalchemy import func
from users_api.models.UserModel import User
from flask_marshmallow import Marshmallow
import hashlib

ma = Marshmallow(db)

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'firstname', 'lastname', 'username', 'email')

user_sch = UserSchema()
users_sch = UserSchema(many=True)
bp = Blueprint('users_api', __name__)

@bp.route('/')
def index():
    return 'Welcome to the API!'

@bp.route('/user/add', methods=["POST"])
def add_user():
    firstname = request.json["firstname"]
    lastname = request.json["lastname"]
    username = request.json["username"]
    email = request.json["email"]
    password = request.json["password"]
    password = hashlib.md5(password.encode('utf8')).hexdigest()
    
    new_user = User(firstname,lastname,username,email,password)
    db.session.add(new_user)
    db.session.commit()

    return user_sch.jsonify(new_user)

@bp.route('/user/<id>', methods=["GET"])
def get_user(id):
    user = User.query.get(id)
    return user_sch.jsonify(user)

@bp.route('/user/<id>', methods=["POST"])
def edit_user(id):
    user = User.query.get(id)
    
    firstname = request.json["firstname"]
    lastname = request.json["lastname"]
    username = request.json["username"]
    email = request.json["email"]
    
    user.firstname = firstname
    user.lastname = lastname
    user.username = username
    user.email = email
    
    db.session.commit()

    return user_sch.jsonify(user)

@bp.route('/user/changepsw/<id>', methods=["POST"])
def change_password(id):
    user = User.query.get(id)

    password = request.json["password"]
 
    user.password = hashlib.md5(password.encode('utf8')).hexdigest()
    
    db.session.commit()

    return "Password Changed"

@bp.route('/user/<id>', methods=["DELETE"])
def delete_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()

    return "Deleted"

@bp.route('/users')
@cache.cached(timeout=500)
def user_list():
    u_list = User.query.all()
    
    return users_sch.jsonify(u_list)

@bp.route('/users', methods=["POST"])
@cache.cached(timeout=50)
def filter_list():
    username = request.json.get("username", "No")
    firstname = request.json.get("firstname", "No")
    lastname = request.json.get("lastname", "No")
    email = request.json.get("email", "No")
    PAGE_NUMBER = request.json.get("PAGE_NUMBER", "No")
    ROWS_PER_PAGE = request.json.get("ROWS_PER_PAGE", "No")

    u_list = User.query

    if username != "No":
        u_list = u_list.filter_by(username = username)
    
    if firstname != "No":
        u_list = u_list.filter_by(firstname = firstname)

    if lastname != "No":
        u_list = u_list.filter_by(lastname = lastname)

    if email != "No":
        u_list = u_list.filter_by(email = email)

    if PAGE_NUMBER != "No" and ROWS_PER_PAGE != "No":
        if PAGE_NUMBER != 0:
            try:
                u_list.paginate(page=int(PAGE_NUMBER), per_page=int(ROWS_PER_PAGE))
            except:
                return ""
        else:
            u_list.all()
    else:
        u_list.all()

    return users_sch.jsonify(u_list)
    
