# Network Monitor - Cisco Network Interface Management System

A professional Django-based web application for monitoring and managing Cisco network interfaces. The system supports both real Cisco device connections and simulation mode for testing and demonstration.

## 🌟 Features

- **Real-time Network Monitoring**: Monitor network interface status in real-time
- **Dual Mode Support**: 
  - **Device Mode**: Connect to actual Cisco IOS devices via SSH
  - **Simulation Mode**: Test with simulated network interfaces
- **Automatic Interface Recovery**: Automatically attempt to fix down interfaces
- **Manual Intervention Alerts**: Popup notifications for issues requiring manual attention
- **Activity Logging**: Track all network events with timestamps
- **Interactive Dashboard**: Modern, responsive UI with real-time updates
- **Network Statistics**: Visual charts showing uptime, interface status over time
- **Secure Authentication**: Static credential-based login system

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git (optional, for cloning)

## 🚀 Installation & Setup

### Step 1: Extract the Project

Extract the `network_monitor.zip` file to your desired location:

```bash
unzip network_monitor.zip
cd network_monitor
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

Copy the example environment file and configure it:

```bash
# On Windows
copy env.example .env

# On macOS/Linux
cp env.example .env
```

Edit `.env` file with your preferred settings:

```env
# Network Monitor Configuration

# Mode: 'simulation' or 'device'
MODE=simulation

# Cisco Device Configuration (only used when MODE=device)
CISCO_HOST=192.168.1.1
CISCO_USERNAME=admin
CISCO_PASSWORD=cisco
CISCO_ENABLE_PASSWORD=enable

# Django Secret Key
SECRET_KEY=django-insecure-your-secret-key-here-change-in-production

# Debug Mode
DEBUG=True

# Static Login Credentials
LOGIN_USERNAME=admin
LOGIN_PASSWORD=admin123
```

**Important Configuration Options:**

- **MODE**: 
  - Set to `simulation` for testing without a Cisco device
  - Set to `device` to connect to an actual Cisco router/switch
  
- **CISCO_***: Only needed when MODE=device
  - Configure with your actual Cisco device credentials

- **LOGIN_***: Change these to set your dashboard login credentials

### Step 5: Initialize Database

```bash
python manage.py migrate
```

### Step 6: Create Superuser (Optional)

If you want to access Django admin panel:

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account.

### Step 7: Run the Development Server

```bash
python manage.py runserver
```

The application will be available at: **http://127.0.0.1:8000**

## 📱 Using the Application

### Login

1. Navigate to http://127.0.0.1:8000
2. Use the default credentials:
   - **Username**: admin
   - **Password**: admin123
   
   (Or use the credentials you set in `.env`)

### Dashboard Features

#### 1. **Network Statistics Cards**
- **Total Interfaces**: Shows total number of network interfaces
- **Interfaces Up**: Count of operational interfaces
- **Interfaces Down**: Count of down interfaces (requiring attention)
- **Uptime**: Overall network uptime percentage

#### 2. **Network Interfaces Panel**
- View all network interfaces with their status
- See IP addresses and interface types
- **Fix Button**: Appears for down interfaces - click to attempt automatic recovery
- Real-time status updates every 5 seconds

#### 3. **Activity Logs Panel**
- View chronological log of all network events
- Color-coded by severity (info, success, warning, error)
- Shows timestamps for each event
- **Clear Button**: Remove all logs

#### 4. **Network Statistics Chart**
- Visual representation of network health over time
- Tracks uptime percentage
- Shows interfaces up/down trends
- Updates automatically

#### 5. **Notifications**
- Automatic popup alerts for critical issues
- Appears when an interface cannot be automatically fixed
- Requires manual intervention notification

## 🔧 Operating Modes

### Simulation Mode (Default)

Perfect for testing and demonstration without hardware:

- Simulates 8 network interfaces (mix of GigabitEthernet, FastEthernet, Serial)
- Interfaces randomly go up/down to simulate real-world scenarios
- Automatic recovery attempts with 70% success rate
- Generates realistic activity logs
- No actual network device required

**To use Simulation Mode:**
```env
MODE=simulation
```

### Device Mode

Connect to actual Cisco IOS devices:

- Connects via SSH to Cisco routers/switches
- Executes real IOS commands
- Retrieves actual interface status
- Can execute fix commands (`no shutdown`)
- Requires network access to the device

**To use Device Mode:**

1. Update `.env`:
```env
MODE=device
CISCO_HOST=192.168.1.1
CISCO_USERNAME=admin
CISCO_PASSWORD=cisco
CISCO_ENABLE_PASSWORD=enable
```

2. Ensure the Cisco device:
   - Has SSH enabled
   - Is reachable from your network
   - Has the correct credentials configured

## 🎨 Modern UI Features

The interface uses a modern design inspired by contemporary UI frameworks:

- **Responsive Design**: Works on desktop, tablet, and mobile
- **Real-time Updates**: Auto-refreshes every 5 seconds
- **Smooth Animations**: Professional transitions and effects
- **Color-coded Status**: Easy visual identification
- **Interactive Charts**: Chart.js powered visualizations
- **Intuitive Navigation**: Clean, user-friendly layout

## 📊 API Endpoints

The application provides RESTful API endpoints:

- `GET /api/interfaces/` - Get all network interfaces
- `POST /api/fix-interface/` - Attempt to fix a down interface
- `GET /api/logs/` - Get activity logs
- `GET /api/stats/` - Get network statistics
- `POST /api/clear-logs/` - Clear all logs

## 🔐 Security Considerations

**For Production Use:**

1. Change `SECRET_KEY` in `.env` to a strong, random value
2. Set `DEBUG=False` in `.env`
3. Update login credentials from defaults
4. Configure proper `ALLOWED_HOSTS` in settings.py
5. Use HTTPS/SSL encryption
6. Implement proper user authentication (replace static credentials)
7. Secure SSH credentials for device mode
8. Set up proper firewall rules

## 🛠️ Troubleshooting

### Issue: "No module named 'django'"
**Solution**: Install dependencies
```bash
pip install -r requirements.txt
```

### Issue: "Connection refused" in Device Mode
**Solution**: 
- Check CISCO_HOST is correct
- Verify network connectivity: `ping CISCO_HOST`
- Ensure SSH is enabled on Cisco device
- Verify firewall rules allow SSH (port 22)

### Issue: "Authentication failed" in Device Mode
**Solution**:
- Verify credentials in `.env` are correct
- Check user has proper privileges on Cisco device
- Enable password might be required - set CISCO_ENABLE_PASSWORD

### Issue: "Port already in use"
**Solution**: 
```bash
# Use a different port
python manage.py runserver 8080
```

### Issue: Charts not displaying
**Solution**: 
- Check internet connection (Chart.js loads from CDN)
- Clear browser cache
- Try a different browser

## 📁 Project Structure

```
network_monitor/
├── config/                 # Django project configuration
│   ├── __init__.py
│   ├── settings.py        # Main settings
│   ├── urls.py            # URL routing
│   ├── wsgi.py
│   └── asgi.py
├── monitor/               # Main application
│   ├── migrations/        # Database migrations
│   ├── templates/         # HTML templates
│   │   └── monitor/
│   │       ├── login.html
│   │       └── dashboard.html
│   ├── models.py          # Database models
│   ├── views.py           # View logic
│   ├── urls.py            # App URL routing
│   ├── cisco_handler.py   # Cisco device & simulation handler
│   ├── admin.py           # Admin configuration
│   └── apps.py
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── .env                  # Your configuration (create this)
├── .gitignore
└── README.md             # This file
```

## 🔄 Development Workflow

### Making Changes

1. Modify code as needed
2. If models changed: 
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
3. Restart server: `Ctrl+C` then `python manage.py runserver`

### Adding New Interfaces (Simulation Mode)

Edit `monitor/cisco_handler.py` and modify the `INTERFACES` list in `SimulationHandler` class.

### Customizing Auto-Refresh Interval

Edit `monitor/templates/monitor/dashboard.html` and change:
```javascript
updateInterval = setInterval(async () => {
    // ...
}, 5000); // Change 5000 to desired milliseconds
```

## 🌐 Accessing from Other Devices

To access the dashboard from other devices on your network:

1. Find your computer's IP address:
   ```bash
   # Windows
   ipconfig
   
   # macOS/Linux
   ifconfig
   ```

2. Run server on all interfaces:
   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```

3. Access from other devices: `http://YOUR_IP:8000`

## 📝 Default Credentials

**Dashboard Login:**
- Username: `admin`
- Password: `admin123`

**Cisco Device (Device Mode):**
- Configure in `.env` file with your actual device credentials

## 🆘 Support & Documentation

- Django Documentation: https://docs.djangoproject.com/
- Paramiko (SSH): https://www.paramiko.org/
- Chart.js: https://www.chartjs.org/

## 📄 License

This project is provided as-is for educational and demonstration purposes.

## 🎯 Future Enhancements

Potential features for future versions:
- Multi-user authentication with roles
- SNMP monitoring support
- Email/SMS alerts
- Configuration backup
- Multiple device support
- Historical data analysis
- Export reports (PDF/Excel)
- WebSocket for true real-time updates
- Dark mode theme
- Mobile app

---

**Built with Django, Chart.js, and ❤️**
