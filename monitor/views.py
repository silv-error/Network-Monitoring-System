import os
import json
import random
from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from dotenv import load_dotenv
from .models import NetworkInterface, NetworkLog, NetworkStats
from .cisco_handler import CiscoDeviceHandler, SimulationHandler

load_dotenv()


def custom_login(request):
    """Custom login view with static credentials"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Static credentials from .env
        valid_username = os.getenv('LOGIN_USERNAME', 'admin')
        valid_password = os.getenv('LOGIN_PASSWORD', 'admin123')
        
        if username == valid_username and password == valid_password:
            request.session['authenticated'] = True
            request.session['username'] = username
            messages.success(request, 'Login successful!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials!')
    
    return render(request, 'monitor/login.html')


def custom_logout(request):
    """Custom logout view"""
    request.session.flush()
    messages.success(request, 'Logged out successfully!')
    return redirect('login')


def is_authenticated(request):
    """Check if user is authenticated via session"""
    return request.session.get('authenticated', False)


@require_http_methods(["GET"])
def dashboard(request):
    """Main dashboard view"""
    if not is_authenticated(request):
        return redirect('login')
    
    mode = os.getenv('MODE', 'simulation')
    
    # Get or create initial stats
    stats = NetworkStats.objects.first()
    if not stats:
        stats = NetworkStats.objects.create()
    
    # Create initial log if no logs exist
    if not NetworkLog.objects.exists():
        NetworkLog.objects.create(
            interface_name='System',
            log_type='info',
            message=f'Network Monitor started in {mode.upper()} mode',
            resolved=True
        )
    
    context = {
        'mode': mode,
        'username': request.session.get('username', 'Admin'),
        'stats': stats,
    }
    
    return render(request, 'monitor/dashboard.html', context)


@require_http_methods(["GET"])
def get_interfaces(request):
    """API endpoint to get network interfaces"""
    if not is_authenticated(request):
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    
    mode = os.getenv('MODE', 'simulation')
    
    if mode == 'device':
        handler = CiscoDeviceHandler()
    else:
        handler = SimulationHandler()
    
    interfaces = handler.get_interfaces()
    
    # Update or create interface records (with error handling for locked database)
    for interface_data in interfaces:
        try:
            existing = NetworkInterface.objects.filter(interface_name=interface_data['name']).first()
            
            if existing:
                # Check if status changed
                old_status = existing.status
                new_status = interface_data['status']
                
                # Update the interface
                existing.interface_type = interface_data['type']
                existing.ip_address = interface_data.get('ip_address')
                existing.status = new_status
                existing.save()
                
                # Log status changes
                if old_status != new_status:
                    if new_status == 'down':
                        NetworkLog.objects.create(
                            interface_name=interface_data['name'],
                            log_type='error',
                            message=f'Interface went DOWN',
                            resolved=False
                        )
                    else:
                        NetworkLog.objects.create(
                            interface_name=interface_data['name'],
                            log_type='success',
                            message=f'Interface came back UP (auto-recovery)',
                            resolved=True
                        )
            else:
                # Create new interface
                NetworkInterface.objects.create(
                    interface_name=interface_data['name'],
                    interface_type=interface_data['type'],
                    ip_address=interface_data.get('ip_address'),
                    status=interface_data['status']
                )
        except Exception as e:
            print(f"Error updating interface {interface_data['name']}: {e}")
            continue
    
    return JsonResponse({'interfaces': interfaces})


@require_http_methods(["POST"])
def fix_interface(request):
    """API endpoint to fix a down interface"""
    if not is_authenticated(request):
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    
    data = json.loads(request.body)
    interface_name = data.get('interface_name')
    
    if not interface_name:
        return JsonResponse({'success': False, 'message': 'Interface name required'})
    
    mode = os.getenv('MODE', 'simulation')
    
    if mode == 'device':
        handler = CiscoDeviceHandler()
    else:
        handler = SimulationHandler()
    
    result = handler.fix_interface(interface_name)
    
    # Log the action
    if result['success']:
        NetworkLog.objects.create(
            interface_name=interface_name,
            log_type='success',
            message=result['message'],
            resolved=True
        )
    else:
        NetworkLog.objects.create(
            interface_name=interface_name,
            log_type='error',
            message=result['message'],
            resolved=False
        )
    
    return JsonResponse(result)


@require_http_methods(["GET"])
def get_logs(request):
    """API endpoint to get network logs"""
    if not is_authenticated(request):
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    
    limit = int(request.GET.get('limit', 50))
    logs = NetworkLog.objects.all()[:limit]
    
    logs_data = [{
        'id': log.id,
        'interface_name': log.interface_name,
        'log_type': log.log_type,
        'message': log.message,
        'timestamp': log.timestamp.isoformat(),
        'resolved': log.resolved,
    } for log in logs]
    
    return JsonResponse({'logs': logs_data})


@require_http_methods(["GET"])
def get_stats(request):
    """API endpoint to get network statistics"""
    if not is_authenticated(request):
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    
    # Calculate current stats
    total_interfaces = NetworkInterface.objects.count()
    interfaces_up = NetworkInterface.objects.filter(status='up').count()
    interfaces_down = NetworkInterface.objects.filter(status='down').count()
    total_errors = NetworkLog.objects.filter(log_type='error', resolved=False).count()
    
    uptime_percentage = (interfaces_up / total_interfaces * 100) if total_interfaces > 0 else 100
    
    # Update stats
    NetworkStats.objects.create(
        total_interfaces=total_interfaces,
        interfaces_up=interfaces_up,
        interfaces_down=interfaces_down,
        total_errors=total_errors,
        uptime_percentage=uptime_percentage
    )
    
    # Get historical data for charts
    historical_stats = NetworkStats.objects.all()[:24]  # Last 24 entries
    
    chart_data = {
        'labels': [stat.timestamp.strftime('%H:%M') for stat in reversed(historical_stats)],
        'uptime': [stat.uptime_percentage for stat in reversed(historical_stats)],
        'interfaces_up': [stat.interfaces_up for stat in reversed(historical_stats)],
        'interfaces_down': [stat.interfaces_down for stat in reversed(historical_stats)],
    }
    
    stats_data = {
        'total_interfaces': total_interfaces,
        'interfaces_up': interfaces_up,
        'interfaces_down': interfaces_down,
        'total_errors': total_errors,
        'uptime_percentage': round(uptime_percentage, 2),
        'chart_data': chart_data,
    }
    
    return JsonResponse(stats_data)


@require_http_methods(["POST"])
def clear_logs(request):
    """API endpoint to clear all logs"""
    if not is_authenticated(request):
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    
    NetworkLog.objects.all().delete()
    
    return JsonResponse({'success': True, 'message': 'All logs cleared'})
