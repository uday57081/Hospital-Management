"""
Password Migration Script
This script migrates all existing plain-text passwords to hashed passwords using werkzeug.
Run this ONCE after implementing password hashing.
"""

import sqlite3
from werkzeug.security import generate_password_hash

DATABASE_NAME = 'hms.db'

def migrate_passwords():
    """Hash all existing plain-text passwords."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    
    # Get all users
    users = cursor.execute('SELECT id, username, password FROM users').fetchall()
    
    print(f"Found {len(users)} users to migrate...")
    
    for user in users:
        user_id, username, plain_password = user
        
        # Check if password is already hashed (starts with hash method identifier)
        if plain_password.startswith(('pbkdf2:', 'scrypt:', 'bcrypt')):
            print(f"  ✓ {username}: Already hashed, skipping")
            continue
        
        # Hash the password
        hashed_password = generate_password_hash(plain_password)
        
        # Update the database
        cursor.execute('UPDATE users SET password = ? WHERE id = ?', (hashed_password, user_id))
        print(f"  ✓ {username}: Migrated from '{plain_password}' to hashed password")
    
    conn.commit()
    conn.close()
    
    print("\n✅ Password migration completed!")
    print("⚠️  Users can still log in with their original passwords.")
    print("   The system now stores them securely as hashes.")

if __name__ == '__main__':
    print("=" * 60)
    print("PASSWORD MIGRATION SCRIPT")
    print("=" * 60)
    print()
    
    response = input("This will hash all passwords in the database. Continue? (yes/no): ")
    
    if response.lower() == 'yes':
        migrate_passwords()
    else:
        print("Migration cancelled.")
