from flask import Flask, render_template, redirect, url_for, request
import MySQLdb
import MySQLdb.cursors

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

    # Insert into sql database (currently only students)
    cursor.execute(
        f"""
        INSERT INTO users (name, email, password_hash, role)
        VALUES ('{name}', '{email}', '{password_hash}', '{role}');
        """
    )

    db.commit()
    cursor.close()
    db.close()

    return redirect(url_for('login'))

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