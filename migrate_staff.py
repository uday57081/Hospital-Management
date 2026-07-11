"""
Database Migration Script - Staff Management Module
Creates staff table for managing hospital staff members
"""

import sqlite3
from datetime import datetime

def create_staff_table():
    conn = sqlite3.connect('hms.db')
    cursor = conn.cursor()
    
    try:
        print("Creating staff table...")
        
        # Create staff table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS staff (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                role TEXT NOT NULL,
                department TEXT,
                shift TEXT,
                contact TEXT,
                photo_url TEXT,
                email TEXT,
                join_date TEXT,
                status TEXT DEFAULT 'active',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        print("✓ Staff table created successfully")
        
        # Check if table has any data
        cursor.execute("SELECT COUNT(*) FROM staff")
        count = cursor.fetchone()[0]
        
        if count == 0:
            print("\nAdding sample staff data...")
            sample_staff = [
                ('Dr. Sarah Johnson', 'Doctor', 'Cardiology', 'morning', '+1-555-0101', None, 'sarah.j@hospital.com', '2023-01-15', 'active'),
                ('John Smith', 'Nurse', 'Emergency', 'evening', '+1-555-0102', None, 'john.s@hospital.com', '2023-03-20', 'active'),
                ('Emily Davis', 'Lab Technician', 'Laboratory', 'morning', '+1-555-0103', None, 'emily.d@hospital.com', '2023-05-10', 'active'),
                ('Michael Brown', 'Pharmacist', 'Pharmacy', 'morning', '+1-555-0104', None, 'michael.b@hospital.com', '2023-02-01', 'active'),
                ('Lisa Anderson', 'Receptionist', 'Reception', 'morning', '+1-555-0105', None, 'lisa.a@hospital.com', '2023-06-15', 'active'),
            ]
            
            cursor.executemany("""
                INSERT INTO staff (full_name, role, department, shift, contact, photo_url, email, join_date, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, sample_staff)
            
            print(f"✓ Added {len(sample_staff)} sample staff members")
        
        conn.commit()
        print(f"\n✅ Staff table migration completed successfully at {datetime.now()}")
        
    except sqlite3.Error as e:
        print(f"❌ Error during migration: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    create_staff_table()
