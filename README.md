# Acadvault — Assessment Portal 📚

A full-stack Django web application for managing and taking online quizzes. Acadvault provides a streamlined experience for both teachers (who create and manage content) and students (who take assessments and track their progress), complete with a **secure exam mode** that monitors for academic integrity violations.

🔗 **Live Demo:** [assessmentportal-seven.vercel.app](https://assessmentportal-seven.vercel.app)

---

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Database Setup](#database-setup)
  - [Running the Server](#running-the-server)
- [Environment Variables](#environment-variables)
- [User Roles](#user-roles)
- [URL Structure](#url-structure)
- [Deployment](#deployment)
- [Contributing](#contributing)

---

## Features

### For Students
- 📝 **Take Quizzes** — Browse available categories and start an assessment
- 🔒 **Secure Exam Mode** — Full-screen enforcement with tab-switch and window-blur detection
- 📊 **Personalized Dashboard** — View total attempts, average score, best score, and performance by subject
- 📈 **Improvement Tracking** — Detects upward or downward score trends over time
- 🧾 **Instant Results** — Detailed answer review with correct/incorrect feedback immediately after submission

### For Teachers / Admins
- 📂 **Category Management** — Create, edit, and delete quiz categories (e.g., Mathematics, Science)
- ❓ **Question Management** — Add multiple-choice questions (A/B/C/D) with a designated correct answer per category
- 📋 **Results Dashboard** — View all student attempts with filtering by category, student, date range, and flag status
- 🚩 **Academic Integrity Monitoring** — Attempts are automatically flagged when tab switches exceed 3 or fullscreen exits exceed 2
- 📤 **CSV Export** — Export filtered results to a downloadable CSV file
- 🗑️ **Result Management** — Delete individual attempts; drill into per-student history

### General
- 🌗 **Dark Mode** — System-aware theme that persists via localStorage
- 🔐 **Role-Based Access** — Teacher/admin views are protected with `@user_passes_test`
- 🛡️ **Anti-Cheating** — Right-click, copy/paste, and keyboard shortcuts disabled during secure quiz mode; 5-second auto-submit countdown on fullscreen exit
- 🕐 **Live Clock** — Real-time clock displayed on the landing page navbar

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.12 |
| Framework | Django 5.x |
| Database | PostgreSQL (Supabase) |
| Frontend | HTML5, Django Templates, Tailwind CSS (CDN) |
| Static Files | WhiteNoise |
| Deployment | Vercel (WSGI via `@vercel/python`) |

---

## Project Structure

```
acadvault/
│
├── quiz_app/                  # Django project root
│   ├── settings.py            # Configuration (DB, static files, security)
│   ├── urls.py                # Root URL routing
│   ├── wsgi.py                # WSGI entry point (also used by Vercel)
│   └── asgi.py
│
├── accounts/                  # Authentication app
│   ├── views.py               # Landing page, login, register
│   ├── urls.py                # /, /login/, /register/
│   ├── models.py              # Category, Question, Answer, Profile (legacy)
│   └── templates/accounts/
│       ├── home.html          # Landing page
│       ├── login.html
│       └── register.html
│
├── home/                      # Core quiz app
│   ├── models.py              # Category, Question, QuizAttempt, Profile_Type
│   ├── views.py               # Dashboard, quiz, results, admin management
│   ├── urls.py                # All /subjects/... routes
│   ├── admin.py               # Django Admin customizations with security display
│   ├── migrations/            # Database migrations
│   └── templates/home/
│       ├── dashboard.html
│       ├── select_category.html
│       ├── start_quiz_secure.html   # Secure exam mode
│       ├── evaluation.html          # Post-quiz results
│       ├── manage_categories.html
│       ├── add_category.html
│       ├── edit_category.html
│       ├── delete_category.html
│       ├── add_question.html
│       ├── view_all_results.html
│       └── user_detail.html
│
├── subjects/                  # Placeholder app (reserved for future use)
│
├── vercel.json                # Vercel deployment config
├── manage.py
└── .gitignore
```

---

## Getting Started

### Prerequisites

- Python 3.11 or higher
- pip
- Git
- A PostgreSQL database (local or Supabase)

### Installation

**1. Clone the repository**
```bash
git clone <repository_url>
cd acadvault
```

**2. Create and activate a virtual environment**
```bash
python -m venv venv

# Linux / macOS
source venv/bin/activate

# Windows (PowerShell)
.\venv\Scripts\Activate.ps1
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

### Database Setup

**4. Create a `.env` file** in the project root with your database credentials:

```env
SECRET_KEY=your-django-secret-key
DEBUG=True

DB_HOST=your-db-host
DB_NAME=your-db-name
DB_USER=your-db-user
DB_PASSWORD=your-db-password
DB_PORT=5432
```

You can verify your connection before running migrations:
```bash
python test_connection.py
```

**5. Run migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

**6. Create a superuser (Teacher/Admin account)**
```bash
python manage.py createsuperuser
```

### Running the Server

```bash
python manage.py runserver
```

The app will be available at **http://127.0.0.1:8000**.

---

## Environment Variables

| Variable | Description |
|---|---|
| `SECRET_KEY` | Django secret key |
| `DEBUG` | `True` for development, `False` for production |
| `DB_HOST` | PostgreSQL host (e.g., Supabase connection string) |
| `DB_NAME` | Database name |
| `DB_USER` | Database user |
| `DB_PASSWORD` | Database password |
| `DB_PORT` | Database port (default: `5432`) |

---

## User Roles

Acadvault uses Django's built-in `is_staff` and `is_superuser` flags for role-based access control — no separate role model is required.

| Role | How to Create | Access |
|---|---|---|
| **Student** | Register via `/register/` with "Student" selected | Dashboard, quizzes, own results |
| **Teacher/Admin** | Register with "Teacher/Admin" selected (sets `is_staff=True`, `is_superuser=True`) | Everything above + category management, all results, CSV export |

> **Note:** Teachers created via the registration form are granted full superuser access. For more granular permissions, use Django Admin at `/admin/`.

---

## URL Structure

| URL | View | Description |
|---|---|---|
| `/` | `landing_page` | Home page with Login / Register cards |
| `/login/` | `login_view` | User login |
| `/register/` | `register` | User registration |
| `/subjects/dashboard/` | `dashboard` | Personalized student dashboard |
| `/subjects/start-assessment/` | `select_category` | Category selection page |
| `/subjects/quiz/<id>/` | `start_quiz` | Secure quiz page |
| `/subjects/manage-categories/` | `manage_categories` | Admin: list all categories *(staff only)* |
| `/subjects/add-category/` | `add_category` | Admin: add category *(staff only)* |
| `/subjects/add-question/<id>/` | `add_question` | Admin: add question to category *(staff only)* |
| `/subjects/results/` | `view_all_results` | Admin: all results with filters *(staff only)* |
| `/subjects/results/export/` | `export_results_csv` | Admin: CSV download *(staff only)* |
| `/subjects/results/user/<id>/` | `view_user_detail` | Admin: per-student history *(staff only)* |
| `/admin/` | Django Admin | Full database administration |

---

## Deployment

The project is configured for deployment on **Vercel** using `@vercel/python`.

### Key files

- **`vercel.json`** — Configures the WSGI build and static file routing
- **`quiz_app/wsgi.py`** — Exposes both `application` and `app` for Vercel compatibility
- **WhiteNoise** — Serves compressed static files in production via `STATICFILES_STORAGE`

### Steps to deploy

1. Push the repository to GitHub
2. Import the project into [Vercel](https://vercel.com)
3. Add all environment variables from the [Environment Variables](#environment-variables) section in the Vercel dashboard
4. Set `DEBUG=False` in production
5. Deploy — Vercel will run the build automatically

> **Database:** The app is configured to connect to a **Supabase PostgreSQL** instance with SSL required (`sslmode=require`). `CONN_MAX_AGE=0` and `DISABLE_SERVER_SIDE_CURSORS=True` are set to ensure compatibility with Supabase's connection pooler.

---

## Contributing

Contributions are welcome! To get started:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add some feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

---

## License

This project is open source. Feel free to use and adapt it for your own educational projects.
