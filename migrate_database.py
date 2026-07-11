"""
Database Schema Migration Script
Adds new columns to existing tables for enhanced functionality
"""

import sqlite3

DATABASE_NAME = 'hms.db'

def migrate_database():
    """Add new columns to existing tables."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    
    try:
        # Patient table enhancements
        print("Migrating patients table...")
        cursor.execute("ALTER TABLE patients ADD COLUMN photo_path TEXT")
        cursor.execute("ALTER TABLE patients ADD COLUMN status TEXT DEFAULT 'Outpatient'")
        cursor.execute("ALTER TABLE patients ADD COLUMN admission_date DATE")
        print("  ✓ Added photo_path, status, admission_date to patients")
        
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("  ⚠ Patients columns already exist, skipping...")
        else:
            raise
    
    try:
        # Medicine table enhancements
        print("Migrating medicines table...")
        cursor.execute("ALTER TABLE medicines ADD COLUMN batch_number TEXT")
        cursor.execute("ALTER TABLE medicines ADD COLUMN category TEXT")
        print("  ✓ Added batch_number, category to medicines")
        
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("  ⚠ Medicine columns already exist, skipping...")
        else:
            raise
    
    try:
        # Bills table enhancements
        print("Migrating bills table...")
        cursor.execute("ALTER TABLE bills ADD COLUMN tax_amount REAL DEFAULT 0")
        cursor.execute("ALTER TABLE bills ADD COLUMN discount REAL DEFAULT 0")
        cursor.execute("ALTER TABLE bills ADD COLUMN invoice_number TEXT UNIQUE")
        print("  ✓ Added tax_amount, discount, invoice_number to bills")
        
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("  ⚠ Bills columns already exist, skipping...")
        else:
            raise
    
    try:
        # Lab tests enhancements
        print("Migrating patient_tests table...")
        cursor.execute("ALTER TABLE patient_tests ADD COLUMN report_path TEXT")
        cursor.execute("ALTER TABLE patient_tests ADD COLUMN completed_at TIMESTAMP")
        print("  ✓ Added report_path, completed_at to patient_tests")
        
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("  ⚠ Patient_tests columns already exist, skipping...")
        else:
            raise
    
    # Create new tables
    print("Creating new tables...")
    
    # Stock transactions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stock_transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            medicine_id INTEGER NOT NULL,
            transaction_type TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (medicine_id) REFERENCES medicines (id)
        )
    ''')
    print("  ✓ Created stock_transactions table")
    
    # Staff schedules table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS staff_schedules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            shift TEXT NOT NULL,
            date DATE NOT NULL,
            status TEXT DEFAULT 'scheduled',
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    print("  ✓ Created staff_schedules table")
    
    # Notifications table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            message TEXT NOT NULL,
            type TEXT,
            is_read INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    print("  ✓ Created notifications table")
    
    conn.commit()
    conn.close()
    
    print("\n✅ Database migration completed successfully!")

if __name__ == '__main__':
    print("=" * 60)
    print("DATABASE SCHEMA MIGRATION")
    print("=" * 60)
    print()
    
    migrate_database()
