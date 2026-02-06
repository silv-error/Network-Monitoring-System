from django.contrib import admin
from .models import NetworkInterface, NetworkLog, NetworkStats


@admin.register(NetworkInterface)
class NetworkInterfaceAdmin(admin.ModelAdmin):
    list_display = ['interface_name', 'interface_type', 'ip_address', 'status', 'last_checked']
    list_filter = ['status', 'interface_type']
    search_fields = ['interface_name', 'ip_address']


@admin.register(NetworkLog)
class NetworkLogAdmin(admin.ModelAdmin):
    list_display = ['timestamp', 'interface_name', 'log_type', 'message', 'resolved']
    list_filter = ['log_type', 'resolved', 'timestamp']
    search_fields = ['interface_name', 'message']


@admin.register(NetworkStats)
class NetworkStatsAdmin(admin.ModelAdmin):
    list_display = ['timestamp', 'total_interfaces', 'interfaces_up', 'interfaces_down', 'uptime_percentage']
    list_filter = ['timestamp']
