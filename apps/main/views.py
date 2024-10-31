from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import LoginForm, RegisterForm
from django.contrib import messages

def login_view(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('main:dashboard')  # Redirect to dashboard after login
        else:
            error = "Eroare la autentificare! Adaugați utilizatorul și parola primită!"
    
    return render(request, 'main/login.html', {'error': error})


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            # Create the new user
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            
            # Automatically log in the new user after registration
            login(request, user)
            return redirect('main:dashboard')  # Redirect to dashboard after registration
        else:
            messages.error(request, 'A apărut o eroare la înregistrare!')
    else:
        form = RegisterForm()

    return render(request, 'main/register.html', {'form': form})


@login_required
def dashboard_view(request):
    return render(request, 'main/dashboard.html')

@login_required
def profile_view(request):
    return render(request, 'main/profile.html')

def logout_view(request):
    logout(request)
    return redirect('main:login')

def settings_view(request):
    return render(request, 'main/settings.html')


@login_required
def analytics_view(request):
    # Context data for the analytics page, if needed
    context = {
        'title': 'Analytics',
        # You can add additional data for charts, metrics, etc.
    }
    return render(request, 'main/analytics.html', context)