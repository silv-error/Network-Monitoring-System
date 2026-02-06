from django.db import models
from django.utils import timezone


class NetworkInterface(models.Model):
    """Model to store network interface information"""
    interface_name = models.CharField(max_length=100)
    interface_type = models.CharField(max_length=50)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    status = models.CharField(max_length=20, default='up')
    last_checked = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['interface_name']

    def __str__(self):
        return f"{self.interface_name} - {self.status}"


class NetworkLog(models.Model):
    """Model to store network event logs"""
    LOG_TYPES = [
        ('info', 'Info'),
        ('warning', 'Warning'),
        ('error', 'Error'),
        ('success', 'Success'),
    ]

    interface_name = models.CharField(max_length=100)
    log_type = models.CharField(max_length=20, choices=LOG_TYPES, default='info')
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    resolved = models.BooleanField(default=False)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.timestamp} - {self.interface_name}: {self.log_type}"


class NetworkStats(models.Model):
    """Model to store network statistics"""
    total_interfaces = models.IntegerField(default=0)
    interfaces_up = models.IntegerField(default=0)
    interfaces_down = models.IntegerField(default=0)
    total_errors = models.IntegerField(default=0)
    uptime_percentage = models.FloatField(default=100.0)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name_plural = 'Network Stats'

    def __str__(self):
        return f"Stats at {self.timestamp}"
