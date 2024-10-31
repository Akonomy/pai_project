from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('profile/', views.profile_view, name='profile'),
    path('logout/', views.logout_view, name='logout'),
     path('settings/', views.settings_view, name='settings'),  
      path('analytics/', views.analytics_view, name='analytics'),  # Analytics URL
]

