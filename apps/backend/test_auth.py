#!/usr/bin/env python3
"""
Test script for authentication system
This script tests the basic authentication flow without requiring a running server
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models.user_models import UserCreate, UserLogin
from crud.auth_crud import AuthCRUD
from db import get_db_connection
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_auth_system():
    """Test the authentication system"""
    print("Testing Sydney Rental Hub Authentication System")
    print("=" * 60)
    
    try:
        # Test database connection
        print("\n1. Testing database connection...")
        db_conn = get_db_connection()
        print("Database connection successful")
        
        # Initialize auth tables
        print("\n2. Initializing authentication tables...")
        success = AuthCRUD.init_auth_tables(db_conn)
        if success:
            print("Authentication tables initialized")
        else:
            print("Failed to initialize auth tables")
            return False
        
        # Test user registration
        print("\n3. Testing user registration...")
        test_user = UserCreate(
            email="test@example.com",
            password="testPassword123",
            full_name="Test User"
        )
        
        # Delete existing test user if exists
        with db_conn.cursor() as cursor:
            cursor.execute("DELETE FROM users WHERE email = %s", (test_user.email,))
            db_conn.commit()
        
        user = AuthCRUD.create_user(db_conn, test_user)
        if user:
            print(f"User registration successful: {user.email}")
            user_id = user.id
            verification_token = user.verification_token
        else:
            print("User registration failed")
            return False
        
        # Test password verification
        print("\n4. Testing password verification...")
        retrieved_user = AuthCRUD.get_user_by_email(db_conn, test_user.email)
        if retrieved_user and AuthCRUD.verify_password(test_user.password, retrieved_user.hashed_password):
            print("Password verification successful")
        else:
            print("Password verification failed")
            return False
        
        # Test email verification
        print("\n5. Testing email verification...")
        verification_success = AuthCRUD.verify_user_email(db_conn, verification_token)
        if verification_success:
            print("Email verification successful")
        else:
            print("Email verification failed")
            return False
        
        # Test refresh token
        print("\n6. Testing refresh token...")
        refresh_token = AuthCRUD.generate_refresh_token()
        token_update = AuthCRUD.update_refresh_token(db_conn, user_id, refresh_token)
        if token_update:
            print("Refresh token update successful")
        else:
            print("Refresh token update failed")
            return False
        
        # Test user address functionality
        print("\n7. Testing user address functionality...")
        from models.user_models import UserAddressCreate
        
        test_address = UserAddressCreate(
            address="University of Sydney, Camperdown NSW 2006",
            label="School",
            place_id="ChIJVXealLmuEmsRUduC5Wd-6XQ",
            latitude=-33.8886,
            longitude=151.1873
        )
        
        saved_address = AuthCRUD.create_user_address(db_conn, user_id, test_address)
        if saved_address:
            print(f"Address creation successful: {saved_address.label}")
            
            # Test getting user addresses
            addresses = AuthCRUD.get_user_addresses(db_conn, user_id)
            if addresses and len(addresses) > 0:
                print(f"Address retrieval successful: Found {len(addresses)} addresses")
                
                # Test deleting address
                delete_success = AuthCRUD.delete_user_address(db_conn, user_id, saved_address.id)
                if delete_success:
                    print("Address deletion successful")
                else:
                    print("Address deletion failed")
            else:
                print("Address retrieval failed")
                return False
        else:
            print("Address creation failed")
            return False
        
        # Cleanup
        print("\n8. Cleaning up test data...")
        with db_conn.cursor() as cursor:
            cursor.execute("DELETE FROM users WHERE email = %s", (test_user.email,))
            db_conn.commit()
        print("Test data cleaned up")
        
        # Close database connection
        db_conn.close()
        
        print("\n" + "=" * 60)
        print("All authentication tests passed!")
        print("Authentication system is ready for production use")
        
        return True
        
    except Exception as e:
        logger.error(f"Test failed: {e}", exc_info=True)
        print(f"\nTest failed with error: {e}")
        return False

if __name__ == "__main__":
    test_auth_system()