import serial
import requests

ser = serial.Serial('COM3', 9600)  # Windows: COM3, Linux: /dev/ttyUSB0
USERNAME = "ashutosh"
PASSWORD = "1234"

while True:
    try:
        line = ser.readline().decode('utf-8').strip()
        if "Z:" in line:
            parts = line.split()
            z = int(parts[-1])
            payload = {
                "nmf2": 7.5,  # Simulated/test value
                "thermal": 950,  # Simulated/test value
                "magnet_z": z,
                "radon": 210,  # Simulated/test value
                "username": USERNAME,
                "timestamp": None
            }
            # Login session (if needed, else use API token)
            res = requests.post('http://127.0.0.1:5000/submit_sensor', json=payload)
            print("Sent:", payload, "Response:", res.text)
    except Exception as e:
        print("Error:", e)
