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


# Registration View - FIXED to match HTML form field names
def register(request):
    if request.method == 'POST':
        # Get form data matching the HTML form field names
        name = request.POST.get('name')  # Full name from form
        email = request.POST.get('email')  # Email/Student ID
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-password')
        
        print(f"Registration attempt - Name: {name}, Email: {email}")  # Debug
        
        # Validation
        if not name or not email or not password or not confirm_password:
            messages.error(request, "All fields are required")
            return render(request, 'accounts/register.html')

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return render(request, 'accounts/register.html')
        
        if len(password) < 6:
            messages.error(request, "Password must be at least 6 characters long")
            return render(request, 'accounts/register.html')

        # Use email as username if it's an email, otherwise use it as-is (for Student ID)
        username = email.split('@')[0] if '@' in email else email
        
        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists. Please use a different email/ID")
            return render(request, 'accounts/register.html')
        
        # Check if email already exists (if it's a valid email)
        if '@' in email and User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return render(request, 'accounts/register.html')

        try:
            # Create user with properly hashed password
            user = User.objects.create_user(
                username=username,
                email=email if '@' in email else '',
                password=password,
                first_name=name  # Store full name in first_name field
            )
            user.save()
            
            print(f"New user registered: {username}")  # Debug
            messages.success(request, "Registration successful! Please login with your credentials.")
            return redirect('login')
            
        except Exception as e:
            print(f"Registration error: {e}")  # Debug
            messages.error(request, f"An error occurred during registration: {str(e)}")
            return render(request, 'accounts/register.html')

    return render(request, 'accounts/register.html')