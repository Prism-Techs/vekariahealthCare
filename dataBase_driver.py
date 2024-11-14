# Example usage of the AuthUser database

from database import DatabaseConnection
from datetime import datetime

def test_auth_user_db():
    db = DatabaseConnection()
    db.connect()
    
    # Add a new user
    new_user = {
        'username': 'testdoctor',
        'password': 'doctoct',
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john.doe@example.com',
        'is_doctor': True,
        'is_operator': False,
        'is_admin': False,
        'date_joined': datetime.now(),
        'phone': 1234567890,
        'address': '123 Medical Street',
        'city': 1,
        'state': 1,
        'machine_access_list': {'machine1': True, 'machine2': False},
        'title': 'Dr.',
        'is_superuser': False,
        'is_staff': False
    }
    
    user_id = db.add_user(**new_user)
    print(f"Added user with ID: {user_id}")
    
    # Get user
    user = db.get_user('testdoctor')
    if user:
        print(f"Retrieved user: {user['first_name']} {user['last_name']}")
    
    # Update user
    db.update_user('testdoctor', phone=9876543210, is_sync=1)
    
    # Verify login
    logged_in_user = db.verify_login('testdoctor', 'hashed_password_here')
    if logged_in_user:
        print(f"Login successful for: {logged_in_user['username']}")
    
    db.disconnect()

if __name__ == "__main__":
    test_auth_user_db()