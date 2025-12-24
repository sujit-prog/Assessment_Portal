from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages


# Landing Page
def landing_page(request):
    return render(request, 'accounts/home.html')


# Login View
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        print(f"Login attempt - Username: {username}")  # Debug
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            print(f"User {username} logged in successfully")  # Debug
            return redirect('dashboard')
        else:
            print(f"Authentication failed for user: {username}")  # Debug
            messages.error(request, 'Invalid username or password')

    return render(request, 'accounts/login.html')


# Registration View - UPDATED with proper user_type handling
def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-password')
        user_type = request.POST.get('user_type', 'student')  # Get user type from form

        # Validation
        if not name or not username or not email or not password:
            messages.error(request, "All fields are required")
            return render(request, 'accounts/register.html')

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return render(request, 'accounts/register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
            return render(request, 'accounts/register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already taken")
            return render(request, 'accounts/register.html')

        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=name
        )

        # Set permissions based on user_type
        if user_type == "teacher":
            user.is_staff = True
            user.is_superuser = True
            user.save()
            messages.success(request, "Teacher account created successfully! You now have admin privileges. Please login.")
        else:
            # Student account (default)
            user.is_staff = False
            user.is_superuser = False
            user.save()
            messages.success(request, "Student account created successfully! Please login.")
        
        return redirect('login')

    return render(request, 'accounts/register.html')