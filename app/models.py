from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app.extensions import db


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


class Project(db.Model):
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    tagline = db.Column(db.String(300), default="")
    description = db.Column(db.Text, default="")
    tech_stack = db.Column(db.String(300), default="")
    github_url = db.Column(db.String(500), default="")
    demo_url = db.Column(db.String(500), default="")
    image_url = db.Column(db.String(500), default="")
    featured = db.Column(db.Boolean, default=False)
    position = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "tagline": self.tagline,
            "description": self.description,
            "tech_stack": [
                t.strip() for t in (self.tech_stack or "").split(",") if t.strip()
            ],
            "github_url": self.github_url,
            "demo_url": self.demo_url,
            "image_url": self.image_url,
            "featured": self.featured,
            "position": self.position,
        }


class Certificate(db.Model):
    __tablename__ = "certificates"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    issuer = db.Column(db.String(200), default="")
    issue_date = db.Column(db.String(50), default="")
    credential_url = db.Column(db.String(500), default="")
    position = db.Column(db.Integer, default=0)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "issuer": self.issuer,
            "issue_date": self.issue_date,
            "credential_url": self.credential_url,
            "position": self.position,
        }


class Skill(db.Model):
    __tablename__ = "skills"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), default="General")
    level = db.Column(db.Integer, default=80)
    position = db.Column(db.Integer, default=0)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "level": self.level,
            "position": self.position,
        }


class Education(db.Model):
    __tablename__ = "education"

    id = db.Column(db.Integer, primary_key=True)
    institution = db.Column(db.String(200), nullable=False)
    degree = db.Column(db.String(200), default="")
    field = db.Column(db.String(200), default="")
    start_year = db.Column(db.String(20), default="")
    end_year = db.Column(db.String(20), default="")
    score = db.Column(db.String(50), default="")
    position = db.Column(db.Integer, default=0)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "institution": self.institution,
            "degree": self.degree,
            "field": self.field,
            "start_year": self.start_year,
            "end_year": self.end_year,
            "score": self.score,
            "position": self.position,
        }


class About(db.Model):
    """Single-row profile / hero / about content."""

    __tablename__ = "about"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(150), default="")
    headline = db.Column(db.String(250), default="")
    hero_subtitle = db.Column(db.String(400), default="")
    bio = db.Column(db.Text, default="")
    email = db.Column(db.String(200), default="")
    phone = db.Column(db.String(50), default="")
    location = db.Column(db.String(150), default="")
    github_url = db.Column(db.String(500), default="")
    linkedin_url = db.Column(db.String(500), default="")
    resume_filename = db.Column(db.String(300), default="")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "full_name": self.full_name,
            "headline": self.headline,
            "hero_subtitle": self.hero_subtitle,
            "bio": self.bio,
            "email": self.email,
            "phone": self.phone,
            "location": self.location,
            "github_url": self.github_url,
            "linkedin_url": self.linkedin_url,
            "resume_filename": self.resume_filename,
        }


class Message(db.Model):
    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    subject = db.Column(db.String(250), default="")
    body = db.Column(db.Text, default="")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "subject": self.subject,
            "body": self.body,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
