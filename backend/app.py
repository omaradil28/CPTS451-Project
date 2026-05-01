import os
from datetime import datetime, timedelta
from flask import Flask, render_template, redirect, url_for, request, session
from dotenv import load_dotenv

# Database and Security modules
import database as dbl
import reservations
from pwsecurity import HashPassword, CheckHash
from user_bookings import get_bookings, cancel_booking

load_dotenv()

app = Flask(__name__, 
            template_folder='../frontend/templates', 
            static_folder='../frontend/static')

app.secret_key = os.getenv('FLASK_SECRET_KEY', 'dev_key_for_testing')
app.permanent_session_lifetime = timedelta(hours=6)

@app.route('/')
def login():
    if "user_id" in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html', user_logged_in=False)

@app.route('/login/submit', methods=["POST"])
def submit_login():
    email = request.form.get("email")
    password_pt = request.form.get("password")
    stay_logged_in = request.form.get("stay_logged_in") is not None

    db = dbl.get_db_connection()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()
    
    cursor.close()
    db.close()

    if user and CheckHash(password_pt, user["password_hash"].encode('utf-8')):
        session.permanent = stay_logged_in
        session["user_id"] = user["user_id"]
        session["user_name"] = user["name"]
        session["user_email"] = user["email"]
        session["user_role"] = user["role"]
        return redirect(url_for('dashboard'))
    
    return render_template('login.html', user_logged_in=False, bad_login=True, error="Invalid email or password.")

@app.route('/register')
def register():
    return render_template('register.html')

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
        cursor.execute("INSERT INTO users (name, email, password_hash, role) VALUES (%s, %s, %s, %s);", 
                       (name, email, password_hash, role))
        db.commit()
        
        cursor.execute("SELECT user_id, role FROM users WHERE email = %s;", (email,))
        user = cursor.fetchone()
        
        session['user_id'] = user['user_id']
        session['user_name'] = name
        session['user_role'] = user['role']
        
        cursor.close()
        db.close()
        return redirect(url_for('dashboard'))
    
    cursor.close()
    db.close()
    return render_template('register.html', account_exists=True)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session: 
        return redirect(url_for('login'))
    
    db = dbl.get_db_connection()
    cursor = db.cursor() 
    cursor.execute("SELECT * FROM equipment")
    equipment_list = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template('equipment.html', equipment=equipment_list, user_logged_in=True)

@app.route('/book/<int:equipment_id>')
def render_booking_page(equipment_id, error=None):
    if 'user_id' not in session: return redirect(url_for('login'))
    
    db = dbl.get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM equipment WHERE equipment_id = %s", (equipment_id,))
    item = cursor.fetchone()
    
    if not item or item['status'] == 'repair':
        cursor.close()
        db.close()
        return "Equipment unavailable", 403
    
    now = datetime.now()
    available_dates = [{'value': (now + timedelta(days=i)).strftime('%Y-%m-%d'), 
                        'label': (now + timedelta(days=i)).strftime('%A, %b %d')} for i in range(14)]
    
    grace_period_hour = now.hour + 2 if now.minute > 30 else now.hour + 1
    today_hours = [{'value': f"{h:02d}:00", 'label': datetime.strptime(f"{h}", "%H").strftime("%I:%M %p").lstrip("0")} 
                   for h in range(8, 21) if h >= grace_period_hour]
    other_hours = [{'value': f"{h:02d}:00", 'label': datetime.strptime(f"{h}", "%H").strftime("%I:%M %p").lstrip("0")} 
                   for h in range(8, 21)]
    
    cursor.close()
    db.close()
    
    return render_template('book.html', item=item, dates=available_dates, 
                           today_date=now.strftime('%Y-%m-%d'), today_hours=today_hours, 
                           other_hours=other_hours, error=(error is not None), errorMsg=error)

@app.route('/book/submit', methods=['POST'])
def submit_booking():
    if 'user_id' not in session: return redirect(url_for('login'))
    
    start_dt = f"{request.form['booking_date']}T{request.form['start_hour']}"
    end_dt = f"{request.form['booking_date']}T{request.form['end_hour']}"
    
    res = reservations.create_reservation(session['user_id'], request.form['equipment_id'], start_dt, end_dt)
    
    if res['status'] == 'success':
        return redirect(url_for('dashboard'))
    else:
        return render_booking_page(request.form['equipment_id'], "Error: " + res['message'])

@app.route('/bookings')
def my_bookings_page():
    if 'user_id' not in session: return redirect(url_for('login'))
    bookings_list = get_bookings(session['user_id'])
    return render_template('my_bookings.html', bookings=bookings_list)

@app.route('/bookings/cancel/<int:reservation_id>')
def cancel_booking_conn(reservation_id):
    if 'user_id' not in session: return redirect(url_for('login'))
    cancel_booking(reservation_id)
    return redirect(url_for('my_bookings_page'))

@app.route('/admin')
def admin_panel():
    if 'user_id' not in session or session.get('user_role') != 'technician':
        return "Access Denied", 403
    
    db = dbl.get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM equipment")
    equipment_list = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template('admin.html', equipment=equipment_list)

@app.route('/admin/add', methods=['POST'])
def admin_add():
    if session.get('user_role') != 'technician': return "Unauthorized", 403
    db = dbl.get_db_connection()
    cursor = db.cursor()
    cursor.execute("INSERT INTO equipment (name, status) VALUES (%s, 'available')", (request.form.get('name'),))
    db.commit()
    cursor.close()
    db.close()
    return redirect(url_for('admin_panel'))

@app.route('/admin/update/<int:equipment_id>', methods=['POST'])
def admin_update(equipment_id):
    if session.get('user_role') != 'technician': return "Unauthorized", 403
    new_name = request.form.get('name')
    new_status = request.form.get('status')
    
    db = dbl.get_db_connection()
    cursor = db.cursor()
    try:
        cursor.execute("UPDATE equipment SET name = %s, status = %s WHERE equipment_id = %s", 
                       (new_name, new_status, equipment_id))
        db.commit()
    except Exception as e:
        return f"Update Failed: {str(e)}", 500
    finally:
        cursor.close()
        db.close()
    return redirect(url_for('admin_panel'))

@app.route('/admin/delete/<int:equipment_id>', methods=['POST'])
def admin_delete(equipment_id):
    if session.get('user_role') != 'technician': return "Unauthorized", 403
    db = dbl.get_db_connection()
    cursor = db.cursor()
    try:
        cursor.execute("DELETE FROM equipment WHERE equipment_id = %s", (equipment_id,))
        db.commit()
    except:
        return "Error: Cannot delete item with active reservations.", 400
    finally:
        cursor.close()
        db.close()
    return redirect(url_for('admin_panel'))

if __name__ == '__main__':
    app.run(debug=True)