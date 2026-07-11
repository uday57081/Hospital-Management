import sqlite3

def migrate():
    conn = sqlite3.connect('hms.db')
    cursor = conn.cursor()
    try:
        cursor.execute('ALTER TABLE patients ADD COLUMN status TEXT DEFAULT "Outpatient"')
        conn.commit()
        print("Successfully added status column to patients table.")
    except sqlite3.OperationalError as e:
        print(f"Column might already exist: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    migrate()
