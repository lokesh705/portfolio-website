import io

import pytest

from app import create_app
from app.config import Config
from app.extensions import db


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    SECRET_KEY = "test"
    ADMIN_USERNAME = "admin"
    ADMIN_PASSWORD = "secret"
    WTF_CSRF_ENABLED = False


@pytest.fixture
def app(tmp_path):
    TestConfig.UPLOAD_FOLDER = str(tmp_path)
    app = create_app(TestConfig)
    yield app
    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def admin(client):
    client.post("/admin/login", data={"username": "admin", "password": "secret"})
    return client


def test_public_page_renders(client):
    response = client.get("/")
    assert response.status_code == 200


def test_admin_requires_login(client):
    assert client.get("/admin/").status_code == 302


def test_login_and_dashboard(admin):
    assert admin.get("/admin/").status_code == 200


def test_login_rejects_bad_password(client):
    response = client.post(
        "/admin/login",
        data={"username": "admin", "password": "nope"},
        follow_redirects=True,
    )
    assert b"Invalid username or password" in response.data


@pytest.mark.parametrize(
    ("resource", "payload", "key"),
    [
        (
            "projects",
            {"title": "Travel Mate AI", "tech_stack": "Flask, React"},
            "title",
        ),
        ("certificates", {"name": "ML Specialization", "issuer": "Coursera"}, "name"),
        ("skills", {"name": "Python", "level": 90}, "name"),
        ("education", {"institution": "Uni", "degree": "B.Tech"}, "institution"),
    ],
)
def test_crud_cycle(admin, resource, payload, key):
    created = admin.post(f"/api/{resource}", json=payload).get_json()
    assert created[key] == payload[key]

    updated = admin.put(
        f"/api/{resource}/{created['id']}", json={key: "Renamed"}
    ).get_json()
    assert updated[key] == "Renamed"

    assert len(admin.get(f"/api/{resource}").get_json()) == 1

    assert admin.delete(f"/api/{resource}/{created['id']}").status_code == 200
    assert admin.get(f"/api/{resource}").get_json() == []


@pytest.mark.parametrize(
    "resource", ["projects", "certificates", "skills", "education"]
)
def test_writes_require_auth(client, resource):
    assert (
        client.post(f"/api/{resource}", json={"name": "x", "title": "x"}).status_code
        == 401
    )
    assert client.put(f"/api/{resource}/1", json={}).status_code == 401
    assert client.delete(f"/api/{resource}/1").status_code == 401


def test_reads_are_public(client):
    assert client.get("/api/projects").status_code == 200
    assert client.get("/api/about").status_code == 200


def test_unknown_resource(admin):
    assert admin.get("/api/unicorns").status_code == 404


def test_about_update(admin):
    response = admin.put("/api/about", json={"full_name": "Lokesh", "headline": "Dev"})
    assert response.get_json()["full_name"] == "Lokesh"
    assert admin.get("/api/about").get_json()["headline"] == "Dev"


def test_contact_flow(app, client):
    assert client.post("/api/contact", json={"name": "A"}).status_code == 400
    created = client.post(
        "/api/contact", json={"name": "A", "email": "a@b.c", "body": "hello"}
    )
    assert created.status_code == 201
    assert client.get("/api/messages").status_code == 401

    admin = app.test_client()
    admin.post("/admin/login", data={"username": "admin", "password": "secret"})
    assert len(admin.get("/api/messages").get_json()) == 1


def test_resume_upload_and_download(admin):
    assert admin.get("/resume").status_code == 404
    admin.post(
        "/admin/resume",
        data={"resume": (io.BytesIO(b"%PDF-1.4"), "cv.pdf")},
        content_type="multipart/form-data",
    )
    assert admin.get("/resume").status_code == 200


def test_resume_rejects_bad_extension(admin):
    response = admin.post(
        "/admin/resume",
        data={"resume": (io.BytesIO(b"nope"), "cv.exe")},
        content_type="multipart/form-data",
        follow_redirects=True,
    )
    assert b"Only PDF or Word documents are allowed" in response.data
    assert admin.get("/resume").status_code == 404


def test_logout(admin):
    admin.get("/admin/logout")
    assert admin.get("/admin/").status_code == 302
