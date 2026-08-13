# Portfolio

Personal portfolio site with a public page, a password-protected admin dashboard, and a Flask + SQLite REST backend.

```
Public site      /            hero, about, skills, projects, education, certifications, resume, contact
Admin dashboard  /admin       login, CRUD for projects / certificates / skills / education, about editor, resume upload
REST API         /api/...     JSON endpoints backing both
```

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env      # set SECRET_KEY, ADMIN_USERNAME, ADMIN_PASSWORD
python seed.py            # optional: load starter content
python run.py             # http://localhost:5000
```

The database is created automatically at `instance/portfolio.db` on first run, along with an
admin user from `ADMIN_USERNAME` / `ADMIN_PASSWORD` (defaults `admin` / `admin123` — change these).

## API

| Method | Endpoint | Auth | Description |
| --- | --- | --- | --- |
| GET | `/api/<resource>` | public | List `projects`, `certificates`, `skills` or `education` |
| POST | `/api/<resource>` | admin | Create an item |
| PUT | `/api/<resource>/<id>` | admin | Update an item |
| DELETE | `/api/<resource>/<id>` | admin | Delete an item |
| GET | `/api/about` | public | Profile / about content |
| PUT | `/api/about` | admin | Update profile / about content |
| POST | `/api/contact` | public | Submit a contact message |
| GET | `/api/messages` | admin | List contact messages |

Resume is uploaded at `POST /admin/resume` (multipart) and served at `/resume`.

## Layout

```
app/
  __init__.py      app factory, db bootstrap, admin bootstrap
  config.py        configuration
  extensions.py    db + login manager
  models.py        User, Project, Certificate, Skill, Education, About, Message
  views/
    public.py      public site + resume download
    admin.py       login/logout, dashboard, resume upload
    api.py         generic REST CRUD + about + contact
  templates/       public/index.html, admin/login.html, admin/dashboard.html
  static/          css/, js/, uploads/
run.py             entrypoint
seed.py            starter content
```
