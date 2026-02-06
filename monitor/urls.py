from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('api/interfaces/', views.get_interfaces, name='get_interfaces'),
    path('api/fix-interface/', views.fix_interface, name='fix_interface'),
    path('api/logs/', views.get_logs, name='get_logs'),
    path('api/stats/', views.get_stats, name='get_stats'),
    path('api/clear-logs/', views.clear_logs, name='clear_logs'),
]
