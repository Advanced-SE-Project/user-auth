from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2  # Make sure to install this package

# Create a Blueprint for authentication
auth_bp = Blueprint('auth', __name__)

# Database connection parameters
DATABASE_URL = ""

def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

@auth_bp.route('/api/auth/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    password_confirm = data.get('password_confirm')

    # Validate input
    if not username or not password or not password_confirm:
        return jsonify({'message': 'Username and passwords are required!'}), 400

    if password != password_confirm:
        return jsonify({'message': 'Passwords do not match!'}), 400

    hashed_password = generate_password_hash(password)

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s) RETURNING id;", (username, hashed_password))
        user_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'message': 'User registered successfully', 'user_id': user_id}), 201
    except Exception as e:
        return jsonify({'message': 'An error occurred while registering the user', 'error': str(e)}), 500

@auth_bp.route('/api/auth/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password are required!'}), 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, password FROM users WHERE username = %s;", (username,))
        user = cur.fetchone()

        if user and check_password_hash(user[1], password):
            return jsonify({'message': 'Authenticated successfully', 'user_id': user[0]}), 200
        else:
            return jsonify({'message': 'Invalid username or password'}), 401
    except Exception as e:
        return jsonify({'message': 'An error occurred during login', 'error': str(e)}), 500

@auth_bp.route('/api/auth/change', methods=['POST'])
def change_credentials():
    data = request.json
    user_id = data.get('user_id')
    new_username = data.get('new_username')
    new_password = data.get('new_password')
    new_password_confirm = data.get('new_password_confirm')

    if not new_username or not new_password or not new_password_confirm:
        return jsonify({'message': 'New username and passwords are required!'}), 400

    if new_password != new_password_confirm:
        return jsonify({'message': 'New passwords do not match!'}), 400

    hashed_password = generate_password_hash(new_password)

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("UPDATE users SET username = %s, password = %s WHERE id = %s;", (new_username, hashed_password, user_id))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'message': 'User credentials updated successfully'}), 200
    except Exception as e:
        return jsonify({'message': 'An error occurred while updating credentials', 'error': str(e)}), 500

@auth_bp.route('/api/auth/delete', methods=['DELETE'])
def delete_account():
    data = request.json
    user_id = data.get('user_id')

    if not user_id:
        return jsonify({'message': 'User ID is required!'}), 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM users WHERE id = %s;", (user_id,))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'message': 'User account deleted successfully'}), 200
    except Exception as e: #activating pipeline
        return jsonify({'message': 'An error occurred while deleting the account', 'error': str(e)}), 500
