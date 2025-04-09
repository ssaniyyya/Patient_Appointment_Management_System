import sqlite3

# Connect to SQLite database (this will create the database file if it doesn't exist)
conn = sqlite3.connect('patient_management.db')
cursor = conn.cursor()

# Create the 'patients' table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        age INTEGER,
        gender TEXT,
        phone_number TEXT NOT NULL
    );
''')

# Create the 'appointments' table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS appointments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        appointment_date TEXT NOT NULL,
        appointment_time TEXT NOT NULL,
        doctor_name TEXT NOT NULL,
        FOREIGN KEY (patient_id) REFERENCES patients(id)
    );
''')

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Database and tables created successfully!")

