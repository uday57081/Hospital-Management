"""
Hospital Management System - Admin Password Reset Utility
This script resets the administrator login details to defaults.
"""
import os
import sys
import sqlite3

# Ensure we can import from the app package
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from app.auth.security import get_password_hash
except ImportError:
    # Fallback to a local definition if path is not resolved
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["pbkdf2_sha256", "bcrypt"], deprecated="auto")
    def get_password_hash(password):
        return pwd_context.hash(password)

DATABASE_NAME = 'hms.db'

def reset_admin():
    print("=" * 60)
    print("🏥 HMS ADMIN DETAILS RESET TOOL")
    print("=" * 60)
    
    if not os.path.exists(DATABASE_NAME):
        print(f"❌ Error: Database file '{DATABASE_NAME}' not found.")
        print("Please run this script from the project root directory containing the 'hms.db' file.")
        return

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    
    # Check if users table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
    if not cursor.fetchone():
        print("❌ Error: 'users' table does not exist. Please initialize the database schema first.")
        conn.close()
        return

    # Choose password
    print("Select a new admin password:")
    print("1) 'admin' (Recommended)")
    print("2) 'admin123' (Documentation Default)")
    print("3) Custom password")
    
    choice = input("Enter choice (1/2/3): ").strip()
    
    if choice == '1' or not choice:
        password = "admin"
    elif choice == '2':
        password = "admin123"
    elif choice == '3':
        password = input("Enter custom admin password: ").strip()
        if not password:
            print("Password cannot be empty. Defaulting to 'admin'.")
            password = "admin"
    else:
        password = "admin"

    hashed_password = get_password_hash(password)
    
    # Check if admin user exists
    user = cursor.execute("SELECT id, username FROM users WHERE username = 'admin'").fetchone()
    
    if user:
        # Update existing
        cursor.execute("UPDATE users SET password = ?, role = 'admin' WHERE username = 'admin'", (hashed_password,))
        print(f"\n✓ Updated password for existing 'admin' user to: '{password}'")
    else:
        # Insert new admin
        cursor.execute(
            "INSERT INTO users (username, password, role, full_name, email) VALUES (?, ?, ?, ?, ?)",
            ("admin", hashed_password, "admin", "System Administrator", "admin@hospital.com")
        )
        print(f"\n✓ Created new 'admin' user with username: 'admin' and password: '{password}'")
        
    conn.commit()
    conn.close()
    
    print("\n✅ Admin credentials successfully reset!")
    print("Start your server and log in using:")
    print(f"   - Username: admin")
    print(f"   - Password: {password}")
    print("=" * 60)

if __name__ == '__main__':
    reset_admin()
