from flask import Flask, render_template, redirect, url_for, request, session
from datetime import datetime, timedelta
import reservations
import database as dbl
from pwsecurity import HashPassword, CheckHash
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, 
            template_folder='../frontend/templates', 
            static_folder='../frontend/static')
app.secret_key = os.getenv('SECRET_KEY', 'dev_key_for_testing')

@app.route('/')
def login():
    return render_template('login.html', user_logged_in=False)

@app.route('/login/submit', methods=['POST'])
def submit_login():
    email = request.form.get('email')
    password_pt = request.form.get('password')

    db = dbl.get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()
    cursor.close()
    db.close()

    if user and CheckHash(password_pt, user['password_hash'].encode('utf-8')):
        session['user_id'] = user['user_id']
        session['user_name'] = user['name']
        return redirect(url_for('dashboard'))
    else:
        return render_template('login.html', user_logged_in=False, error="Invalid email or password.")

@app.route('/register')
def register():
    return render_template('register.html', user_logged_in=False)

@app.route('/register/submit', methods=["POST"])
def submit_registration():
    db = dbl.get_db_connection()
    cursor = db.cursor()
    name = request.form["name"]
    email = request.form["email"]
    password_pt = request.form["password"]
    role = request.form["role"]
    password_hash = HashPassword(password_pt).decode('utf-8')
    
    cursor.execute("SELECT * FROM users WHERE email = %s;", (email,))
    if not cursor.fetchone():
        cursor.execute(
            "INSERT INTO users (name, email, password_hash, role) VALUES (%s, %s, %s, %s);",
            (name, email, password_hash, role)
        )
        db.commit()
        cursor.execute("SELECT user_id FROM users WHERE email = %s;", (email,))
        user = cursor.fetchone()
        session['user_id'] = user['user_id']
        session['user_name'] = name
        cursor.close()
        db.close()
        return redirect(url_for('dashboard'))
    else:
        cursor.close()
        db.close()
        return render_template('register.html', user_logged_in=False, account_exists=True)

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    try:
        db = dbl.get_db_connection()
        cursor = db.cursor() 
        cursor.execute("SELECT * FROM equipment")
        equipment_list = cursor.fetchall()
        cursor.close()
        db.close()
        return render_template('equipment.html', equipment=equipment_list, user_logged_in=True)
    except Exception as e:
        return f"Database Error: {str(e)}", 500

@app.route('/book/<int:equipment_id>')
def render_booking_page(equipment_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    try:
        db = dbl.get_db_connection()
        cursor = db.cursor()
        cursor.execute("SELECT equipment_id, name, status FROM equipment WHERE equipment_id = %s", (equipment_id,))
        selected_item = cursor.fetchone()
        
        if not selected_item:
            cursor.close()
            db.close()
            return "Equipment not found", 404
            
        if selected_item['status'] == 'repair':
            cursor.close()
            db.close()
            return "This equipment is under repair and unavailable for booking.", 403

        now = datetime.now()
        available_dates = []
        for i in range(14):
            date = now + timedelta(days=i)
            available_dates.append({'value': date.strftime('%Y-%m-%d'), 'label': date.strftime('%A, %b %d')})
        
        full_day_hours = range(8, 21)
        today_str = now.strftime('%Y-%m-%d')
        grace_period_hour = now.hour + 2 if now.minute > 30 else now.hour + 1
        
        today_hours = []
        for h in full_day_hours:
            if h >= grace_period_hour:
                dt = datetime.strptime(f"{h}", "%H")
                today_hours.append({'value': f"{h:02d}:00", 'label': dt.strftime("%I:%M %p").lstrip("0")})

        other_day_hours = []
        for h in full_day_hours:
            dt = datetime.strptime(f"{h}", "%H")
            other_day_hours.append({'value': f"{h:02d}:00", 'label': dt.strftime("%I:%M %p").lstrip("0")})

        cursor.close()
        db.close()
        return render_template('book.html', item=selected_item, dates=available_dates, today_date=today_str, today_hours=today_hours, other_hours=other_day_hours)
    except Exception as e:
        return f"Database Error: {str(e)}", 500

@app.route('/book/submit', methods=['POST'])
def submit_booking():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    equipment_id = request.form['equipment_id']
    date = request.form['booking_date']
    start_hour = request.form['start_hour']
    end_hour = request.form['end_hour']
    start_time_str = f"{date}T{start_hour}"
    end_time_str = f"{date}T{end_hour}"
    user_id = session['user_id']
    result = reservations.create_reservation(user_id, equipment_id, start_time_str, end_time_str)
    if result['status'] == 'success':
        return redirect(url_for('dashboard'))
    else:
        return f"<h3>Error</h3><p>{result['message']}</p><a href='/dashboard'>Back</a>"

if __name__ == '__main__':
    app.run(debug=True)