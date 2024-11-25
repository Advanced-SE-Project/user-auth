import psycopg2
import os

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:12345678@localhost:5432/budget_db')

def get_connection_to_postgres():
    """Connect to the default PostgreSQL database to manage other databases."""
    try:
        # Default connection without specifying a database
        return psycopg2.connect(
            host="localhost",
            port=5432,
            user="postgres",
            password="12345678",
            dbname="postgres"  # Default admin database
        )
    except Exception as e:
        print(f"Error connecting to PostgreSQL: {e}")
        raise

def create_database_if_not_exists():
    """Check if the database exists and create it if not."""
    try:
        conn = get_connection_to_postgres()
        conn.autocommit = True  # Required for creating databases
        with conn.cursor() as cur:
            # Check if the database exists
            cur.execute("SELECT 1 FROM pg_database WHERE datname = 'budget_db';")
            exists = cur.fetchone()
            
            if not exists:
                # Create the database if it does not exist
                cur.execute("CREATE DATABASE budget_db;")
                print("Database 'budget_db' created successfully.")
            else:
                print("Database 'budget_db' already exists.")
        conn.close()
    except Exception as e:
        print(f"Error checking or creating the database: {e}")
        raise

def get_db_connection():
    """Use a context manager to handle database connections."""
    return psycopg2.connect(DATABASE_URL)

def initialize_db():
    """Initialize the database by ensuring it exists and applying schema."""
    try:
        # Step 1: Create the database if it doesn't exist
        create_database_if_not_exists()

        # Step 2: Connect to the budget_db and check for tables
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
                # If the table doesn't exist, create it using schema.sql
                with open('schema.sql', 'r') as f:
                    cur.execute(f.read())
                conn.commit()
                print("Database tables created successfully.")
            else:
                print("Database tables already initialized.")
        conn.close()
    except Exception as e:
        print(f"Error initializing the database: {e}")
        raise
