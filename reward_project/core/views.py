from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from .models import App, Task
from .forms import AdminAppForm, TaskForm, UserSignUpForm

# Hardcoded admin credentials
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'pass'

# Admin Login
def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            request.session['is_admin'] = True
            return redirect('admin_dashboard')
        else:
            return HttpResponse('Invalid credentials', status=401)
    return render(request, 'admin_login.html')

# Admin Dashboard
def admin_dashboard(request):
    if not request.session.get('is_admin'):
        return redirect('user_dashboard')
    apps = App.objects.all()
    return render(request, 'admin_dashboard.html', {'apps': apps})

# Admin Add App
def admin_add_app(request):
    if not request.session.get('is_admin'):
        return redirect('user_dashboard')
    form = AdminAppForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('admin_dashboard')
    return render(request, 'admin_add_app.html', {'form': form})

# Admin Update App
def admin_update_app(request, app_id):
    if not request.session.get('is_admin'):
        return redirect('user_dashboard')
    app = get_object_or_404(App, id=app_id)
    form = AdminAppForm(request.POST or None, instance=app)
    if form.is_valid():
        form.save()
        return redirect('admin_dashboard')
    return render(request, 'admin_update_app.html', {'form': form})

# Admin Delete App
def admin_delete_app(request, app_id):
    if not request.session.get('is_admin'):
        return redirect('user_dashboard')
    app = get_object_or_404(App, id=app_id)
    app.delete()
    return redirect('admin_dashboard')

# User Sign Up
def signup(request):
    if request.method == 'POST':
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('user_dashboard')
    else:
        form = UserSignUpForm()
    return render(request, 'signup.html', {'form': form})

# User Login
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('user_dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# User Logout
@login_required
def logout(request):
    auth_logout(request)
    return redirect('user_login')

# User Dashboard
@login_required
def user_dashboard(request):
    apps = App.objects.all()
    return render(request, 'user_dashboard.html', {'apps': apps})

# Submit Task (Screenshot)
@login_required
def submit_task(request, app_id):
    app = App.objects.get(id=app_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.app = app
            task.points_earned = app.points
            task.completed = True
            task.save()
            return redirect('user_profile')
    else:
        form = TaskForm()
    return render(request, 'submit_task.html', {'form': form, 'app': app})

# User Profile
@login_required
def user_profile(request):
    tasks = Task.objects.filter(user=request.user)
    total_points = sum(task.points_earned for task in tasks if task.completed)
    return render(request, 'user_profile.html', {'tasks': tasks, 'total_points': total_points})

# Admin Logout
def admin_logout(request):
    request.session.flush()
    return redirect('admin_login')
