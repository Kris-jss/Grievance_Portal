from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import User

def home_view(request):
    """Home page with information"""
    return render(request, 'home.html')

def register_view(request):
    """Student registration"""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        # Validation
        if password1 != password2:
            messages.error(request, "Passwords don't match!")
            return redirect('register')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect('register')
        
        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1,
            role='student',
            phone=phone
        )
        
        messages.success(request, "Registration successful! Please login.")
        return redirect('login')
    
    return render(request, 'accounts/register.html')


def login_view(request):
    """Login for both students and admins"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password!")
            return redirect('login')
    
    return render(request, 'accounts/login.html')


def logout_view(request):
    """Logout user"""
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('login')


@login_required
def dashboard_view(request):
    """
    Redirect to appropriate dashboard based on user role
    """
    if request.user.role == 'admin':
        return redirect('admin_dashboard')
    else:
        return redirect('student_dashboard')