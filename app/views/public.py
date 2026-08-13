from flask import Blueprint, abort, current_app, render_template, send_from_directory

from app.models import About, Certificate, Education, Project, Skill

public_bp = Blueprint("public", __name__)


@public_bp.route("/")
def index():
    about = About.query.first()
    projects = Project.query.order_by(
        Project.featured.desc(), Project.position.asc(), Project.id.asc()
    ).all()
    skills = Skill.query.order_by(Skill.position.asc(), Skill.id.asc()).all()
    categories: dict[str, list[Skill]] = {}
    for skill in skills:
        categories.setdefault(skill.category or "General", []).append(skill)
    education = Education.query.order_by(
        Education.position.asc(), Education.id.asc()
    ).all()
    certificates = Certificate.query.order_by(
        Certificate.position.asc(), Certificate.id.asc()
    ).all()
    return render_template(
        "public/index.html",
        about=about,
        projects=projects,
        skill_categories=categories,
        education=education,
        certificates=certificates,
    )


@public_bp.route("/resume")
def resume():
    about = About.query.first()
    if not about or not about.resume_filename:
        abort(404)
    return send_from_directory(
        current_app.config["UPLOAD_FOLDER"], about.resume_filename, as_attachment=False
    )
