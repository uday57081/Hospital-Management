"""
Migration script to add staff table and enhance existing tables for HMS enhancements.
Run this once to update the database schema.
"""
import sqlite3
from datetime import datetime

DATABASE_NAME = 'hms.db'

def run_migration():
    """Add new tables and columns for HMS enhancements."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    
    print("Starting HMS Enhancement Migration...")
    
    # 1. Create Staff table
    print("Creating staff table...")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS staff (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            role TEXT NOT NULL,
            department TEXT,
            phone TEXT,
            email TEXT,
            shift TEXT DEFAULT 'morning',
            schedule TEXT,
            photo_url TEXT,
            status TEXT DEFAULT 'active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 2. Add status column to patients table if not exists
    print("Checking patients table for status column...")
    try:
        cursor.execute('ALTER TABLE patients ADD COLUMN status TEXT DEFAULT "active"')
        print("  Added status column to patients table")
    except sqlite3.OperationalError:
        print("  Status column already exists in patients table")
    
    # 3. Add batch_number and category to medicines table if not exists
    print("Checking medicines table for new columns...")
    try:
        cursor.execute('ALTER TABLE medicines ADD COLUMN batch_number TEXT')
        print("  Added batch_number column to medicines table")
    except sqlite3.OperationalError:
        print("  batch_number column already exists")
    
    try:
        cursor.execute('ALTER TABLE medicines ADD COLUMN category TEXT DEFAULT "General"')
        print("  Added category column to medicines table")
    except sqlite3.OperationalError:
        print("  category column already exists")
    
    # 4. Add report_file column to patient_tests table if not exists
    print("Checking patient_tests table for report_file column...")
    try:
        cursor.execute('ALTER TABLE patient_tests ADD COLUMN report_file TEXT')
        print("  Added report_file column to patient_tests table")
    except sqlite3.OperationalError:
        print("  report_file column already exists")
    
    # 5. Add more lab tests
    print("Adding additional lab tests...")
    additional_tests = [
        ('CT Scan', 'Computed Tomography imaging', 200.00),
        ('MRI', 'Magnetic Resonance Imaging', 350.00),
        ('COVID-19 RT-PCR', 'COVID-19 detection test', 75.00),
        ('Urine Analysis', 'Complete urine examination', 20.00),
        ('Thyroid Profile', 'T3, T4, TSH test', 45.00),
        ('Liver Function Test', 'LFT panel', 40.00),
        ('Kidney Function Test', 'KFT panel', 40.00)
    ]
    for test in additional_tests:
        try:
            cursor.execute('INSERT OR IGNORE INTO lab_tests (test_name, description, price) VALUES (?, ?, ?)', test)
        except:
            pass
    
    # 6. Insert sample staff members
    print("Adding sample staff members...")
    sample_staff = [
        ('Sarah Johnson', 'Nurse', 'Emergency', '555-0101', 'sarah.j@hospital.com', 'morning', 'Mon-Fri', None, 'active'),
        ('Michael Chen', 'Lab Technician', 'Laboratory', '555-0102', 'michael.c@hospital.com', 'evening', 'Mon-Sat', None, 'active'),
        ('Emily Rodriguez', 'Pharmacist', 'Pharmacy', '555-0103', 'emily.r@hospital.com', 'morning', 'Mon-Fri', None, 'active'),
        ('James Wilson', 'Receptionist', 'Front Desk', '555-0104', 'james.w@hospital.com', 'morning', 'Mon-Fri', None, 'active'),
        ('Lisa Thompson', 'Nurse', 'Cardiology', '555-0105', 'lisa.t@hospital.com', 'night', 'Tue-Sat', None, 'active')
    ]
    for staff in sample_staff:
        try:
            cursor.execute('''
                INSERT OR IGNORE INTO staff (full_name, role, department, phone, email, shift, schedule, photo_url, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', staff)
        except:
            pass
    
    conn.commit()
    conn.close()
    
    print("\nMigration completed successfully!")
    print("New features available:")
    print("  - Staff management module")
    print("  - Enhanced patient status tracking")
    print("  - Pharmacy categories and batch tracking")
    print("  - Lab report file uploads")
    print("  - Additional lab test types")

if __name__ == '__main__':
    run_migration()
