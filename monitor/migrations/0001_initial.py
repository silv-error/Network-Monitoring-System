# Generated migration file

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NetworkInterface',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('interface_name', models.CharField(max_length=100)),
                ('interface_type', models.CharField(max_length=50)),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True)),
                ('status', models.CharField(default='up', max_length=20)),
                ('last_checked', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['interface_name'],
            },
        ),
        migrations.CreateModel(
            name='NetworkLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('interface_name', models.CharField(max_length=100)),
                ('log_type', models.CharField(choices=[('info', 'Info'), ('warning', 'Warning'), ('error', 'Error'), ('success', 'Success')], default='info', max_length=20)),
                ('message', models.TextField()),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('resolved', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='NetworkStats',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_interfaces', models.IntegerField(default=0)),
                ('interfaces_up', models.IntegerField(default=0)),
                ('interfaces_down', models.IntegerField(default=0)),
                ('total_errors', models.IntegerField(default=0)),
                ('uptime_percentage', models.FloatField(default=100.0)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Network Stats',
                'ordering': ['-timestamp'],
            },
        ),
    ]
