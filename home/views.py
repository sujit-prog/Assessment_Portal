from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.db.models import Avg, Max
from .models import Category, Question, QuizAttempt
import random

# ==================== AUTHENTICATION VIEWS ====================

def login_view(request):
    """Handle user login"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Debug logging
        print(f"Login attempt - Username: {username}")
        
        # Check if user exists
        try:
            user_exists = User.objects.get(username=username)
            print(f"User found: {user_exists.username}, Active: {user_exists.is_active}")
        except User.DoesNotExist:
            print(f"User '{username}' does not exist in database")
            messages.error(request, 'Invalid username or password.')
            return render(request, 'login.html')
        
        # Authenticate user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            messages.success(request, 'Login successful!')
            print(f"User {username} logged in successfully")
            return redirect('dashboard')
        else:
            print(f"Authentication failed for user: {username}")
            messages.error(request, 'Invalid username or password.')
            return render(request, 'login.html')
    
    return render(request, 'login.html')

def register_view(request):
    """Handle user registration"""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        # Validation
        if not username or not email or not password:
            messages.error(request, 'All fields are required.')
            return render(request, 'register.html')
        
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'register.html')
        
        if len(password) < 6:
            messages.error(request, 'Password must be at least 6 characters long.')
            return render(request, 'register.html')
        
        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'register.html')
        
        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return render(request, 'register.html')
        
        try:
            # CRITICAL: Use create_user to properly hash the password
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            user.save()
            
            messages.success(request, 'Registration successful! Please login.')
            print(f"New user registered: {username}")
            return redirect('login')
            
        except IntegrityError as e:
            print(f"Registration error: {e}")
            messages.error(request, 'An error occurred during registration. Please try again.')
            return render(request, 'register.html')
    
    return render(request, 'register.html')

def logout_view(request):
    """Handle user logout"""
    auth_logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')

# ==================== DASHBOARD & QUIZ VIEWS ====================

@login_required(login_url='login')
def dashboard(request):
    """Display user dashboard with quiz statistics"""
    attempts = QuizAttempt.objects.filter(user=request.user).order_by('-timestamp')

    total_attempts = attempts.count()
    average_score = round(attempts.aggregate(Avg('score'))['score__avg'] or 0, 2)
    best_score = round(attempts.aggregate(Max('score'))['score__max'] or 0, 2)

    # Prepare data for the chart
    dates = [a.timestamp.strftime("%b %d") for a in attempts[:10]]  # Last 10 attempts
    scores = [a.score for a in attempts[:10]]

    context = {
        'attempts': attempts,
        'total_attempts': total_attempts,
        'average_score': average_score,
        'best_score': best_score,
        'dates': dates,
        'scores': scores,
    }
    return render(request, 'home/dashboard.html', context)

@login_required(login_url='login')
def select_category(request):
    """Display available quiz categories"""
    categories = Category.objects.all()
    return render(request, 'home/select_category.html', {'categories': categories})

@login_required(login_url='login')
def start_quiz(request, category_id):
    """Start a quiz for selected category"""
    category = get_object_or_404(Category, id=category_id)
    questions = Question.objects.filter(category=category)

    if request.method == 'POST':
        score = 0
        total = questions.count()

        # Calculate score
        for q in questions:
            selected_option = request.POST.get(f'q{q.id}')
            if selected_option == q.correct_option:
                score += 1

        # Save quiz attempt
        QuizAttempt.objects.create(
            user=request.user,
            category=category,
            score=score,
            total=total
        )

        percentage = (score / total) * 100 if total > 0 else 0

        return render(request, 'home/evaluation.html', {
            'category': category,
            'score': score,
            'total': total,
            'percentage': round(percentage, 2),
        })

    return render(request, 'home/start_quiz.html', {
        'category': category,
        'questions': questions,
    })

@login_required(login_url='login')
def quiz_result(request, attempt_id):
    """Display specific quiz result"""
    attempt = get_object_or_404(QuizAttempt, id=attempt_id, user=request.user)
    return render(request, 'home/quiz_result.html', {'attempt': attempt})

@login_required(login_url='login')
def submit_quiz(request):
    """Submit quiz answers and calculate score"""
    print("✅ submit_quiz view called!")
    if request.method == 'POST':
        score = 0
        total = 0
        
        for key, value in request.POST.items():
            if key.startswith('question_'):
                question_id = key.split('_')[1]
                selected_option = value
                try:
                    question = Question.objects.get(id=question_id)
                    total += 1
                    if question.correct_option == selected_option:
                        score += 1
                except Question.DoesNotExist:
                    pass

        percentage = (score / total) * 100 if total > 0 else 0
        
        return render(request, 'home/result.html', {
            'score': score,
            'total': total,
            'percentage': round(percentage, 2),
        })

    return redirect('dashboard')

@login_required(login_url='login')
def result_page(request):
    """Show latest quiz result"""
    latest_attempt = QuizAttempt.objects.filter(user=request.user).last()
    return render(request, 'home/quiz_result.html', {'attempt': latest_attempt})