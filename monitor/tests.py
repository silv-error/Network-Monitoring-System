from django.test import TestCase, Client
from django.urls import reverse
from .models import NetworkInterface, NetworkLog, NetworkStats
from .cisco_handler import SimulationHandler


class NetworkInterfaceModelTest(TestCase):
    def setUp(self):
        self.interface = NetworkInterface.objects.create(
            interface_name='GigabitEthernet0/0',
            interface_type='ethernet',
            ip_address='192.168.1.1',
            status='up'
        )

    def test_interface_creation(self):
        self.assertEqual(self.interface.interface_name, 'GigabitEthernet0/0')
        self.assertEqual(self.interface.status, 'up')

    def test_interface_str(self):
        self.assertEqual(str(self.interface), 'GigabitEthernet0/0 - up')


class SimulationHandlerTest(TestCase):
    def setUp(self):
        self.handler = SimulationHandler()

    def test_get_interfaces(self):
        interfaces = self.handler.get_interfaces()
        self.assertIsInstance(interfaces, list)
        self.assertGreater(len(interfaces), 0)

    def test_interface_structure(self):
        interfaces = self.handler.get_interfaces()
        interface = interfaces[0]
        self.assertIn('name', interface)
        self.assertIn('status', interface)
        self.assertIn('type', interface)


class ViewsTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_login_page(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_login_success(self):
        response = self.client.post(reverse('login'), {
            'username': 'admin',
            'password': 'admin123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after login

    def test_dashboard_requires_auth(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
