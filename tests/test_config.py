
"""
===========================================
File: test_config.py
Author: Erisa Halipaj
Date: 19/01/2025
===========================================
"""
import pytest
from app import app
from database import get_db_connection

@pytest.fixture
def client():
    """Flask test client fixture."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture(scope="function", autouse=True)
def clean_database():
    """
    Clean up the database before and after each test.
    Ensures no leftover data affects subsequent tests.
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("TRUNCATE TABLE users RESTART IDENTITY CASCADE;")  
            conn.commit()
    finally:
        conn.close()
    
    yield  # Ensures the test runs after cleanup
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("TRUNCATE TABLE users RESTART IDENTITY CASCADE;")  
            conn.commit()
    finally:
        conn.close()
