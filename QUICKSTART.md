# 🚀 QUICK START GUIDE

## Getting Started in 5 Minutes

### 1. Extract the Files
```bash
unzip network_monitor.zip
cd network_monitor
```

### 2. Install Python Packages
```bash
pip install -r requirements.txt
```

### 3. Setup Configuration
```bash
# Windows
copy env.example .env

# Mac/Linux
cp env.example .env
```

### 4. Initialize Database
```bash
python manage.py migrate
```

### 5. Run the Server
```bash
python manage.py runserver
```

### 6. Open Your Browser
Navigate to: **http://127.0.0.1:8000**

### 7. Login
- **Username**: admin
- **Password**: admin123

## That's It! 🎉

The system is now running in **simulation mode** with 8 virtual network interfaces.

You'll see:
- Real-time interface status updates
- Simulated network failures and recoveries
- Activity logs
- Network statistics charts

## Need to Connect to Real Cisco Device?

Edit `.env` file:
```env
MODE=device
CISCO_HOST=192.168.1.1
CISCO_USERNAME=your_username
CISCO_PASSWORD=your_password
```

Then restart the server.

## Troubleshooting

**Error: "No module named django"**
→ Run: `pip install -r requirements.txt`

**Port already in use**
→ Run: `python manage.py runserver 8080`

**Can't login**
→ Check credentials in `.env` file

---

For detailed documentation, see **README.md**
