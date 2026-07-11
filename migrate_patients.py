"""
Database Migration Script - Patient Management Enhancements
Adds status, photo_url, and qr_code columns to patients table
"""

import sqlite3
from datetime import datetime

def migrate_patients_table():
    conn = sqlite3.connect('hms.db')
    cursor = conn.cursor()
    
    try:
        print("Starting patient table migration...")
        
        # Check if columns already exist
        cursor.execute("PRAGMA table_info(patients)")
        columns = [column[1] for column in cursor.fetchall()]
        
        # Add status column if it doesn't exist
        if 'status' not in columns:
            cursor.execute("""
                ALTER TABLE patients 
                ADD COLUMN status TEXT DEFAULT 'outpatient'
            """)
            print("✓ Added 'status' column to patients table")
        else:
            print("⚠ 'status' column already exists")
        
        # Add photo_url column if it doesn't exist
        if 'photo_url' not in columns:
            cursor.execute("""
                ALTER TABLE patients 
                ADD COLUMN photo_url TEXT
            """)
            print("✓ Added 'photo_url' column to patients table")
        else:
            print("⚠ 'photo_url' column already exists")
        
        # Add qr_code column if it doesn't exist
        if 'qr_code' not in columns:
            cursor.execute("""
                ALTER TABLE patients 
                ADD COLUMN qr_code TEXT
            """)
            print("✓ Added 'qr_code' column to patients table")
        else:
            print("⚠ 'qr_code' column already exists")
        
        conn.commit()
        print(f"\n✅ Migration completed successfully at {datetime.now()}")
        
    except sqlite3.Error as e:
        print(f"❌ Error during migration: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    # Create backup first
    import shutil
    try:
        shutil.copy2('hms.db', f'hms_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.db')
        print("✓ Database backup created\n")
    except Exception as e:
        print(f"Warning: Could not create backup: {e}\n")
    
    migrate_patients_table()
