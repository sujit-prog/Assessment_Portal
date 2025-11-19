from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.db.models import Avg, Max, Count
from .models import Category, Question, QuizAttempt
import random

# ==================== DASHBOARD & QUIZ VIEWS ====================

@login_required(login_url='login')
def dashboard(request):
    """Display user dashboard with quiz statistics"""
    # Get user's quiz attempts
    attempts = QuizAttempt.objects.filter(user=request.user).order_by('-timestamp')
    
    # Calculate statistics
    total_attempts = attempts.count()
    
    # Calculate average percentage
    if total_attempts > 0:
        total_percentage = sum((attempt.score / attempt.total * 100) if attempt.total > 0 else 0 
                               for attempt in attempts)
        average_score = round(total_percentage / total_attempts, 1)
    else:
        average_score = 0
    
    # Get recent attempts for display
    recent_attempts = attempts[:4]  # Last 4 attempts
    
    # Calculate subject-wise performance
    subject_performance = []
    categories = Category.objects.all()
    for category in categories:
        cat_attempts = attempts.filter(category=category)
        if cat_attempts.exists():
            cat_total = sum((a.score / a.total * 100) if a.total > 0 else 0 for a in cat_attempts)
            avg_score = round(cat_total / cat_attempts.count(), 1)
            subject_performance.append({
                'subject': category.name,
                'score': avg_score
            })

    context = {
        'attempts': recent_attempts,
        'total_attempts': total_attempts,
        'average_score': average_score,
        'subject_performance': subject_performance,
        'user': request.user,
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
    questions = list(Question.objects.filter(category=category))
    
    # Shuffle questions for randomness
    random.shuffle(questions)

    if request.method == 'POST':
        score = 0
        total = len(questions)
        results = []

        # Calculate score and prepare results
        for q in questions:
            selected_option = request.POST.get(f'q{q.id}')
            is_correct = selected_option == q.correct_option
            
            if is_correct:
                score += 1
            
            # Get the text of the selected and correct options
            option_map = {
                'A': q.option_a,
                'B': q.option_b,
                'C': q.option_c,
                'D': q.option_d
            }
            
            results.append({
                'question': q.question_text,
                'selected': option_map.get(selected_option, 'Not answered'),
                'correct': option_map.get(q.correct_option, 'N/A'),
                'is_correct': is_correct
            })

        # Save quiz attempt with user
        QuizAttempt.objects.create(
            user=request.user,
            category=category,
            score=score,
            total=total
        )

        percentage = round((score / total) * 100, 1) if total > 0 else 0

        return render(request, 'home/evaluation.html', {
            'category': category,
            'score': score,
            'total': total,
            'percentage': percentage,
            'results': results,
        })

    return render(request, 'home/start_quiz.html', {
        'category': category,
        'questions': questions,
    })

@login_required(login_url='login')
def quiz_result(request, attempt_id):
    """Display specific quiz result"""
    attempt = get_object_or_404(QuizAttempt, id=attempt_id, user=request.user)
    percentage = round((attempt.score / attempt.total) * 100, 1) if attempt.total > 0 else 0
    
    return render(request, 'home/quiz_result.html', {
        'attempt': attempt,
        'percentage': percentage
    })

@login_required(login_url='login')
def submit_quiz(request):
    """Submit quiz answers and calculate score"""
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

        percentage = round((score / total) * 100, 1) if total > 0 else 0
        
        return render(request, 'home/result.html', {
            'score': score,
            'total': total,
            'percentage': percentage,
        })

    return redirect('dashboard')

@login_required(login_url='login')
def result_page(request):
    """Show latest quiz result"""
    latest_attempt = QuizAttempt.objects.filter(user=request.user).order_by('-timestamp').first()
    if latest_attempt:
        percentage = round((latest_attempt.score / latest_attempt.total) * 100, 1) if latest_attempt.total > 0 else 0
        return render(request, 'home/quiz_result.html', {
            'attempt': latest_attempt,
            'percentage': percentage
        })
    return redirect('dashboard')