from flask import Flask, request, jsonify, render_template, send_file, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import csv
import os

app = Flask(__name__, static_url_path='/static', static_folder='static')
app.secret_key = "your_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)
data_log = []

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Sensor log to CSV
def log_to_csv(entry, filename='sensor_log.csv'):
    file_exists = os.path.isfile(filename)
    with open(filename, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=entry.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(entry)

# Alert Functions (सभी पैरामीटर के लिए)
def nmf2_alert(val):
    if val < 4: return "Y007N"
    elif 4 <= val < 6: return "Y007YEL"
    elif 6 <= val < 7: return "Y007YORng"
    elif 7 <= val < 8: return "Y007YR"
    elif 8 <= val < 12: return "Y007YRR"
    elif val >= 12: return "Y007RRR"
    else: return "Y007N"

def thermal_alert(val):
    if val < 600: return "Y011N"
    elif 600 <= val < 700: return "Y011Y"
    elif 700 <= val < 800: return "Y011OR"
    elif 800 <= val < 900: return "Y011R"
    elif 900 <= val < 1000: return "Y011RR"
    elif 1000 <= val < 1100: return "Y011RRR"
    else: return "Y011N"

def magnet_alert(val):
    if val < 230: return "Y009N"
    elif 230 <= val < 240: return "Y009Y"
    elif 240 <= val < 245: return "Y009OR"
    elif 245 <= val < 250: return "Y009R"
    elif 250 <= val < 255: return "Y009RR"
    elif 255 <= val < 265: return "Y009RRR"
    else: return "Y009N"

def radon_alert(val):
    if val < 100: return "Y010N"
    elif 100 <= val < 150: return "Y010Y"
    elif 150 <= val < 200: return "Y010OR"
    elif 200 <= val < 250: return "Y010R"
    elif 250 <= val < 265: return "Y010RR"
    elif 265 <= val < 400: return "Y010RRR"
    else: return "Y010N"

@app.route('/')
def index():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            return "User already exists!"
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['username'] = username
            return redirect(url_for('index'))
        return "Invalid username or password"
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/submit_sensor', methods=['POST'])
def receive_sensor():
    if 'username' not in session:
        return jsonify({"error": "Not logged in"}), 401
    data = request.json
    nmf2 = float(data['nmf2'])
    thermal = float(data['thermal'])
    magnet_z = int(data['magnet_z'])
    radon = float(data['radon'])
    # आप चाहें तो electron_density, kp_index आदि भी जोड़ सकते हैं

    alert_data = {
        "nmf2": nmf2,
        "thermal": thermal,
        "magnet_z": magnet_z,
        "radon": radon,
        "alert_nmf2": nmf2_alert(nmf2),
        "alert_thermal": thermal_alert(thermal),
        "alert_magnet": magnet_alert(magnet_z),
        "alert_radon": radon_alert(radon),
        "username": session['username'],
        "timestamp": data.get("timestamp", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    }
    data_log.append(alert_data)
    log_to_csv(alert_data)
    return jsonify(alert_data)

@app.route('/data')
def send_data():
    return jsonify(data_log[-100:])

@app.route('/download_csv')
def download_csv():
    return send_file("sensor_log.csv", as_attachment=True)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Default user create (only if not exists)
        if not User.query.filter_by(username="ashutosh").first():
            user = User(username="ashutosh")
            user.set_password("1234")
            db.session.add(user)
            db.session.commit()
    app.run(debug=True)
