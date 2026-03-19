from flask import Flask, render_template, redirect, url_for, request, session
import MySQLdb
import MySQLdb.cursors
from datetime import timedelta

import database as dbl
from dotenv import load_dotenv
from pwsecurity import HashPassword, CheckHash
import os

# Load environment variables from .env in the project root
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '../.env'))

app = Flask(__name__, 
            template_folder='../frontend/templates', 
            static_folder='../frontend/static')

app.secret_key = os.getenv("FLASK_SECRET_KEY")
app.permanent_session_lifetime = timedelta(hours=6)

@app.route('/')
def login():
    if "user_id" not in session:
        return render_template('login.html', user_logged_in=False)
    else:
        return redirect(url_for('dashboard'))

@app.route('/login/submit', methods=["POST"])
def submit_login():
    db = dbl.get_db_connection()
    cursor = db.cursor()

    # Get login details
    email = request.form["email"]
    password_pt = request.form["password"]
    stay_logged_in = request.form.get("stay_logged_in") is not None

    # Check for account in database
    cursor.execute(
        """
        SELECT * FROM users 
            WHERE email = %s;
        """,
        (email,)
    )
    tableRow = cursor.fetchone()
    
    if tableRow is None:
        cursor.close()
        db.close()
        return render_template('login.html', user_logged_in=False, bad_login=True)
    
    else:
        cursor.close()
        db.close()

        # Check password matches
        dbPasswordHash = tableRow["password_hash"]
        if CheckHash(password_pt, dbPasswordHash.encode('utf-8')):
            # Successful login
            session.permanent = stay_logged_in
            session["user_id"] = tableRow["user_id"]
            session["user_name"] = tableRow["name"]
            session["user_email"] = tableRow["email"]
            session["user_role"] = tableRow["role"]

            return redirect(url_for('dashboard'))
        
        else:
            return render_template('login.html', user_logged_in=False, bad_login=True)

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
    if "user_id" not in session:
        return redirect(url_for('login'))

    try:
        # Create a new database connection for this request
        db = dbl.get_db_connection()
        cursor = db.cursor()
        
        cursor.execute("SELECT * FROM equipment")
        equipment_list = cursor.fetchall()
        
        cursor.close()
        db.close()
        
        return render_template('equipment.html', equipment=equipment_list, user_logged_in=True)
    except Exception as e:
        return f"Database Error: {str(e)}", 500
    

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)