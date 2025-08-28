# Authentication CRUD operations

import psycopg2
import psycopg2.extras
from passlib.context import CryptContext
import secrets
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from models.user_models import UserCreate, UserInDB, UserAddress, UserAddressCreate
import logging

logger = logging.getLogger(__name__)

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthCRUD:
    """Authentication and user management CRUD operations"""
    
    @staticmethod
    def init_auth_tables(db_conn) -> bool:
        """Initialize authentication tables if they don't exist"""
        try:
            with db_conn.cursor() as cursor:
                # Create users table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id SERIAL PRIMARY KEY,
                        email VARCHAR(255) UNIQUE NOT NULL,
                        full_name VARCHAR(100),
                        hashed_password VARCHAR(255) NOT NULL,
                        status VARCHAR(20) DEFAULT 'pending',
                        verification_token VARCHAR(255),
                        verification_token_expires TIMESTAMP,
                        refresh_token VARCHAR(255),
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """)
                
                # Create user_addresses table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS user_addresses (
                        id SERIAL PRIMARY KEY,
                        user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                        address VARCHAR(500) NOT NULL,
                        label VARCHAR(50) NOT NULL,
                        place_id VARCHAR(255),
                        latitude DECIMAL(10, 8) NOT NULL,
                        longitude DECIMAL(11, 8) NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """)
                
                # Create indexes
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_verification_token ON users(verification_token);")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_refresh_token ON users(refresh_token);")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_user_addresses_user_id ON user_addresses(user_id);")
                
                db_conn.commit()
                logger.info("Authentication tables initialized successfully")
                return True
        except Exception as e:
            logger.error(f"Error initializing auth tables: {e}")
            db_conn.rollback()
            return False
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password using bcrypt"""
        return pwd_context.hash(password)
    
    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        """Verify password against hash"""
        try:
            return pwd_context.verify(password, hashed_password)
        except Exception as e:
            logger.error(f"Password verification error: {e}")
            return False
    
    @staticmethod
    def generate_verification_token() -> str:
        """Generate a secure verification token"""
        return secrets.token_urlsafe(32)
    
    @staticmethod
    def generate_refresh_token() -> str:
        """Generate a secure refresh token"""
        return secrets.token_urlsafe(64)
    
    @staticmethod
    def create_user(db_conn, user_data: UserCreate) -> Optional[UserInDB]:
        """Create a new user"""
        try:
            with db_conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                # Check if user already exists
                cursor.execute("SELECT id FROM users WHERE email = %s", (user_data.email,))
                if cursor.fetchone():
                    logger.warning(f"User already exists: {user_data.email}")
                    return None
                
                # Hash password and generate verification token
                hashed_password = AuthCRUD.hash_password(user_data.password)
                verification_token = AuthCRUD.generate_verification_token()
                verification_expires = datetime.utcnow() + timedelta(hours=24)  # Token expires in 24 hours
                
                # Insert new user
                cursor.execute("""
                    INSERT INTO users (email, full_name, hashed_password, verification_token, verification_token_expires)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING *
                """, (user_data.email, user_data.full_name, hashed_password, verification_token, verification_expires))
                
                user_row = cursor.fetchone()
                db_conn.commit()
                
                if user_row:
                    logger.info(f"User created successfully: {user_data.email}")
                    return UserInDB(**dict(user_row))
                return None
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            db_conn.rollback()
            return None
    
    @staticmethod
    def get_user_by_email(db_conn, email: str) -> Optional[UserInDB]:
        """Get user by email"""
        try:
            with db_conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
                user_row = cursor.fetchone()
                return UserInDB(**dict(user_row)) if user_row else None
        except Exception as e:
            logger.error(f"Error getting user by email: {e}")
            return None
    
    @staticmethod
    def get_user_by_id(db_conn, user_id: int) -> Optional[UserInDB]:
        """Get user by ID"""
        try:
            with db_conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
                user_row = cursor.fetchone()
                return UserInDB(**dict(user_row)) if user_row else None
        except Exception as e:
            logger.error(f"Error getting user by ID: {e}")
            return None
    
    @staticmethod
    def verify_user_email(db_conn, verification_token: str) -> bool:
        """Verify user email using token"""
        try:
            with db_conn.cursor() as cursor:
                # Find user with valid token
                cursor.execute("""
                    SELECT id FROM users 
                    WHERE verification_token = %s 
                    AND verification_token_expires > %s
                    AND status = 'pending'
                """, (verification_token, datetime.utcnow()))
                
                user = cursor.fetchone()
                if not user:
                    logger.warning(f"Invalid or expired verification token: {verification_token}")
                    return False
                
                # Update user status
                cursor.execute("""
                    UPDATE users 
                    SET status = 'verified', 
                        verification_token = NULL, 
                        verification_token_expires = NULL,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id = %s
                """, (user[0],))
                
                db_conn.commit()
                logger.info(f"User email verified successfully: {user[0]}")
                return True
        except Exception as e:
            logger.error(f"Error verifying email: {e}")
            db_conn.rollback()
            return False
    
    @staticmethod
    def update_refresh_token(db_conn, user_id: int, refresh_token: str) -> bool:
        """Update user's refresh token"""
        try:
            with db_conn.cursor() as cursor:
                cursor.execute("""
                    UPDATE users 
                    SET refresh_token = %s, updated_at = CURRENT_TIMESTAMP
                    WHERE id = %s
                """, (refresh_token, user_id))
                
                db_conn.commit()
                return True
        except Exception as e:
            logger.error(f"Error updating refresh token: {e}")
            db_conn.rollback()
            return False
    
    @staticmethod
    def get_user_by_refresh_token(db_conn, refresh_token: str) -> Optional[UserInDB]:
        """Get user by refresh token"""
        try:
            with db_conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT * FROM users 
                    WHERE refresh_token = %s AND status = 'verified'
                """, (refresh_token,))
                user_row = cursor.fetchone()
                return UserInDB(**dict(user_row)) if user_row else None
        except Exception as e:
            logger.error(f"Error getting user by refresh token: {e}")
            return None
    
    @staticmethod
    def get_user_by_verification_token(db_conn, verification_token: str) -> Optional[UserInDB]:
        """Get user by verification token"""
        try:
            with db_conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT * FROM users 
                    WHERE verification_token = %s 
                    AND verification_token_expires > %s 
                    AND status = 'pending'
                """, (verification_token, datetime.utcnow()))
                user_row = cursor.fetchone()
                return UserInDB(**dict(user_row)) if user_row else None
        except Exception as e:
            logger.error(f"Error getting user by verification token: {e}")
            return None
    
    @staticmethod
    def resend_verification_email(db_conn, email: str) -> Optional[str]:
        """Regenerate and return new verification token"""
        try:
            with db_conn.cursor() as cursor:
                # Check if user exists and is still pending
                cursor.execute("""
                    SELECT id FROM users 
                    WHERE email = %s AND status = 'pending'
                """, (email,))
                
                user = cursor.fetchone()
                if not user:
                    logger.warning(f"User not found or already verified: {email}")
                    return None
                
                # Generate new token
                new_token = AuthCRUD.generate_verification_token()
                new_expires = datetime.utcnow() + timedelta(hours=24)
                
                cursor.execute("""
                    UPDATE users 
                    SET verification_token = %s, 
                        verification_token_expires = %s,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id = %s
                """, (new_token, new_expires, user[0]))
                
                db_conn.commit()
                logger.info(f"Verification email resent for user: {email}")
                return new_token
        except Exception as e:
            logger.error(f"Error resending verification email: {e}")
            db_conn.rollback()
            return None
    
    # User Address CRUD operations
    @staticmethod
    def create_user_address(db_conn, user_id: int, address_data: UserAddressCreate) -> Optional[UserAddress]:
        """Create a new user address"""
        try:
            with db_conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute("""
                    INSERT INTO user_addresses (user_id, address, label, place_id, latitude, longitude)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING *
                """, (user_id, address_data.address, address_data.label, 
                      address_data.place_id, address_data.latitude, address_data.longitude))
                
                address_row = cursor.fetchone()
                db_conn.commit()
                
                if address_row:
                    return UserAddress(**dict(address_row))
                return None
        except Exception as e:
            logger.error(f"Error creating user address: {e}")
            db_conn.rollback()
            return None
    
    @staticmethod
    def get_user_addresses(db_conn, user_id: int) -> List[UserAddress]:
        """Get all addresses for a user"""
        try:
            with db_conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT * FROM user_addresses 
                    WHERE user_id = %s 
                    ORDER BY created_at DESC
                """, (user_id,))
                
                address_rows = cursor.fetchall()
                return [UserAddress(**dict(row)) for row in address_rows]
        except Exception as e:
            logger.error(f"Error getting user addresses: {e}")
            return []
    
    @staticmethod
    def delete_user_address(db_conn, user_id: int, address_id: int) -> bool:
        """Delete a user address"""
        try:
            with db_conn.cursor() as cursor:
                cursor.execute("""
                    DELETE FROM user_addresses 
                    WHERE id = %s AND user_id = %s
                """, (address_id, user_id))
                
                deleted_count = cursor.rowcount
                db_conn.commit()
                
                if deleted_count > 0:
                    logger.info(f"Address deleted successfully: {address_id}")
                    return True
                return False
        except Exception as e:
            logger.error(f"Error deleting user address: {e}")
            db_conn.rollback()
            return False