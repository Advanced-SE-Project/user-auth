"""

===========================================
File: database.py
Author: Erisa Halipaj
Description:Manages database connections and initializes the users table if it does not exist.
Date: 19/01/2025
===========================================

"""
import psycopg2
from dotenv import load_dotenv
import os
import logging


logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

# Load .env variables
load_dotenv()

# Get the database URL from .env
DATABASE_URL = os.getenv('DATABASE_URL')

def get_db_connection():
    """Connect to the specified PostgreSQL database."""
    try:
        return psycopg2.connect(DATABASE_URL)
    except Exception as e:
        logging.error(f"Database connection error: {e}")
        raise

def initialize_db():
    """Initialize the database by ensuring the 'users' table exists."""
    try:
        # Connect to the UserAuth database
        conn = get_db_connection()
        with conn.cursor() as cur:
            # Check if the 'users' table exists
            cur.execute("""
                SELECT EXISTS (
                    SELECT 1 FROM information_schema.tables
                    WHERE table_name = 'users'
                );
            """)
            table_exists = cur.fetchone()[0]

            if not table_exists:
                # Create the 'users' table using schema.sql
                with open('schema.sql', 'r') as f:
                    cur.execute(f.read())
                conn.commit()
                logging.info("Database tables created successfully.")
            else:
                logging.info("Database tables already exist.")
        conn.close()
    except Exception as e:
        logging.error(f"Error initializing the database: {e}")
        raise