# Test email service
import os
import sys

# Add backend directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.email_service import email_service

def test_email_service():
    """Test the email service in development mode"""
    
    print("Testing Email Service...")
    print("=" * 60)
    
    # Test verification email
    print("\n1. Testing Verification Email:")
    success = email_service.send_verification_email(
        to_email="test@example.com",
        verification_token="test-token-12345",
        user_name="Test User"
    )
    
    if success:
        print("[PASS] Verification email test passed!")
    else:
        print("[FAIL] Verification email test failed!")
    
    # Test password reset email
    print("\n2. Testing Password Reset Email:")
    success = email_service.send_password_reset_email(
        to_email="test@example.com",
        reset_token="reset-token-67890",
        user_name="Test User"
    )
    
    if success:
        print("[PASS] Password reset email test passed!")
    else:
        print("[FAIL] Password reset email test failed!")
    
    print("\n" + "=" * 60)
    print("Email Service Test Complete!")

if __name__ == "__main__":
    test_email_service()