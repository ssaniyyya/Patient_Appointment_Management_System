from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Function to connect to the SQLite database
def connect_db():
    return sqlite3.connect('patient_management.db')

# Home route to display patients and appointments
@app.route('/')
def index():
    conn = connect_db()
    cursor = conn.cursor()

    # Fetch all patients
    cursor.execute("SELECT * FROM patients")
    patients = cursor.fetchall()

    # Fetch all appointments
    cursor.execute("SELECT * FROM appointments")
    appointments = cursor.fetchall()
    conn.close()

    return render_template('index.html', patients=patients, appointments=appointments)

# Route to add a new patient
@app.route('/add_patient', methods=['POST'])
def add_patient():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    age = request.form['age']
    gender = request.form['gender']
    phone_number = request.form['phone_number']
    
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO patients (first_name, last_name, age, gender, phone_number)
                     VALUES (?, ?, ?, ?, ?)''',
                   (first_name, last_name, age, gender, phone_number))
    conn.commit()
    conn.close()
    
    return redirect(url_for('index'))

# Route to schedule a new appointment
@app.route('/schedule_appointment', methods=['POST'])
def schedule_appointment():
    patient_id = request.form['patient_id']
    appointment_date = request.form['appointment_date']
    appointment_time = request.form['appointment_time']
    doctor_name = request.form['doctor_name']
    
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO appointments (patient_id, appointment_date, appointment_time, doctor_name)
                     VALUES (?, ?, ?, ?)''',
                   (patient_id, appointment_date, appointment_time, doctor_name))
    conn.commit()
    conn.close()
    
    return redirect(url_for('index'))

# Route to delete a patient
@app.route('/delete_patient/<int:patient_id>', methods=['POST'])
def delete_patient(patient_id):
    conn = connect_db()
    cursor = conn.cursor()
    
    # Delete any appointments associated with this patient first (to avoid foreign key constraints)
    cursor.execute('DELETE FROM appointments WHERE patient_id = ?', (patient_id,))
    
    # Delete the patient
    cursor.execute('DELETE FROM patients WHERE id = ?', (patient_id,))
    
    conn.commit()
    conn.close()
    
    return redirect(url_for('index'))

# Route to delete an appointment
@app.route('/delete_appointment/<int:appointment_id>', methods=['POST'])
def delete_appointment(appointment_id):
    conn = connect_db()
    cursor = conn.cursor()
    
    # Delete the appointment
    cursor.execute('DELETE FROM appointments WHERE id = ?', (appointment_id,))
    
    conn.commit()
    conn.close()
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

