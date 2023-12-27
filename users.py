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
    #Flaw 3, which is Cryptographic failure
    #the below mentioned if statement should be used

    #if not check_password_hash(user[0], password):
    #    return False

    session["user_id"] = user[1]
    session["user_username"] = username
    session["user_role"] = user[2]
    session["csrf_token"] = os.urandom(16).hex()
    return True

def logout():
    del session["user_id"]
    del session["user_username"]
    del session["user_role"]

def create_user(username: str, email: str, password: str, role: int):
    #Flaw 3, which is Cryptographic failure
    #In the user creation the password hash is not generated
    #This should be corrected by adding the below mentioned lines and password variable's parameter set to hash_value as mentioned in line 42.

    #hash_value = generate_password_hash(password)
    try:
        sql = text("""
                   INSERT INTO users (username, email, password, role) 
                   VALUES (:username, :email, :password, :role)
                   """)
        db.session.execute(sql, {"username":username, "email":email, "password":password, "role":role})
                                                                    #"password":hash_value should be used to use and store the hashed value
        db.session.commit()
    except:
        return False

    return login(username, password)

def get_all_users():
    sql = text("SELECT id, username, role FROM users")
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

def delete_user(user_id: int):
    try:
        sql_messages = text("DELETE FROM messages WHERE creator_id=:user_id")
        db.session.execute(sql_messages, {"user_id": user_id})

        sql_user = text("DELETE FROM users WHERE id=:user_id")
        db.session.execute(sql_user, {"user_id": user_id})

        db.session.commit()
        return True
    except:
        return False

def get_username(user_id: int):
    sql = text("SELECT username FROM users WHERE id=:user_id")
    result = db.session.execute(sql, {"user_id": user_id}).fetchone()
    if result:
        return result[0]
    return None

def get_email(user_id: int):
    sql = text("SELECT email FROM users WHERE id=:user_id")
    result = db.session.execute(sql, {"user_id": user_id}).fetchone()
    if result:
        return result[0]
    return None

def get_user_id(user_id: int):
    sql = text("SELECT id, username FROM users WHERE id=:user_id")
    result = db.session.execute(sql, {"user_id":user_id})
    users = result.fetchone()
    return users

def update_email(email: str, user_id: int):
    #Flaw 5, which is injection.
    #Injection can happen when the SQL query does not use parameters as values
    #This is due that the user can change the structure of the query and make the user or all of the users admins
    #i.e. user can use the following type of query '; UPDATE users SET role = 2 WHERE id > 0; --
    #After this inserted in the email form if the user logs out and in the user has admin rights and can see admin buttons
    #In addition the update.html should have min and max lenghts for email

    sql = text("UPDATE users SET email='" + email + "' WHERE id=" + str(user_id))
    db.session.execute(sql)
    db.session.commit()

    #corrected query below, where the parameters are used so injection cannot happen

    # sql = text("UPDATE users SET email=:email WHERE id=:user_id")
    # db.session.execute(sql, {"email":email, "user_id":user_id})
    # db.session.commit()

def check_csrf():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

def require_role(role: int):
    if role > session.get("user_role", 0):
        abort(403)
