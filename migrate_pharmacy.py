"""
Database Migration Script - Pharmacy Enhancements
Adds batch_number and category columns to medicines table
"""

import sqlite3
from datetime import datetime

def migrate_medicines_table():
    conn = sqlite3.connect('hms.db')
    cursor = conn.cursor()
    
    try:
        print("Starting medicines table migration...")
        
        # Check if columns already exist
        cursor.execute("PRAGMA table_info(medicines)")
        columns = [column[1] for column in cursor.fetchall()]
        
        # Add batch_number column if it doesn't exist
        if 'batch_number' not in columns:
            cursor.execute("""
                ALTER TABLE medicines 
                ADD COLUMN batch_number TEXT
            """)
            print("✓ Added 'batch_number' column to medicines table")
        else:
            print("⚠ 'batch_number' column already exists")
        
        # Add category column if it doesn't exist
        if 'category' not in columns:
            cursor.execute("""
                ALTER TABLE medicines 
                ADD COLUMN category TEXT DEFAULT 'General'
            """)
            print("✓ Added 'category' column to medicines table")
        else:
            print("⚠ 'category' column already exists")
        
        conn.commit()
        print(f"\n✅ Migration completed successfully at {datetime.now()}")
        
    except sqlite3.Error as e:
        print(f"❌ Error during migration: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    migrate_medicines_table()
