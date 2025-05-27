
from flask import Blueprint, render_template, session, redirect, url_for

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

@admin_bp.route("/dashboard")
def dashboard():
    user = session.get("user")
    if not user or not user.get("is_admin"):
        return redirect(url_for("auth.login"))
    return render_template("admin_dashboard.html", user=user)


from flask import request, send_file
import csv
import io
from sheets_api import get_all_records

@admin_bp.route("/logs")
def view_logs():
    user = session.get("user")
    if not user or not user.get("is_admin"):
        return redirect(url_for("auth.login"))

    logs = get_all_records("smart_logs")
    status = request.args.get("status")

    if status:
        logs = [log for log in logs if log.get("status") == status]

    return render_template("admin_logs.html", logs=logs)

@admin_bp.route("/logs/export")
def export_logs():
    user = session.get("user")
    if not user or not user.get("is_admin"):
        return redirect(url_for("auth.login"))

    status = request.args.get("status")
    logs = get_all_records("smart_logs")
    if status:
        logs = [log for log in logs if log.get("status") == status]

    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=logs[0].keys())
    writer.writeheader()
    writer.writerows(logs)
    output.seek(0)

    return send_file(io.BytesIO(output.getvalue().encode()), mimetype="text/csv", as_attachment=True, download_name="logs.csv")


@admin_bp.route("/analytics")
def analytics():
    user = session.get("user")
    if not user or not user.get("is_admin"):
        return redirect(url_for("auth.login"))

    users = get_all_records("users")
    logs = get_all_records("smart_logs")

    hours_by_student = {}
    activity_counts = {}
    daily_counts = {}

    for log in logs:
        sid = log.get("student_id", "unknown")
        hours = float(log.get("hours", 0)) if log.get("hours") else 0
        activity = log.get("activity", "unspecified")
        date = log.get("start", "").split("T")[0]

        hours_by_student[sid] = hours_by_student.get(sid, 0) + hours
        activity_counts[activity] = activity_counts.get(activity, 0) + 1
        daily_counts[date] = daily_counts.get(date, 0) + 1

    return render_template("admin_analytics.html",
                           hours_by_student=hours_by_student,
                           activity_counts=activity_counts,
                           daily_counts=daily_counts)
