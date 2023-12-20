import os
from db import db
from flask import session, request, abort
from sqlalchemy import text
from werkzeug.security import check_password_hash, generate_password_hash

def login(username: str, password: str):
    sql = text("SELECT password, id, role FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    #if not check_password_hash(user[0], password):
    #    return False
    session["user_id"] = user[1]
    session["user_username"] = username
    session["user_role"] = user[2]
    #session["csrf_token"] = os.urandom(16).hex()
    return True

def logout():
    del session["user_id"]
    del session["user_username"]
    del session["user_role"]

def create_user(username: str, password: str, role: int):
    #Flaw 3
    #In the user creation the password hash is not generated
    #This should be corrected by adding the below mentioned lines, which are commented with #

    #hash_value = generate_password_hash(password)
    try:
        sql = text("""
                   INSERT INTO users (username, password, role) 
                   VALUES (:username, :password, :role)
                   """)
        db.session.execute(sql, {"username":username, "password":password, "role":role})
        #Password":hash_value should be used to use and store the hashed value
        db.session.commit()
    except:
        return False
    
    return login(username, password)

def get_all_users():
    sql = text("SELECT username, password FROM users")
    result = db.session.execute(sql)
    all_messages = result.fetchall()
    return all_messages

def user_exists(username: str):
    sql = text("SELECT username from users WHERE username=:username")
    result = db.session.execute(sql, {"username": username})
    existing_user = result.fetchone()

    if existing_user:
        return True

def get_user_role(user_id: int):
    sql = text("SELECT role FROM users WHERE id=:user_id")
    result = db.session.execute(sql, {"user_id":user_id})
    user = result.fetchone()
    if user:
        return user.role
    return None

def check_csrf():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)