import os
import random
import time
from datetime import datetime
from typing import List, Dict


class CiscoDeviceHandler:
    """Handler for actual Cisco device connections"""
    
    def __init__(self):
        self.host = os.getenv('CISCO_HOST', '192.168.1.1')
        self.username = os.getenv('CISCO_USERNAME', 'admin')
        self.password = os.getenv('CISCO_PASSWORD', 'cisco')
        self.enable_password = os.getenv('CISCO_ENABLE_PASSWORD', 'enable')
        self.connection = None
    
    def connect(self):
        """Connect to Cisco device via SSH"""
        try:
            import paramiko
            
            self.connection = paramiko.SSHClient()
            self.connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.connection.connect(
                hostname=self.host,
                username=self.username,
                password=self.password,
                timeout=10
            )
            return True
        except Exception as e:
            print(f"Connection error: {e}")
            return False
    
    def execute_command(self, command: str) -> str:
        """Execute command on Cisco device"""
        if not self.connection:
            if not self.connect():
                return ""
        
        try:
            stdin, stdout, stderr = self.connection.exec_command(command)
            return stdout.read().decode('utf-8')
        except Exception as e:
            print(f"Command execution error: {e}")
            return ""
    
    def get_interfaces(self) -> List[Dict]:
        """Get list of interfaces from Cisco device"""
        if not self.connect():
            return []
        
        output = self.execute_command("show ip interface brief")
        interfaces = []
        
        # Parse output (simplified)
        lines = output.split('\n')
        for line in lines[1:]:  # Skip header
            if line.strip():
                parts = line.split()
                if len(parts) >= 6:
                    interfaces.append({
                        'name': parts[0],
                        'ip_address': parts[1] if parts[1] != 'unassigned' else None,
                        'status': parts[4].lower(),
                        'protocol': parts[5].lower(),
                        'type': 'ethernet' if 'Ethernet' in parts[0] else 'other',
                    })
        
        return interfaces
    
    def fix_interface(self, interface_name: str) -> Dict:
        """Attempt to fix a down interface"""
        if not self.connect():
            return {
                'success': False,
                'message': 'Could not connect to device',
                'requires_manual_intervention': True
            }
        
        # Try to bring up the interface
        commands = [
            f"configure terminal",
            f"interface {interface_name}",
            "no shutdown",
            "end"
        ]
        
        try:
            for cmd in commands:
                self.execute_command(cmd)
            
            # Wait and check status
            time.sleep(2)
            output = self.execute_command(f"show interface {interface_name}")
            
            if 'up' in output.lower():
                return {
                    'success': True,
                    'message': f'Interface {interface_name} brought up successfully',
                    'requires_manual_intervention': False
                }
            else:
                return {
                    'success': False,
                    'message': f'Interface {interface_name} could not be brought up - manual intervention required',
                    'requires_manual_intervention': True
                }
        except Exception as e:
            return {
                'success': False,
                'message': f'Error fixing interface: {str(e)}',
                'requires_manual_intervention': True
            }
    
    def disconnect(self):
        """Close connection to device"""
        if self.connection:
            self.connection.close()


class SimulationHandler:
    """Handler for simulation mode without actual device"""
    
    # Static interface data that changes over time
    INTERFACES = [
        {'name': 'Computer Lab 1', 'type': 'ethernet', 'base_ip': '192.168.1.1'},
        {'name': 'Computer Lab 2', 'type': 'ethernet', 'base_ip': '192.168.1.2'},
        {'name': 'Computer Lab 3', 'type': 'ethernet', 'base_ip': '192.168.2.1'},
        {'name': 'Computer Lab 4', 'type': 'ethernet', 'base_ip': '192.168.2.2'},
        {'name': 'DNS Server', 'type': 'ethernet', 'base_ip': '10.0.0.1'},
        {'name': 'DHCP Server', 'type': 'ethernet', 'base_ip': '10.0.0.2'},
        {'name': 'CONVERGE', 'type': 'serial', 'base_ip': '172.16.0.1'},
        {'name': 'GLOBE', 'type': 'serial', 'base_ip': '172.16.0.2'},
    ]
    
    # Class-level state (shared across instances)
    _interface_states = {}
    _last_check = 0
    
    def __init__(self):
        self.failure_probability = 0.10  # 10% chance of failure per check (increased from 5%)
        self.auto_recovery_probability = 0.15  # 15% chance to auto-recover
        self.check_interval = 5  # Check every 5 seconds (more frequent)
    
    def get_interfaces(self) -> List[Dict]:
        """Get simulated interface status"""
        current_time = time.time()
        interfaces = []
        
        # Initialize states if empty
        if not SimulationHandler._interface_states:
            for interface in self.INTERFACES:
                interface_name = interface['name']
                SimulationHandler._interface_states[interface_name] = {
                    'status': 'up',
                    'last_change': current_time,
                    'down_count': 0,
                    'consecutive_checks': 0,
                }
            SimulationHandler._last_check = current_time
        
        # Check if enough time has passed
        time_since_last = current_time - SimulationHandler._last_check
        should_check = time_since_last >= self.check_interval
        
        for interface in self.INTERFACES:
            interface_name = interface['name']
            state = SimulationHandler._interface_states[interface_name]
            state['consecutive_checks'] += 1
            
            # Simulate changes if interval passed
            if should_check:
                if state['status'] == 'up':
                    # Random chance of going down
                    # Increase probability if interface has been up for a while
                    failure_chance = self.failure_probability
                    if state['consecutive_checks'] > 20:  # Been up for 100+ seconds
                        failure_chance = 0.20  # 20% chance
                    
                    if random.random() < failure_chance:
                        state['status'] = 'down'
                        state['last_change'] = current_time
                        state['down_count'] += 1
                        state['consecutive_checks'] = 0
                        print(f"[SIMULATION] {interface_name} went DOWN at {datetime.now()}")
                
                else:  # status is down
                    # Chance to auto-recover
                    if random.random() < self.auto_recovery_probability:
                        state['status'] = 'up'
                        state['last_change'] = current_time
                        state['consecutive_checks'] = 0
                        print(f"[SIMULATION] {interface_name} AUTO-RECOVERED at {datetime.now()}")
            
            interfaces.append({
                'name': interface_name,
                'type': interface['type'],
                'ip_address': interface['base_ip'],
                'status': state['status'],
                'protocol': state['status'],
                'down_count': state['down_count'],
                'time_in_state': int(current_time - state['last_change']),
            })
        
        if should_check:
            SimulationHandler._last_check = current_time
        
        return interfaces
    
    def fix_interface(self, interface_name: str) -> Dict:
        """Simulate fixing an interface"""
        if interface_name not in SimulationHandler._interface_states:
            return {
                'success': False,
                'message': f'Interface {interface_name} not found',
                'requires_manual_intervention': False
            }
        
        state = SimulationHandler._interface_states[interface_name]
        
        # 70% success rate for simulation
        if random.random() < 0.7:
            state['status'] = 'up'
            state['last_change'] = time.time()
            state['consecutive_checks'] = 0
            
            return {
                'success': True,
                'message': f'Interface {interface_name} brought up successfully (simulated)',
                'requires_manual_intervention': False
            }
        else:
            return {
                'success': False,
                'message': f'Interface {interface_name} could not be brought up - requires manual intervention (simulated)',
                'requires_manual_intervention': True
            }
