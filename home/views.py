from django.shortcuts import render
from .models import Category  # if needed
from django.contrib.auth import login, authenticate
from django.shortcuts import redirect

# Landing page / Homepage
def homepage(request):
    return render(request, 'home/homepage.html')  # template path must match

# Subject selection page
def subject_selection(request):
    categories = Category.objects.all()
    return render(request, 'home/subject_selection.html', {'categories': categories})
def subject_selection(request):
    # Render the page where user selects a category
    return render(request, 'home/subject_selection.html')

def quiz_view(request, category_id):
    return render(request, 'home/quiz.html', {'category_id': category_id})