
from flask import Blueprint, render_template, request, redirect, session, url_for, flash
import os

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

# In-memory placeholder for registered users
from sheets_api import append_row, find_by_email


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        surname = request.form["surname"]
        email = request.form["email"]
        grade = request.form["grade"]
        password = request.form["password"]
        admin_code = request.form.get("admin_code", "")

        is_admin = (admin_code == os.getenv("ADMIN_REGISTRATION_CODE"))
        
        append_row("users", [
            name, surname, email, grade, password, "admin" if is_admin else "student"
        ])

            "name": name, "surname": surname, "email": email,
            "grade": grade, "password": password, "is_admin": is_admin
        })

        flash("Registration successful. Please log in.")
        return redirect(url_for("auth.login"))
    return render_template("register.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        
        record = find_by_email("users", email)
        user = None
        if record and record.get("password") == password:
            user = {
                "name": record.get("name", ""),
                "surname": record.get("surname", ""),
                "email": record.get("email", ""),
                "grade": record.get("grade", ""),
                "is_admin": (record.get("role") == "admin")
            }

        if user:
            session["user"] = user
            if user["is_admin"]:
                return redirect(url_for("admin.dashboard"))
            else:
                return redirect(url_for("student.dashboard"))
        flash("Invalid credentials")
    return render_template("login.html")

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("public.home"))
