from django.urls import path
from . import views

app_name = 'arduino_comm'

urlpatterns = [
    path('receive/', views.receive_data, name='receive_data'),
    path('send/', views.send_command, name='send_command'),
    path('configure/', views.configure_sensor, name='configure_sensor'),
    path('control/', views.control_page, name='control_panel'),
    path('fetch/', views.fetch_sensor_data, name='fetch_sensor_data'),
    path('active_sensors/', views.active_sensors_page, name='active_sensors_page'),
    path('save_sensors/', views.save_sensors, name='save_sensors'),
]
