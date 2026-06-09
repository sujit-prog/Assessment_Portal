"""
Seed script to populate the database with default test users and quiz data.
Usage: python seed_data.py
"""

import os
import sys
import django
from pathlib import Path

# Setup Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quiz_app.settings')
django.setup()

from django.contrib.auth.models import User
from home.models import Category, Question

def seed():
    print("Seeding database...")
    
    # 1. Create Teacher / Admin account
    teacher_username = "teacher"
    teacher_email = "teacher@example.com"
    teacher_password = "password123"
    
    if not User.objects.filter(username=teacher_username).exists():
        User.objects.create_superuser(
            username=teacher_username,
            email=teacher_email,
            password=teacher_password,
            first_name="Admin",
            last_name="Teacher"
        )
        print(f"✅ Created superuser (Teacher): {teacher_username} / {teacher_password}")
    else:
        print(f"ℹ️ Superuser (Teacher) '{teacher_username}' already exists.")
        
    # 2. Create Student account
    student_username = "student"
    student_email = "student@example.com"
    student_password = "password123"
    
    if not User.objects.filter(username=student_username).exists():
        User.objects.create_user(
            username=student_username,
            email=student_email,
            password=student_password,
            first_name="John",
            last_name="Student"
        )
        print(f"✅ Created user (Student): {student_username} / {student_password}")
    else:
        print(f"ℹ️ User (Student) '{student_username}' already exists.")

    # 3. Create Categories and Questions
    # Category: Python Basics
    python_cat, created = Category.objects.get_or_create(name="Python Basics")
    if created:
        print("✅ Created category: Python Basics")
    
    python_questions = [
        {
            "text": "What is the correct file extension for Python files?",
            "a": ".pyt",
            "b": ".py",
            "c": ".python",
            "d": ".pyw",
            "correct": "B"
        },
        {
            "text": "Which of the following is used to define a block of code in Python language?",
            "a": "Key",
            "b": "Brackets",
            "c": "Indentation",
            "d": "All of these",
            "correct": "C"
        },
        {
            "text": "Which keyword is used to create a function in Python?",
            "a": "fun",
            "b": "function",
            "c": "define",
            "d": "def",
            "correct": "D"
        },
        {
            "text": "What does print(type([]) is list) output?",
            "a": "True",
            "b": "False",
            "c": "Error",
            "d": "None",
            "correct": "A"
        },
        {
            "text": "How do you insert comments in Python code?",
            "a": "// this is a comment",
            "b": "/* this is a comment */",
            "c": "# this is a comment",
            "d": "<!-- this is a comment -->",
            "correct": "C"
        }
    ]
    
    for q in python_questions:
        Question.objects.get_or_create(
            category=python_cat,
            question_text=q["text"],
            defaults={
                "option_a": q["a"],
                "option_b": q["b"],
                "option_c": q["c"],
                "option_d": q["d"],
                "correct_option": q["correct"]
            }
        )
    print("✅ Seeded questions for Python Basics")

    # Category: Web Development
    web_cat, created = Category.objects.get_or_create(name="Web Development")
    if created:
        print("✅ Created category: Web Development")
        
    web_questions = [
        {
            "text": "What does HTML stand for?",
            "a": "Hyper Text Markup Language",
            "b": "Home Tool Markup Language",
            "c": "Hyperlinks and Text Markup Language",
            "d": "Hyper Tool Multi Language",
            "correct": "A"
        },
        {
            "text": "Who is making the Web standards?",
            "a": "Google",
            "b": "Mozilla",
            "c": "Microsoft",
            "d": "The World Wide Web Consortium (W3C)",
            "correct": "D"
        },
        {
            "text": "Which HTML element is used for the largest heading?",
            "a": "<heading>",
            "b": "<h6>",
            "c": "<h1>",
            "d": "<head>",
            "correct": "C"
        },
        {
            "text": "What is the correct HTML element for inserting a line break?",
            "a": "<lb>",
            "b": "<break>",
            "c": "<br>",
            "d": "<hr>",
            "correct": "C"
        },
        {
            "text": "Which CSS property is used to change the text color of an element?",
            "a": "fgcolor",
            "b": "text-color",
            "c": "color",
            "d": "font-color",
            "correct": "C"
        }
    ]
    
    for q in web_questions:
        Question.objects.get_or_create(
            category=web_cat,
            question_text=q["text"],
            defaults={
                "option_a": q["a"],
                "option_b": q["b"],
                "option_c": q["c"],
                "option_d": q["d"],
                "correct_option": q["correct"]
            }
        )
    print("✅ Seeded questions for Web Development")
    print("🎉 Database seeding complete!")

if __name__ == "__main__":
    seed()
