import sqlite3
from datetime import datetime

DATABASE_NAME = 'hms.db'

def get_db_connection():
    """Create and return a database connection."""
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def add_new_columns():
    """Add new columns to existing tables for Phase 1-11 enhancements."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    print("Adding new columns to database...")
    
    # Phase 1: Patient Management - Add status and photo columns
    try:
        cursor.execute("ALTER TABLE patients ADD COLUMN status TEXT DEFAULT 'outpatient'")
        print("✓ Added 'status' column to patients table")
    except sqlite3.OperationalError:
        print("- 'status' column already exists in patients table")
    
    try:
        cursor.execute("ALTER TABLE patients ADD COLUMN photo TEXT")
        print("✓ Added 'photo' column to patients table")
    except sqlite3.OperationalError:
        print("- 'photo' column already exists in patients table")
    
    # Phase 2: Billing - Add tax and subtotal columns
    try:
        cursor.execute("ALTER TABLE bills ADD COLUMN tax_amount REAL DEFAULT 0")
        print("✓ Added 'tax_amount' column to bills table")
    except sqlite3.OperationalError:
        print("- 'tax_amount' column already exists in bills table")
    
    try:
        cursor.execute("ALTER TABLE bills ADD COLUMN subtotal REAL DEFAULT 0")
        print("✓ Added 'subtotal' column to bills table")
    except sqlite3.OperationalError:
        print("- 'subtotal' column already exists in bills table")
    
    # Phase 3: Pharmacy - Add batch_number and category columns
    try:
        cursor.execute("ALTER TABLE medicines ADD COLUMN batch_number TEXT")
        print("✓ Added 'batch_number' column to medicines table")
    except sqlite3.OperationalError:
        print("- 'batch_number' column already exists in medicines table")
    
    try:
        cursor.execute("ALTER TABLE medicines ADD COLUMN category TEXT DEFAULT 'General'")
        print("✓ Added 'category' column to medicines table")
    except sqlite3.OperationalError:
        print("- 'category' column already exists in medicines table")
    
    # Phase 4: Laboratory - Add report_file column
    try:
        cursor.execute("ALTER TABLE patient_tests ADD COLUMN report_file TEXT")
        print("✓ Added 'report_file' column to patient_tests table")
    except sqlite3.OperationalError:
        print("- 'report_file' column already exists in patient_tests table")
    
    conn.commit()
    
    # Create new tables for additional features
    print("\nCreating new tables...")
    
    # Phase 2: Bill Items table for itemized billing
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bill_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bill_id INTEGER NOT NULL,
            description TEXT NOT NULL,
            quantity INTEGER DEFAULT 1,
            unit_price REAL NOT NULL,
            total_price REAL NOT NULL,
            FOREIGN KEY (bill_id) REFERENCES bills (id) ON DELETE CASCADE
        )
    ''')
    print("✓ Created 'bill_items' table")
    
    # Phase 3: Stock Movements table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stock_movements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            medicine_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            movement_type TEXT NOT NULL,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (medicine_id) REFERENCES medicines (id)
        )
    ''')
    print("✓ Created 'stock_movements' table")
    
    # Phase 5: Staff table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS staff (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            role TEXT NOT NULL,
            department_id INTEGER,
            photo TEXT,
            phone TEXT,
            email TEXT,
            shift TEXT DEFAULT 'morning',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (department_id) REFERENCES departments (id)
        )
    ''')
    print("✓ Created 'staff' table")
    
    # Phase 5: Attendance table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            staff_id INTEGER NOT NULL,
            date DATE NOT NULL,
            status TEXT NOT NULL,
            notes TEXT,
            FOREIGN KEY (staff_id) REFERENCES staff (id),
            UNIQUE(staff_id, date)
        )
    ''')
    print("✓ Created 'attendance' table")
    
    # Phase 6: Notifications table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            type TEXT NOT NULL,
            message TEXT NOT NULL,
            is_read INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    print("✓ Created 'notifications' table")

    # Phase 7: Bed Management
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS wards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            type TEXT NOT NULL,
            capacity INTEGER NOT NULL
        )
    ''')
    print("✓ Created 'wards' table")

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS beds (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bed_number TEXT NOT NULL,
            ward_id INTEGER NOT NULL,
            is_occupied BOOLEAN DEFAULT 0,
            patient_id INTEGER,
            FOREIGN KEY (ward_id) REFERENCES wards (id),
            FOREIGN KEY (patient_id) REFERENCES patients (id)
        )
    ''')
    print("✓ Created 'beds' table")
    
    # Phase 10: Settings table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key TEXT UNIQUE NOT NULL,
            value TEXT NOT NULL,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    print("✓ Created 'settings' table")
    
    # Insert default settings
    cursor.execute("INSERT OR IGNORE INTO settings (key, value) VALUES ('tax_rate', '10')")
    cursor.execute("INSERT OR IGNORE INTO settings (key, value) VALUES ('low_stock_threshold', '10')")
    cursor.execute("INSERT OR IGNORE INTO settings (key, value) VALUES ('expiry_alert_days', '30')")
    cursor.execute("INSERT OR IGNORE INTO settings (key, value) VALUES ('session_timeout_minutes', '15')")
    print("✓ Inserted default settings")
    
    # Add more comprehensive lab tests
    additional_lab_tests = [
        ('CT Scan', 'Computed Tomography scan', 200.00),
        ('MRI Scan', 'Magnetic Resonance Imaging', 350.00),
        ('COVID-19 RT-PCR', 'COVID-19 test', 50.00),
        ('Urine Analysis', 'Complete urine test', 20.00),
        ('ECG', 'Electrocardiogram', 40.00),
        ('Ultrasound', 'Ultrasound imaging', 80.00)
    ]
    cursor.executemany('INSERT OR IGNORE INTO lab_tests (test_name, description, price) VALUES (?, ?, ?)', additional_lab_tests)
    print("✓ Added additional lab test types")
    
    conn.commit()
    conn.close()
    print("\n✅ Database schema updated successfully!")

if __name__ == '__main__':
    add_new_columns()
