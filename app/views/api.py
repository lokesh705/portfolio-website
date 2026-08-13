from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required

from app.extensions import db
from app.models import About, Certificate, Education, Message, Project, Skill

api_bp = Blueprint("api", __name__)


PUBLIC_ENDPOINTS = {"api.contact", "api.list_resource", "api.get_about"}


@api_bp.before_request
def require_admin():
    """Return 401 JSON instead of redirecting to the login page."""
    if request.endpoint in PUBLIC_ENDPOINTS:
        return None
    if not current_user.is_authenticated:
        return jsonify({"error": "authentication required"}), 401
    return None


MODELS = {
    "projects": Project,
    "certificates": Certificate,
    "skills": Skill,
    "education": Education,
}

EDITABLE_FIELDS = {
    Project: [
        "title",
        "tagline",
        "description",
        "tech_stack",
        "github_url",
        "demo_url",
        "image_url",
        "featured",
        "position",
    ],
    Certificate: ["name", "issuer", "issue_date", "credential_url", "position"],
    Skill: ["name", "category", "level", "position"],
    Education: [
        "institution",
        "degree",
        "field",
        "start_year",
        "end_year",
        "score",
        "position",
    ],
    About: [
        "full_name",
        "headline",
        "hero_subtitle",
        "bio",
        "email",
        "phone",
        "location",
        "github_url",
        "linkedin_url",
    ],
}


def apply_payload(instance, payload: dict):
    for field in EDITABLE_FIELDS[type(instance)]:
        if field in payload:
            setattr(instance, field, payload[field])
    return instance


@api_bp.route("/<resource>", methods=["GET"])
def list_resource(resource: str):
    model = MODELS.get(resource)
    if model is None:
        return jsonify({"error": "unknown resource"}), 404
    items = model.query.order_by(model.position.asc(), model.id.asc()).all()
    return jsonify([item.to_dict() for item in items])


@api_bp.route("/<resource>", methods=["POST"])
@login_required
def create_resource(resource: str):
    model = MODELS.get(resource)
    if model is None:
        return jsonify({"error": "unknown resource"}), 404
    instance = apply_payload(model(), request.get_json(silent=True) or {})
    db.session.add(instance)
    db.session.commit()
    return jsonify(instance.to_dict()), 201


@api_bp.route("/<resource>/<int:item_id>", methods=["PUT"])
@login_required
def update_resource(resource: str, item_id: int):
    model = MODELS.get(resource)
    if model is None:
        return jsonify({"error": "unknown resource"}), 404
    instance = db.session.get(model, item_id)
    if instance is None:
        return jsonify({"error": "not found"}), 404
    apply_payload(instance, request.get_json(silent=True) or {})
    db.session.commit()
    return jsonify(instance.to_dict())


@api_bp.route("/<resource>/<int:item_id>", methods=["DELETE"])
@login_required
def delete_resource(resource: str, item_id: int):
    model = MODELS.get(resource)
    if model is None:
        return jsonify({"error": "unknown resource"}), 404
    instance = db.session.get(model, item_id)
    if instance is None:
        return jsonify({"error": "not found"}), 404
    db.session.delete(instance)
    db.session.commit()
    return jsonify({"deleted": item_id})


@api_bp.route("/about", methods=["GET"])
def get_about():
    about = About.query.first()
    return jsonify(about.to_dict() if about else {})


@api_bp.route("/about", methods=["PUT"])
@login_required
def update_about():
    about = About.query.first()
    if about is None:
        about = About()
        db.session.add(about)
    apply_payload(about, request.get_json(silent=True) or {})
    db.session.commit()
    return jsonify(about.to_dict())


@api_bp.route("/contact", methods=["POST"])
def contact():
    payload = request.get_json(silent=True) or {}
    name = (payload.get("name") or "").strip()
    email = (payload.get("email") or "").strip()
    body = (payload.get("body") or "").strip()
    if not (name and email and body):
        return jsonify({"error": "name, email and body are required"}), 400
    message = Message(
        name=name,
        email=email,
        subject=(payload.get("subject") or "").strip(),
        body=body,
    )
    db.session.add(message)
    db.session.commit()
    return jsonify({"ok": True, "id": message.id}), 201


@api_bp.route("/messages", methods=["GET"])
@login_required
def list_messages():
    items = Message.query.order_by(Message.created_at.desc()).all()
    return jsonify([item.to_dict() for item in items])
