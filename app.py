import os
import yaml
import logging
from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from database import initialize_db, get_db_connection
from flask_cors import CORS

# Configure logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

# Load configuration from YAML file
with open("appconfig.yaml", 'r') as file:
    config = yaml.safe_load(file)

# Create the Flask app
app = Flask(__name__)
CORS(app)

# Initialize the database (check if it exists and create tables if not)
initialize_db()

# Health check route
@app.route('/')
def health_check():
    logging.info("Health check route accessed.")
    return "OK"

# Register route for user registration
@app.route('/api/auth/register', methods=['POST'])
def register():
    logging.info("Register route accessed.")
    data = request.json
    username = data.get('username')
    password = data.get('password')
    password_confirm = data.get('password_confirm')

    logging.debug(f"Received data: username={username}")

    # Validate input
    if not username or not password or not password_confirm:
        logging.error("Username and passwords are required!")
        return jsonify({'message': 'Username and passwords are required!'}), 400

    if password != password_confirm:
        logging.error("Passwords do not match!")
        return jsonify({'message': 'Passwords do not match!'}), 400

    hashed_password = generate_password_hash(password)

    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO users (username, password) VALUES (%s, %s) RETURNING id;", (username, hashed_password))
                user_id = cur.fetchone()[0]
                conn.commit()
                logging.info(f"User {username} registered with ID {user_id}")
                return jsonify({'message': 'User registered successfully', 'user_id': user_id}), 201
    except Exception as e:
        logging.error(f"Error during registration: {e}")
        return jsonify({'message': 'An error occurred while registering the user', 'error': str(e)}), 500

# Login route for user authentication
@app.route('/api/auth/login', methods=['POST'])
def login():
    logging.info("Login route accessed.")
    data = request.json
    username = data.get('username')
    password = data.get('password')

    logging.debug(f"Received login request for username: {username}")

    if not username or not password:
        logging.error("Username and password are required!")
        return jsonify({'message': 'Username and password are required!'}), 400

    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, password FROM users WHERE username = %s;", (username,))
                user = cur.fetchone()

                if user and check_password_hash(user[1], password):
                    logging.info(f"User {username} authenticated successfully.")
                    return jsonify({'message': 'Authenticated successfully', 'user_id': user[0]}), 200
                else:
                    logging.warning(f"Failed login attempt for username: {username}")
                    return jsonify({'message': 'Invalid username or password'}), 401
    except Exception as e:
        logging.error(f"Error during login: {e}")
        return jsonify({'message': 'An error occurred during login', 'error': str(e)}), 500

# Change user credentials (username/password)
@app.route('/api/auth/change', methods=['POST'])
def change_credentials():
    logging.info("Change credentials route accessed.")
    data = request.json
    user_id = data.get('user_id')
    new_username = data.get('new_username')
    new_password = data.get('new_password')
    new_password_confirm = data.get('new_password_confirm')

    logging.debug(f"Received change request for user_id: {user_id}")

    if not new_username or not new_password or not new_password_confirm:
        logging.error("New username and passwords are required!")
        return jsonify({'message': 'New username and passwords are required!'}), 400

    if new_password != new_password_confirm:
        logging.error("New passwords do not match!")
        return jsonify({'message': 'New passwords do not match!'}), 400

    hashed_password = generate_password_hash(new_password)

    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("UPDATE users SET username = %s, password = %s WHERE id = %s;", (new_username, hashed_password, user_id))
                conn.commit()
                logging.info(f"User {user_id} credentials updated.")
                return jsonify({'message': 'User credentials updated successfully'}), 200
    except Exception as e:
        logging.error(f"Error while updating credentials: {e}")
        return jsonify({'message': 'An error occurred while updating credentials', 'error': str(e)}), 500

# Delete user account
@app.route('/api/auth/delete', methods=['DELETE'])
def delete_account():
    logging.info("Delete account route accessed.")
    data = request.json
    user_id = data.get('user_id')

    logging.debug(f"Received delete request for user_id: {user_id}")

    if not user_id:
        logging.error("User ID is required!")
        return jsonify({'message': 'User ID is required!'}), 400

    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM users WHERE id = %s;", (user_id,))
                conn.commit()
                logging.info(f"User account with ID {user_id} deleted.")
                return jsonify({'message': 'User account deleted successfully'}), 200
    except Exception as e:
        logging.error(f"Error while deleting account: {e}")
        return jsonify({'message': 'An error occurred while deleting the account', 'error': str(e)}), 500

# Start the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(config['server']['port']), debug=True)
