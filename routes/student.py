
from flask import Blueprint, render_template, session, redirect, url_for

student_bp = Blueprint("student", __name__, url_prefix="/student")

@student_bp.route("/dashboard")
from logs_api import expire_old_logs
@student_bp.route("/dashboard")
from sheets_api import get_all_records
@student_bp.route("/dashboard")
def dashboard():
    expire_old_logs()
    user = session.get("user")
    if not user or user.get("is_admin"):
        return redirect(url_for("auth.login"))
    
from flask import request
from logs_api import log_start, log_stop
from utils import get_client_ip, get_device_info

@student_bp.route("/start-log", methods=["POST"])
def start_log():
    user = session.get("user")
    if not user:
        return redirect(url_for("auth.login"))

    activity = request.form["activity"]
    ip = get_client_ip()
    device = get_device_info()
    location = request.form.get("location", "unknown")

    start_time = log_start(user["email"], activity, ip, location, str(device))
    session["start_time"] = start_time
    session["activity"] = activity
    return redirect(url_for("student.dashboard"))

@student_bp.route("/stop-log", methods=["POST"])
def stop_log():
    user = session.get("user")
    if not user:
        return redirect(url_for("auth.login"))

    activity = session.get("activity")
    start_time = session.get("start_time")
    ip = get_client_ip()
    device = get_device_info()
    location = request.form.get("location", "unknown")

    from logs_api import get_registered_device, is_suspicious
    registered_device, registered_location = get_registered_device(user["email"])
    status, reason = is_suspicious(str(device), location, registered_device, registered_location)
    end_time, duration = log_stop(user["email"], activity, start_time, ip, location, str(device))

    session.pop("start_time", None)
    session.pop("activity", None)
    return redirect(url_for("student.dashboard"))


    
    logs = get_all_records("smart_logs")
    student_logs = [log for log in logs if log.get("student_id") == user["email"]]

    flagged_logs = [log for log in student_logs if log.get("status") == "flagged"]
    expired_logs = [log for log in student_logs if log.get("status") == "expired"]

    alert_message = None
    if flagged_logs:
        alert_message = f"You have {len(flagged_logs)} flagged log(s) that may need review."
    elif expired_logs:
        alert_message = f"You have {len(expired_logs)} expired log(s) — make sure to stop future logs in time."

    return render_template("student_dashboard.html", user=user, alert_message=alert_message)


from sheets_api import get_all_records

@student_bp.route("/my-logs")
def my_logs():
    user = session.get("user")
    if not user:
        return redirect(url_for("auth.login"))

    logs = get_all_records("smart_logs")
    my_logs = [log for log in logs if log.get("student_id") == user["email"]]
    return render_template("my_logs.html", logs=my_logs)


@student_bp.route("/calendar")
def calendar():
    user = session.get("user")
    if not user:
        return redirect(url_for("auth.login"))

    logs = get_all_records("smart_logs")
    my_logs = [log for log in logs if log.get("student_id") == user["email"]]

    events = []
    for log in my_logs:
        if log.get("start"):
            events.append({
                "title": log.get("activity", "Logged"),
                "start": log.get("start").split("T")[0]
            })

    return render_template("student_calendar.html", events=events)
