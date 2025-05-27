
from flask import Blueprint, render_template

public_bp = Blueprint("public", __name__)

@public_bp.route("/")
def home():
    return render_template("home.html")

@public_bp.route("/leaderboard")
def leaderboard():
    
from sheets_api import get_all_records

users = get_all_records("users")
sorted_users = sorted(users, key=lambda x: float(x.get("hours", 0)), reverse=True)
leaderboard = []
for u in sorted_users:
    leaderboard.append({
        "name": u.get("name", ""),
        "surname": u.get("surname", ""),
        "grade": u.get("grade", ""),
        "hours": u.get("hours", 0)
    })
return render_template("leaderboard.html", leaderboard=leaderboard)

