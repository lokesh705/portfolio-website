"""Populate the database with the portfolio's initial content."""

from app import create_app
from app.extensions import db
from app.models import About, Certificate, Education, Project, Skill

PROJECTS = [
    {
        "title": "Travel Mate AI",
        "tagline": "AI travel companion that plans personalised itineraries",
        "description": (
            "An AI-powered trip planner that generates day-by-day itineraries from a "
            "destination, budget and travel style, with live place recommendations and "
            "an interactive chat assistant."
        ),
        "tech_stack": "Python, Flask, LLM APIs, React, SQLite",
        "featured": True,
        "position": 0,
    },
    {
        "title": "AI Job Recommendation",
        "tagline": "Resume-aware job matching engine",
        "description": (
            "Parses a candidate resume, embeds skills and experience, and ranks open "
            "roles by semantic similarity with explainable match scores."
        ),
        "tech_stack": "Python, NLP, scikit-learn, Flask, Pandas",
        "position": 1,
    },
    {
        "title": "Flight Price Prediction",
        "tagline": "ML model forecasting airfare trends",
        "description": (
            "Regression models trained on historical fare data to predict ticket prices "
            "from route, airline, stops and booking window, served through a web app."
        ),
        "tech_stack": "Python, scikit-learn, XGBoost, Flask, Matplotlib",
        "position": 2,
    },
]

SKILLS = [
    ("Python", "Languages", 90, 0),
    ("JavaScript", "Languages", 75, 1),
    ("SQL", "Languages", 80, 2),
    ("Flask", "Frameworks", 88, 3),
    ("React", "Frameworks", 70, 4),
    ("scikit-learn", "AI / ML", 82, 5),
    ("Pandas / NumPy", "AI / ML", 85, 6),
    ("NLP & LLM APIs", "AI / ML", 78, 7),
    ("SQLite / PostgreSQL", "Data", 80, 8),
    ("Git & GitHub", "Tools", 85, 9),
    ("Docker", "Tools", 65, 10),
]

EDUCATION = [
    {
        "institution": "Your University",
        "degree": "B.Tech",
        "field": "Computer Science and Engineering",
        "start_year": "2021",
        "end_year": "2025",
        "score": "CGPA 8.5",
        "position": 0,
    }
]

CERTIFICATES = [
    {"name": "Machine Learning Specialization", "issuer": "Coursera", "issue_date": "2024", "position": 0},
    {"name": "Python for Data Science", "issuer": "NPTEL", "issue_date": "2023", "position": 1},
]

ABOUT = {
    "full_name": "Lokesh Geriki",
    "headline": "AI / Full-Stack Developer",
    "hero_subtitle": "I build AI-powered products and clean, fast web applications.",
    "bio": (
        "I am a developer focused on applied AI and full-stack engineering. I enjoy taking "
        "an idea from a rough concept to a deployed product - designing the data model, "
        "training the model, and shipping the interface around it."
    ),
    "email": "lokesh.geriki28@gmail.com",
    "location": "India",
    "github_url": "https://github.com/lokesh705",
    "linkedin_url": "",
}


def seed() -> None:
    app = create_app()
    with app.app_context():
        about = About.query.first() or About()
        for key, value in ABOUT.items():
            setattr(about, key, value)
        db.session.add(about)

        if Project.query.count() == 0:
            db.session.add_all(Project(**data) for data in PROJECTS)
        if Skill.query.count() == 0:
            db.session.add_all(
                Skill(name=name, category=category, level=level, position=position)
                for name, category, level, position in SKILLS
            )
        if Education.query.count() == 0:
            db.session.add_all(Education(**data) for data in EDUCATION)
        if Certificate.query.count() == 0:
            db.session.add_all(Certificate(**data) for data in CERTIFICATES)

        db.session.commit()
    print("Seed complete.")


if __name__ == "__main__":
    seed()
