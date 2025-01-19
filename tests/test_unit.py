import pytest
from database import get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

def test_database_connection():
    """Test if database connection works"""
    conn = None
    try:
        conn = get_db_connection()
        assert conn is not None  # Ensure we get a valid connection
    finally:
        if conn:
            conn.close()

def test_password_hashing():
    """Test password hashing and verification"""
    password = "securepassword"
    hashed_password = generate_password_hash(password)
    
    assert check_password_hash(hashed_password, password)  # Should return True
    assert not check_password_hash(hashed_password, "wrongpassword")  # Should return False

def test_generate_jwt_token():
    """Test JWT token generation"""
    payload = {"user_id": 1, "username": "testuser"}
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm="HS256")

    assert isinstance(token, str)  # Token should be a string

def test_decode_jwt_token():
    """Test JWT token decoding"""
    payload = {"user_id": 1, "username": "testuser"}
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm="HS256")
    
    decoded_payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
    
    assert decoded_payload["user_id"] == 1
    assert decoded_payload["username"] == "testuser"
