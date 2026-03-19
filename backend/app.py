from flask import Flask, render_template, redirect, url_for, request
import MySQLdb
import MySQLdb.cursors

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

@app.route('/')
def login():
    return render_template('login.html', user_logged_in=False)

@app.route('/login/submit', methods=["POST"])
def submit_login():
    db = dbl.get_db_connection()
    cursor = db.cursor()

    # Get login details
    email = request.form["email"]
    password_pt = request.form["password"]

    # Check for account in database
    emailExists = cursor.execute(
        """
        SELECT * FROM users 
            WHERE email = %s;
        """,
        (email,)
    )

    if not emailExists:
        cursor.close()
        db.close()
        return render_template('login.html', user_logged_in=False, bad_login=True)
    
    else:
        tableRow = cursor.fetchone()
        cursor.close()
        db.close()

        # Check password matches
        dbPasswordHash = tableRow["password_hash"]
        if CheckHash(password_pt, dbPasswordHash.encode('utf-8')):
            # Successful login
            return redirect('/dashboard')
        
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

if __name__ == '__main__':
    app.run(debug=True)