# Elevate-workspace

> **Unit 22: Application Development** | ISMT Nepal | Level 5

A Django-based Job Portal that connects **job seekers** with **companies** through a centralized, role-based web platform.

---

## 🚀 Features

- **Job Seekers** — Register, browse/search jobs, apply with CV, track application status
- **Company Admins** — Post/manage job listings, review applicants, update application status
- **Role-based Access Control** — Secure decorators for each user type
- **Django Admin Panel** — Full database management via `/admin`
- **Responsive UI** — Bootstrap 5 with clean, professional design
- **CSRF Protection** — Secure POST routes on all forms

---

## 🗂️ Project Structure

```
Elevate-workspace/
│
├─ manage.py              # Django entry point
├─ requirements.txt       # Python dependencies
├─ .gitignore
├─ README.md
│
├─ jobportal/             # Django project settings package
│   ├─ settings.py
│   ├─ urls.py
│   ├─ wsgi.py
│   └─ asgi.py
│
├─ jobs/                  # Main application
│   ├─ models.py          # User, Profile, Company, Job, Application
│   ├─ views.py           # All views (home, auth, dashboard, apply)
│   ├─ urls.py
│   ├─ decorators.py      # Role-based access decorators
│   ├─ forms.py
│   └─ context_processors.py
│
├─ templates/             # HTML templates (Django templating)
│   ├─ base.html
│   ├─ home.html
│   ├─ dashboard/
│   └─ jobs/
│
└─ static/                # CSS, JS, image assets
```

---

## ⚙️ Installation & Setup

### Prerequisites
- Python 3.11+
- pip

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/Anush12343/Elevate-workspace.git
cd Elevate-workspace

# 2. Create and activate a virtual environment
python -m venv venv
# Windows:
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Apply database migrations
python manage.py migrate

# 5. Create a superuser (admin)
python manage.py createsuperuser

# 6. Run the development server
python manage.py runserver
```

Visit **http://127.0.0.1:8000** in your browser.

---

## 🌐 Deployment (PythonAnywhere)

The project is configured for deployment at:  
`https://RYzen.pythonanywhere.com`

Key production settings:
- `DEBUG` is automatically `False` when not running `runserver`
- `ALLOWED_HOSTS` includes the PythonAnywhere domain
- `CSRF_TRUSTED_ORIGINS` is configured for HTTPS
- Run `python manage.py collectstatic` before deploying

---

## 🏗️ Architecture

- **Pattern**: Django MVT (Model-View-Template)
- **Database**: SQLite (development) → PostgreSQL (production)
- **Auth**: Django built-in `auth` + custom role decorators
- **Models**: `User`, `Profile`, `Company`, `Job`, `Application`

---

## 📋 Assignment Details

| Field | Value |
|-------|-------|
| **Unit** | Unit 22: Application Development (Y/618/7436) |
| **Level** | 5 (Core) |
| **Student** | Anusharan Bhattarai |
| **Assessor** | Bhuwan Subedi |
| **Institution** | ISMT Nepal |
| **Submission** | July 15, 2026 |

---

## 📄 License

feel free to use
