📚 Assessment Portal

A comprehensive, full-stack application built with Django for managing and taking quizzes or assessments. Designed to provide a streamlined experience for both administrators (to manage questions and categories) and users (to take quizzes and review results).

The application focuses on robust URL handling, secure staff/admin access control, and a modern, responsive user interface built with Tailwind CSS.

✨ Features

User Authentication: Secure login and registration flows.

Role-Based Access Control:

Staff/Admin Users: Dedicated views for creating, editing, and deleting quiz categories and questions.

Regular Users: Access to the dashboard, quiz selection, and assessment taking.

Quiz Management:

Create and manage multiple quiz categories (e.g., Data Structures, Algorithms, Python).

Add multiple-choice questions (MCQs) with four options and a designated correct answer for each category.

Assessment Taking:

Start quizzes based on category selection.

Submit answers and view immediate feedback or a final result summary.

Result Tracking: View historical results and detailed breakdowns of previous attempts.

Modern UI: Fully responsive design using Tailwind CSS with dark mode support for better accessibility.

🚀 Technology Stack

This project is built using the following core technologies:

Category

Technology

Description

Backend

Python 3.12

Core programming language.

Web Framework

Django 5.x

High-level Python Web framework for rapid development.

Database

postgresql

Used for development. Can easily be swapped for PostgreSQL/MySQL for production.

Frontend

HTML5, Django Templates

Structure and server-side rendering.

Styling

Tailwind CSS

Utility-first CSS framework for responsive and modern design.

Deployment

Vercel (Frontend)

The current deployment is linked to Vercel (likely as a static build or a front-end container).

⚙️ Setup and Installation (Local Development)

Follow these steps to get a copy of the project up and running on your local machine for development and testing purposes.

Prerequisites

Python 3.11+

pip (Python package installer)

Git

Step 1: Clone the Repository

git clone <repository_url_here>
cd quiz_app # Adjust folder name if necessary


Step 2: Create and Activate a Virtual Environment

It is highly recommended to use a virtual environment to manage dependencies.

# Create the environment (Linux/macOS/Windows PowerShell)
python -m venv venv

# Activate the environment (Linux/macOS)
source venv/bin/activate

# Activate the environment (Windows Command Prompt)
.\venv\Scripts\activate

# Activate the environment (Windows PowerShell)
.\venv\Scripts\Activate.ps1


Step 3: Install Dependencies

Install all necessary Python packages (assuming you have a requirements.txt file).

pip install -r requirements.txt


Step 4: Database Setup

Apply database migrations to create the necessary tables.

python manage.py makemigrations
python manage.py migrate


Step 5: Create a Superuser (Admin)

Create an administrative account to access the Django Admin site and the staff-only management views (like adding categories and questions).

python manage.py createsuperuser


Step 6: Run the Development Server

Start the local Django development server.

python manage.py runserver


The application will now be running at http://127.0.0.1:8000/.

🌐 Deployment

The live version of this application is hosted at: https://assessmentportal-seven.vercel.app/

This suggests a deployment approach that handles Django's complexities (static files, environment variables, database configuration) possibly using a combination of Vercel (for the frontend/proxy) and a dedicated server (like Heroku, DigitalOcean, or a PaaS solution) for the Django backend.

🤝 Contributing

Contributions are welcome! Please feel free to:

Fork the repository.

Create a new feature branch (git checkout -b feature/AmazingFeature).

Commit your changes (git commit -m 'Add some AmazingFeature').

Push to the branch (git push origin feature/AmazingFeature).

Your Name/Team Name - [Your Email/Contact Info]

Project Link: [repository_url_here]
