from flask import Flask, render_template, redirect, url_for, request
import MySQLdb
import MySQLdb.cursors
import reservations
import database as dbl
from dotenv import load_dotenv
from pwsecurity import HashPassword
import os

# Load environment variables from .env in the project root
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '../.env'))

app = Flask(__name__, 
            template_folder='../frontend/templates', 
            static_folder='../frontend/static')

@app.route('/')
def login():
    return render_template('login.html', user_logged_in=False)

@app.route('/register')
def register():
    return render_template('register.html', user_logged_in=False)

@app.route('/register/submit', methods=["POST"])
def submit_registration():
    db = dbl.get_db_connection()
    cursor = db.cursor()

    # Get names from form
    name = request.form["name"]
    email = request.form["email"]
    password_pt = request.form["password"]
    role = request.form["role"]

    password_hash = HashPassword(password_pt).decode('utf-8')

    # Check if email already exists in database
    emailExists = cursor.execute(
        """
        SELECT * FROM users 
            WHERE email = %s;
        """,
        (email,)
    )

    if not emailExists:
        # Insert into sql database (currently only students)
        cursor.execute(
            """
            INSERT INTO users (name, email, password_hash, role)
                VALUES (%s, %s, %s, %s);
            """,
            (name, email, password_hash, role)
        )

        db.commit()
        cursor.close()
        db.close()

        return redirect(url_for('login'))
    
    else:
        cursor.close()
        db.close()

        return render_template('register.html', user_logged_in=False, account_exists=True)


@app.route('/dashboard')
def dashboard():
    try:
        db = dbl.get_db_connection()
        # FIXED: Removed (dictionary=True) because dbl.get_db_connection sets DictCursor
        cursor = db.cursor() 
        
        cursor.execute("SELECT * FROM equipment")
        equipment_list = cursor.fetchall()
        
        cursor.close()
        db.close()
        
        return render_template('equipment.html', equipment=equipment_list, user_logged_in=True)
    except Exception as e:
        return f"Database Error: {str(e)}", 500
    

@app.route('/book')
def render_booking_page():
    db = dbl.get_db_connection()
    # FIXED: Removed (dictionary=True) 
    cursor = db.cursor()
    
    # Grab the equipment so the user can select what they want to book
    cursor.execute("SELECT equipment_id, name, status FROM equipment")
    equipment_list = cursor.fetchall()
    
    cursor.close()
    db.close()
    
    return render_template('book.html', equipment=equipment_list)

@app.route('/book/submit', methods=['POST'])
def submit_booking():
    # 1. Grab the data from your HTML form
    equipment_id = request.form['equipment_id']
    start_time = request.form['start_time']
    end_time = request.form['end_time']
    
    # 2. Hardcode a user_id for testing (until you set up Flask sessions)
    user_id = 1 

    # 3. Pass it all to your business logic file!
    result = reservations.create_reservation(user_id, equipment_id, start_time, end_time)

    # 4. Handle the result
    if result['status'] == 'success':
        # Send them back to the dashboard if it worked
        return redirect(url_for('dashboard'))
    else:
        # If they got waitlisted or caused an error, show them the message
        return result['message']

if __name__ == '__main__':
    app.run(debug=True)