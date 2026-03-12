from flask import Flask, render_template
import os

app = Flask(__name__, 
            template_folder='../frontend/templates', 
            static_folder='../frontend/static')

EQUIPMENT_DATA = [
    {'id': 1, 'name': 'Centrifuge', 'status': 'available'},
    {'id': 2, 'name': 'Mass Spectrometer', 'status': 'repair'},
    {'id': 3, 'name': 'PCR Machine', 'status': 'available'},
    {'id': 4, 'name': 'Scanning Electron Microscope', 'status': 'available'}
]

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', equipment=EQUIPMENT_DATA)

@app.route('/register')
def register():
    return "<h1>Registration Page Coming Soon</h1>"

if __name__ == '__main__':
    app.run(debug=True)