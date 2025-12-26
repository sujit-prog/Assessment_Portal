from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.db.models import Avg, Max, Count, Q
from django.http import HttpResponse
from .models import Category, Question, QuizAttempt
import random
import csv
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required, user_passes_test

# Check if user is staff/admin
def is_teacher(user):
    return user.is_superuser and user.is_staff

def is_staff_user(user):
    return user.is_staff or user.is_superuser

# ==================== CATEGORY MANAGEMENT ====================

@user_passes_test(is_staff_user)
def manage_categories(request):
    """View and manage all categories (Admin only)"""
    categories = Category.objects.all().annotate(
        question_count=Count('questions'),
        attempt_count=Count('quizattempt')
    ).order_by('name')
    
    context = {
        'categories': categories,
    }
    return render(request, 'home/manage_categories.html', context)

@user_passes_test(is_staff_user)
def add_category(request):
    """Add a new category (Admin only)"""
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        
        if not name:
            messages.error(request, 'Category name is required')
            return render(request, 'home/add_category.html')
        
        # Check if category already exists
        if Category.objects.filter(name__iexact=name).exists():
            messages.error(request, f'Category "{name}" already exists')
            return render(request, 'home/add_category.html')
        
        try:
            Category.objects.create(name=name)
            messages.success(request, f'Category "{name}" added successfully!')
            return redirect('manage_categories')
        except Exception as e:
            messages.error(request, f'Error adding category: {str(e)}')
    
    return render(request, 'home/add_category.html')

@user_passes_test(is_staff_user)
def edit_category(request, category_id):
    """Edit an existing category (Admin only)"""
    category = get_object_or_404(Category, id=category_id)
    
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        
        if not name:
            messages.error(request, 'Category name is required')
            return render(request, 'home/edit_category.html', {'category': category})
        
        # Check if another category with this name exists
        if Category.objects.filter(name__iexact=name).exclude(id=category_id).exists():
            messages.error(request, f'Category "{name}" already exists')
            return render(request, 'home/edit_category.html', {'category': category})
        
        try:
            category.name = name
            category.save()
            messages.success(request, f'Category updated to "{name}"')
            return redirect('manage_categories')
        except Exception as e:
            messages.error(request, f'Error updating category: {str(e)}')
    
    return render(request, 'home/edit_category.html', {'category': category})

@user_passes_test(is_staff_user)
def delete_category(request, category_id):
    """Delete a category (Admin only)"""
    category = get_object_or_404(Category, id=category_id)
    
    if request.method == 'POST':
        category_name = category.name
        try:
            category.delete()
            messages.success(request, f'Category "{category_name}" deleted successfully')
        except Exception as e:
            messages.error(request, f'Error deleting category: {str(e)}')
        return redirect('manage_categories')
    
    # Get related data for confirmation
    question_count = Question.objects.filter(category=category).count()
    attempt_count = QuizAttempt.objects.filter(category=category).count()
    
    context = {
        'category': category,
        'question_count': question_count,
        'attempt_count': attempt_count,
    }
    return render(request, 'home/delete_category.html', context)

@user_passes_test(is_staff_user)
def add_question(request, category_id):
    """Add a new question to a category (Admin only)"""
    category = get_object_or_404(Category, id=category_id)
    
    if request.method == 'POST':
        question_text = request.POST.get('question_text', '').strip()
        option_a = request.POST.get('option_a', '').strip()
        option_b = request.POST.get('option_b', '').strip()
        option_c = request.POST.get('option_c', '').strip()
        option_d = request.POST.get('option_d', '').strip()
        correct_option = request.POST.get('correct_option', '').strip()
        
        # Validation
        if not all([question_text, option_a, option_b, option_c, option_d, correct_option]):
            messages.error(request, 'All fields are required')
            return render(request, 'home/add_question.html', {'category': category})
        
        if correct_option not in ['A', 'B', 'C', 'D']:
            messages.error(request, 'Correct option must be A, B, C, or D')
            return render(request, 'home/add_question.html', {'category': category})
        
        try:
            Question.objects.create(
                category=category,
                question_text=question_text,
                option_a=option_a,
                option_b=option_b,
                option_c=option_c,
                option_d=option_d,
                correct_option=correct_option
            )
            messages.success(request, f'Question added successfully to {category.name}!')
            
            # Check if user wants to add another question
            if request.POST.get('add_another'):
                return redirect('add_question', category_id=category_id)
            else:
                return redirect('manage_categories')
                
        except Exception as e:
            messages.error(request, f'Error adding question: {str(e)}')
    
    return render(request, 'home/add_question.html', {'category': category})

# ==================== RESULTS MANAGEMENT (ADMIN/TEACHER) ====================

@user_passes_test(is_staff_user)
def view_all_results(request):
    """View all quiz results with filtering and search (Admin/Teacher only)"""
    
    # Get all quiz attempts with related data
    attempts = QuizAttempt.objects.select_related('user', 'category').order_by('-timestamp')
    
    # Get filter parameters
    category_filter = request.GET.get('category', '')
    user_filter = request.GET.get('user', '')
    flagged_filter = request.GET.get('flagged', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    search_query = request.GET.get('search', '')
    
    # Apply filters
    if category_filter:
        attempts = attempts.filter(category_id=category_filter)
    
    if user_filter:
        attempts = attempts.filter(user_id=user_filter)
    
    if flagged_filter == 'yes':
        attempts = attempts.filter(is_flagged=True)
    elif flagged_filter == 'no':
        attempts = attempts.filter(is_flagged=False)
    
    if date_from:
        attempts = attempts.filter(timestamp__gte=date_from)
    
    if date_to:
        # Add one day to include the entire end date
        date_to_obj = datetime.strptime(date_to, '%Y-%m-%d')
        date_to_end = date_to_obj + timedelta(days=1)
        attempts = attempts.filter(timestamp__lt=date_to_end)
    
    if search_query:
        attempts = attempts.filter(
            Q(user__username__icontains=search_query) |
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query) |
            Q(user__email__icontains=search_query)
        )
    
    # Calculate statistics
    total_attempts = attempts.count()
    flagged_attempts = attempts.filter(is_flagged=True).count()
    
    if total_attempts > 0:
        avg_score = attempts.aggregate(
            avg=Avg('score')
        )['avg']
        avg_percentage = round(avg_score / attempts.first().total * 100 if attempts.first() else 0, 1)
    else:
        avg_score = 0
        avg_percentage = 0
    
    # Prepare results data
    results_data = []
    for attempt in attempts:
        percentage = round((attempt.score / attempt.total * 100) if attempt.total > 0 else 0, 1)
        results_data.append({
            'id': attempt.id,
            'user': attempt.user,
            'username': attempt.user.username,
            'full_name': f"{attempt.user.first_name} {attempt.user.last_name}".strip() or attempt.user.username,
            'email': attempt.user.email,
            'category': attempt.category.name,
            'score': attempt.score,
            'total': attempt.total,
            'percentage': percentage,
            'timestamp': attempt.timestamp,
            'is_flagged': attempt.is_flagged,
            'tab_switches': attempt.tab_switches,
            'fullscreen_exits': attempt.fullscreen_exits,
        })
    
    # Get all categories and users for filter dropdowns
    categories = Category.objects.all().order_by('name')
    users = User.objects.filter(
        quizattempt__isnull=False
    ).distinct().order_by('username')
    
    context = {
        'results': results_data,
        'total_attempts': total_attempts,
        'flagged_attempts': flagged_attempts,
        'avg_percentage': avg_percentage,
        'categories': categories,
        'users': users,
        'filters': {
            'category': category_filter,
            'user': user_filter,
            'flagged': flagged_filter,
            'date_from': date_from,
            'date_to': date_to,
            'search': search_query,
        }
    }
    
    return render(request, 'home/view_all_results.html', context)


@user_passes_test(is_staff_user)
def export_results_csv(request):
    """Export filtered results to CSV (Admin/Teacher only)"""
    
    # Get all quiz attempts with related data
    attempts = QuizAttempt.objects.select_related('user', 'category').order_by('-timestamp')
    
    # Apply same filters as view_all_results
    category_filter = request.GET.get('category', '')
    user_filter = request.GET.get('user', '')
    flagged_filter = request.GET.get('flagged', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    search_query = request.GET.get('search', '')
    
    if category_filter:
        attempts = attempts.filter(category_id=category_filter)
    
    if user_filter:
        attempts = attempts.filter(user_id=user_filter)
    
    if flagged_filter == 'yes':
        attempts = attempts.filter(is_flagged=True)
    elif flagged_filter == 'no':
        attempts = attempts.filter(is_flagged=False)
    
    if date_from:
        attempts = attempts.filter(timestamp__gte=date_from)
    
    if date_to:
        date_to_obj = datetime.strptime(date_to, '%Y-%m-%d')
        date_to_end = date_to_obj + timedelta(days=1)
        attempts = attempts.filter(timestamp__lt=date_to_end)
    
    if search_query:
        attempts = attempts.filter(
            Q(user__username__icontains=search_query) |
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query) |
            Q(user__email__icontains=search_query)
        )
    
    # Create CSV response
    response = HttpResponse(content_type='text/csv')
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    response['Content-Disposition'] = f'attachment; filename="quiz_results_{timestamp}.csv"'
    
    writer = csv.writer(response)
    
    # Write header
    writer.writerow([
        'Attempt ID',
        'Username',
        'Full Name',
        'Email',
        'Category',
        'Score',
        'Total Questions',
        'Percentage',
        'Date & Time',
        'Flagged',
        'Tab Switches',
        'Fullscreen Exits',
        'Status'
    ])
    
    # Write data rows
    for attempt in attempts:
        percentage = round((attempt.score / attempt.total * 100) if attempt.total > 0 else 0, 1)
        full_name = f"{attempt.user.first_name} {attempt.user.last_name}".strip() or attempt.user.username
        
        # Determine status
        if attempt.is_flagged:
            status = 'FLAGGED'
        elif attempt.tab_switches > 0 or attempt.fullscreen_exits > 0:
            status = 'WARNING'
        else:
            status = 'CLEAN'
        
        writer.writerow([
            attempt.id,
            attempt.user.username,
            full_name,
            attempt.user.email,
            attempt.category.name,
            attempt.score,
            attempt.total,
            f"{percentage}%",
            attempt.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'Yes' if attempt.is_flagged else 'No',
            attempt.tab_switches,
            attempt.fullscreen_exits,
            status
        ])
    
    return response


@user_passes_test(is_staff_user)
def delete_result(request, attempt_id):
    """Delete a specific quiz attempt (Admin/Teacher only)"""
    if request.method == 'POST':
        attempt = get_object_or_404(QuizAttempt, id=attempt_id)
        user_name = attempt.user.username
        category_name = attempt.category.name
        attempt.delete()
        messages.success(request, f'Deleted quiz attempt for {user_name} in {category_name}')
    
    return redirect('view_all_results')


@user_passes_test(is_staff_user)
def view_user_detail(request, user_id):
    """View detailed results for a specific user (Admin/Teacher only)"""
    user_obj = get_object_or_404(User, id=user_id)
    attempts = QuizAttempt.objects.filter(user=user_obj).select_related('category').order_by('-timestamp')
    
    # Calculate user statistics
    total_attempts = attempts.count()
    
    if total_attempts > 0:
        total_percentage = sum((attempt.score / attempt.total * 100) if attempt.total > 0 else 0 
                               for attempt in attempts)
        average_score = round(total_percentage / total_attempts, 1)
        
        # Get best score
        best_attempt = max(attempts, key=lambda x: (x.score / x.total * 100) if x.total > 0 else 0)
        best_score = round((best_attempt.score / best_attempt.total * 100) if best_attempt.total > 0 else 0, 1)
        best_category = best_attempt.category.name
    else:
        average_score = 0
        best_score = 0
        best_category = None
    
    flagged_count = attempts.filter(is_flagged=True).count()
    
    # Prepare attempts data
    attempts_data = []
    for attempt in attempts:
        percentage = round((attempt.score / attempt.total * 100) if attempt.total > 0 else 0, 1)
        attempts_data.append({
            'id': attempt.id,
            'category': attempt.category.name,
            'score': attempt.score,
            'total': attempt.total,
            'percentage': percentage,
            'timestamp': attempt.timestamp,
            'is_flagged': attempt.is_flagged,
            'tab_switches': attempt.tab_switches,
            'fullscreen_exits': attempt.fullscreen_exits,
        })
    
    context = {
        'student': user_obj,
        'full_name': f"{user_obj.first_name} {user_obj.last_name}".strip() or user_obj.username,
        'attempts': attempts_data,
        'total_attempts': total_attempts,
        'average_score': average_score,
        'best_score': best_score,
        'best_category': best_category,
        'flagged_count': flagged_count,
    }
    
    return render(request, 'home/user_detail.html', context)

# ==================== DASHBOARD & QUIZ VIEWS ====================

@login_required(login_url='login')
def dashboard(request):
    """Display personalized user dashboard with quiz statistics and security notifications"""
    user = request.user
    
    # Get user's quiz attempts ordered by most recent
    attempts = QuizAttempt.objects.filter(user=user).select_related('category').order_by('-timestamp')
    
    # Get flagged attempts for notifications (last 10 flagged attempts)
    flagged_attempts = attempts.filter(is_flagged=True)[:10]
    
    # Prepare security notifications
    security_notifications = []
    for attempt in flagged_attempts:
        notification = {
            'category_name': attempt.category.name,
            'timestamp': attempt.timestamp,
            'tab_switches': attempt.tab_switches,
            'fullscreen_exits': attempt.fullscreen_exits,
            'score': attempt.score,
            'total': attempt.total,
            'percentage': round((attempt.score / attempt.total * 100) if attempt.total > 0 else 0, 1)
        }
        security_notifications.append(notification)
    
    # Calculate statistics
    total_attempts = attempts.count()
    
    # Calculate average percentage
    if total_attempts > 0:
        total_percentage = sum((attempt.score / attempt.total * 100) if attempt.total > 0 else 0 
                               for attempt in attempts)
        average_score = round(total_percentage / total_attempts, 1)
    else:
        average_score = 0
    
    # Get recent attempts for display (last 4)
    recent_attempts = []
    for attempt in attempts[:4]:
        percentage = round((attempt.score / attempt.total * 100) if attempt.total > 0 else 0, 1)
        recent_attempts.append({
            'title': f"{attempt.category.name} Quiz",
            'score': percentage,
            'date': attempt.timestamp.strftime('%b %d, %Y'),
            'raw_score': f"{attempt.score}/{attempt.total}",
            'is_flagged': attempt.is_flagged,
            'tab_switches': attempt.tab_switches,
            'fullscreen_exits': attempt.fullscreen_exits
        })
    
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
                'score': avg_score,
                'attempts': cat_attempts.count()
            })
    
    # Get highest score
    highest_score = 0
    best_category = None
    if total_attempts > 0:
        for attempt in attempts:
            percentage = (attempt.score / attempt.total * 100) if attempt.total > 0 else 0
            if percentage > highest_score:
                highest_score = round(percentage, 1)
                best_category = attempt.category.name
    
    # Get user's display name (first name if available, otherwise username)
    display_name = user.first_name if user.first_name else user.username
    
    # Calculate improvement trend (last 5 attempts vs previous 5)
    improvement_trend = "stable"
    if total_attempts >= 10:
        recent_5 = attempts[:5]
        previous_5 = attempts[5:10]
        
        recent_avg = sum((a.score / a.total * 100) for a in recent_5) / 5
        previous_avg = sum((a.score / a.total * 100) for a in previous_5) / 5
        
        if recent_avg > previous_avg + 5:
            improvement_trend = "improving"
        elif recent_avg < previous_avg - 5:
            improvement_trend = "declining"

    context = {
        'user': user,
        'display_name': display_name,
        'recent_attempts': recent_attempts,
        'total_attempts': total_attempts,
        'average_score': average_score,
        'highest_score': highest_score,
        'best_category': best_category,
        'subject_performance': subject_performance,
        'improvement_trend': improvement_trend,
        'security_notifications': security_notifications,
        'has_flagged_attempts': flagged_attempts.exists(),
    }
    return render(request, 'home/dashboard.html', context)

@login_required(login_url='login')
def select_category(request):
    """Display available quiz categories"""
    categories = Category.objects.all().annotate(
        question_count=Count('questions')
    )
    return render(request, 'home/select_category.html', {'categories': categories})

@login_required(login_url='login')
def start_quiz(request, category_id):
    """Start a quiz for selected category with anti-cheating measures"""
    category = get_object_or_404(Category, id=category_id)
    questions = list(Question.objects.filter(category=category))
    
    # Check if category has questions
    if not questions:
        messages.error(request, f'No questions available for {category.name} yet.')
        return redirect('select_category')
    
    # Shuffle questions for randomness
    random.shuffle(questions)

    if request.method == 'POST':
        # Get security tracking data
        tab_switches = int(request.POST.get('tab_switches', '0'))
        fullscreen_exits = int(request.POST.get('fullscreen_exits', '0'))
        
        # REMOVED: Don't use messages.warning here - it persists to other pages
        # Instead, we'll pass the flag status directly to the template
        is_flagged = (tab_switches > 3 or fullscreen_exits > 2)
        
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

        # Save quiz attempt with security tracking
        attempt = QuizAttempt.objects.create(
            user=request.user,
            category=category,
            score=score,
            total=total,
            tab_switches=tab_switches,
            fullscreen_exits=fullscreen_exits,
            is_flagged=is_flagged
        )

        percentage = round((score / total) * 100, 1) if total > 0 else 0

        # Pass security info to the evaluation template instead of using messages
        return render(request, 'home/evaluation.html', {
            'category': category,
            'score': score,
            'total': total,
            'percentage': percentage,
            'results': results,
            'is_flagged': is_flagged,
            'tab_switches': tab_switches,
            'fullscreen_exits': fullscreen_exits,
        })

    # Use secure quiz template
    return render(request, 'home/start_quiz_secure.html', {
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