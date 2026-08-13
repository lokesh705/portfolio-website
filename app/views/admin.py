import os

from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.utils import secure_filename

from app.extensions import db
from app.models import About, Certificate, Education, Message, Project, Skill, User

admin_bp = Blueprint("admin", __name__)

ALLOWED_RESUME_EXTENSIONS = {".pdf", ".doc", ".docx"}


@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("admin.dashboard"))
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(request.args.get("next") or url_for("admin.dashboard"))
        flash("Invalid username or password", "error")
    return render_template("admin/login.html")


@admin_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("admin.login"))


@admin_bp.route("/")
@login_required
def dashboard():
    about = About.query.first()
    return render_template(
        "admin/dashboard.html",
        about=about,
        counts={
            "projects": Project.query.count(),
            "certificates": Certificate.query.count(),
            "skills": Skill.query.count(),
            "education": Education.query.count(),
            "messages": Message.query.count(),
        },
    )


@admin_bp.route("/resume", methods=["POST"])
@login_required
def upload_resume():
    file = request.files.get("resume")
    if not file or not file.filename:
        flash("No file selected", "error")
        return redirect(url_for("admin.dashboard"))
    extension = os.path.splitext(file.filename)[1].lower()
    if extension not in ALLOWED_RESUME_EXTENSIONS:
        flash("Only PDF or Word documents are allowed", "error")
        return redirect(url_for("admin.dashboard"))
    filename = secure_filename(f"resume{extension}")
    file.save(os.path.join(current_app.config["UPLOAD_FOLDER"], filename))
    about = About.query.first()
    if about is None:
        about = About()
        db.session.add(about)
    about.resume_filename = filename
    db.session.commit()
    flash("Resume uploaded", "success")
    return redirect(url_for("admin.dashboard"))
