from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Category, Question, QuizAttempt
import random
from django.shortcuts import get_object_or_404
from django.db.models import Avg, Max


def dashboard(request):
    attempts = QuizAttempt.objects.all().order_by('-timestamp')


    total_attempts = attempts.count()
    average_score = round(attempts.aggregate(Avg('score'))['score__avg'] or 0, 2)
    best_score = round(attempts.aggregate(Max('score'))['score__max'] or 0, 2)

    # Prepare data for the chart
    dates = [a.date.strftime("%b %d") for a in attempts]
    scores = [a.score for a in attempts]

    context = {
        'attempts': attempts,
        'total_attempts': total_attempts,
        'average_score': average_score,
        'best_score': best_score,
        'dates': dates,
        'scores': scores,
    }
    return render(request, 'home/dashboard.html', context)

def select_category(request):
    categories = Category.objects.all()
    return render(request, 'home/select_category.html', {'categories': categories})

@login_required
def start_quiz(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    questions = Question.objects.filter(category=category)

    if request.method == "POST":
        score = 0
        total = questions.count()

        for question in questions:
            selected_option = request.POST.get(str(question.id))
            if selected_option == question.correct_option:
                score += 1

        # Store the attempt
        attempt = QuizAttempt.objects.create(category=category, score=score, total=total)

        # Redirect to result page
        return redirect('quiz_result', attempt_id=attempt.id)

    return render(request, 'start_quiz.html', {'category': category, 'questions': questions})



def quiz_result(request, attempt_id):
    attempt = get_object_or_404(QuizAttempt, id=attempt_id)
    return render(request, 'quiz_result.html', {'attempt': attempt})

def submit_quiz(request):
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

def start_quiz(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    questions = Question.objects.filter(category=category)

    if request.method == 'POST':
        score = 0
        total = questions.count()

        for q in questions:
            selected_option = request.POST.get(f'q{q.id}')
            if selected_option == q.correct_option:
                score += 1

        percentage = (score / total) * 100 if total > 0 else 0

        return render(request, 'home/evaluation.html', {
            'category': category,
            'score': score,
            'total': total,
            'percentage': percentage,
        })

    return render(request, 'home/start_quiz.html', {
        'category': category,
        'questions': questions,
    })
def result_page(request):
    # optional: show the latest attempt
    latest_attempt = QuizAttempt.objects.last()
    return render(request, 'quiz_result.html', {'attempt': latest_attempt})

