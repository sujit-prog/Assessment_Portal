from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    # Add any context you want here
    return render(request, 'home/dashboard.html')
