from app import app
from flask import render_template, redirect, request, session, flash
import users

@app.route("/")
def index():
    return redirect("/login")

@app.route("/register", methods=["GET", "POST"])
def create_user():
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form ["password2"]
        role = request.form["role"]

        if not (3 <= len(username) <= 25):
            flash("Username should be between 1-25 characters.")
            return render_template("register.html")
        
        if users.user_exists(username):
            flash("Username is already taken.")
            return render_template("register.html")
        
        if not ( 5 <= len(password1) <= 25):
            flash("Password should be between 5-25 characters.")
            return render_template("register.html")
        
        if password1 != password2:
            flash("Given passwords are not the same.")
            return render_template("register.html")
        
        if password1 == "":
            flash("Password is empty.")
            return render_template("register.html")
        
        if role not in ("1", "2"):
            flash("Unknown user type.")
            return render_template("register.html")
        
        if not users.create_user(username, password1, role):
            flash("Registration not succesfull, check username and password.")
            return render_template("register.html")
    
        flash("User created succesfully, you can login now!", "success")
        return redirect("/login")
    
    return render_template("register.html")

@app.route("/messages")
def messages():
    return render_template("/messages.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password1"]

    if not users.login(username, password):
        flash("Wrong username, password or no user created.")
        return render_template("login.html")

    user_id = session.get("user_id")
    user_role = users.get_user_role(user_id)
    session["creator_id"] = user_id
    if user_role:
        session["role"] = user_role

    return redirect("/messages")