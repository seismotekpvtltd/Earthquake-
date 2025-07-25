earthquake-dashboard/
├── server.py
├── requirements.txt
├── magnetometer_reader.py
├── templates/
│   ├── dashboard.html
│   ├── login.html
│   └── register.html
└── sensor_log.csv  # (auto-generated)

Earthquake Dashboard System

Features:
- User registration/login/logout (SQLite backend)
- Sensor data: Nmf2, Thermal, Magnetometer Z, Radon
- Real-time alerts (code as per IMPC/ISRO/your doc)
- CSV logging, download
- Real-time graphs (Chart.js)
- Hardware connectivity: Arduino Magnetometer, Radon, Thermal
- Error/status codes: WiFi, Data, Visual, Correction, etc.
- Extendable for MQTT, Email, WhatsApp, etc.

How to Run:
1. pip install -r requirements.txt
2. python server.py
3. Arduino connect, upload code, run magnetometer_reader.py
4. Open http://127.0.0.1:5000/ in browser
5. Login (ashutosh/1234), use dashboard

All alert codes and logic as per your document are implemented in server.py.


Kindly go https://github.com/Ashugee2825/Earthquake-dashboard

