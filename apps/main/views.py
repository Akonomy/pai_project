from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import LoginForm, RegisterForm
from django.contrib import messages

from apps.arduino_comm.models import Sensor
from django.http import JsonResponse



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
    sensors = Sensor.objects.all()  # Fetch all sensors
    asensors = [sensor for sensor in sensors if sensor.active] 
# Group sensors by type and mode
    analog_outputs = [sensor for sensor in asensors if sensor.type == "output" and sensor.mode == "analog"]
    digital_outputs = [sensor for sensor in asensors if sensor.type == "output" and sensor.mode == "digital"]
    analog_inputs = [sensor for sensor in asensors if sensor.type == "input" and sensor.mode == "analog"]
    digital_inputs = [sensor for sensor in asensors if sensor.type == "input" and sensor.mode == "digital"]

    return render(request, 'main/dashboard.html', {
        "analog_outputs": analog_outputs,
        "digital_outputs": digital_outputs,
        "analog_inputs": analog_inputs,
        "digital_inputs": digital_inputs,
    })
  


def get_sensor_data(request):
    try:
        sensors = Sensor.objects.all()
        data = {sensor.id: {
                    "status": sensor.status,
                    "value": sensor.value,
                } for sensor in sensors}
        return JsonResponse(data, safe=False)  # Explicitly return JSON
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)






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