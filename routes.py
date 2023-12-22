from app import app
from flask import render_template, redirect, request, session, flash
import users, messages
import re

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
        password2 = request.form["password2"]
        email = request.form["email"]
        role = request.form["role"]

        if not (3 <= len(username) <= 25):
            flash("Username should be between 1-25 characters.")
            return render_template("register.html")
        
        if users.user_exists(username):
            flash("Username is already taken.")
            return render_template("register.html")
        
        if not (5 <= len(email) <= 40):
            flash("email should be between 5-40 characters.")
            return render_template("register.html")

        if password1 != password2:
            flash("Given passwords are not the same.")
            return render_template("register.html")
        
        if password1 == "":
            flash("Password is empty.")
            return render_template("register.html")
        
        if not (5 <= len(password1) <= 25) or not re.search("[0-9]", password1) or not re.search("[A-Z]", password1):
            flash("Password should be between 5-25 characters and contain number and capital letter")
            return render_template("register.html")
                
        if role not in ("1", "2"):
            flash("Unknown user type.")
            return render_template("register.html")
        
        if users.create_user(username, email, password1,  role):
            flash("User created succesfully, you are now logged in", "success")
            user_id = session.get("user_id")
            user_role = users.get_user_role(user_id)
            session["role"] = user_role
            return redirect("/messages")
    
    return render_template("register.html")

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

@app.route("/messages", methods=["GET", "POST"])
def show_messages():
    if request.method == "GET":
        all_messages = messages.get_all_messages()
        return render_template("messages.html", messages=all_messages)
    
@app.route("/messages/new_message", methods=["GET", "POST"])
def send_message():
    if request.method == "GET":
        return render_template("new_message.html")
    
    if request.method == "POST":
        #Flaw 2
        #This demonstrates the CSRF-flaw
        #Even the messages.html has hidden input form for CSRF, it is never called in the routes
        #Also even the function is available in the users.py, it is not called here
        #Also, users.py should have this function so that routes.py can call it
        #This POST method should have this function calling:
        #users.check_csrf()

        content = request.form["content"]
        creator_id = session.get("user_id")

        if creator_id is None:
            flash("Failed to add message. User not authenticated.")
            return render_template("new_message.html")

        if messages.new_message(content,creator_id):
            return redirect("/messages")
        else:
            flash("failed to add message")
            return render_template("new_message.html")

@app.route("/update", methods=["GET", "POST"])
def update():
    if request.method == "GET":
        return render_template("update.html")
        
@app.route("/logout")
def logout():
     users.logout()
     return redirect("/login")

@app.route("/admin", methods=["GET", "POST"])
def show_admin():
    if request.method == "GET":
        all_users = users.get_all_users()
        all_messages = messages.get_all_messages()
        return render_template("admin.html", users=all_users, messages=all_messages)
    
        #Flaw 4
        #Admin buttons are not shown if the user is regular user in the messages page, but
        #regular user can see the admin page if he/she tries to change the URL to /Admin
        #Below is code which would deny the access if the user is not admin
    
    # if request.method == "GET":    
    #     user_id = session.get("user_id")
    #     user_role = users.get_user_role(user_id)
    #     if user_role and user_role == 2:
    #        all_users = users.get_all_users()
    #        all_messages = messages.get_all_messages()
    #        return render_template("admin.html", users=all_users, messages=all_messages)
    #     else:
    #        flash("Access denied. The page is only for admin users.", "error")
    #        return redirect("/messages")
           
    if request.method == "POST":
        #Flaw2, same as in below line 84
        #Flaw4
        #This is a bad access control as it is not checked if the user is really admin
        #below check should be added:
        #users.check_csrf()
        #users.require_role(2)

        user_id = request.form["user_id"]
        username = users.get_username(user_id)

        if users.delete_user(user_id):
            all_users = users.get_all_users()

            if not all_users:
                flash("All users deleted, please create a new one.")
                return redirect ("/login")
                     
            flash(f"User {username} deleted successfully")
            
        else:
            flash("Failed to delete user, try again")

        return redirect("/admin")
        

