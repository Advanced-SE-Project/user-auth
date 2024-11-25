import os
import yaml
import logging
from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from database import initialize_db, get_db_connection  # Import functions from database.py

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Load configuration from YAML file
with open("appconfig.yaml", 'r') as file:
    config = yaml.safe_load(file)

# Create the Flask app
app = Flask(__name__)

# Initialize the database (check if it exists and create tables if not)
initialize_db()

# Health check route
@app.route('/')
def health_check():
    app.logger.debug("Health check route accessed.")
    return "OK"

# Register route for user registration
@app.route('/api/auth/register', methods=['POST'])
def register():
    app.logger.debug("Register route accessed.")
    data = request.json
    username = data.get('username')
    password = data.get('password')
    password_confirm = data.get('password_confirm')

    app.logger.debug(f"Received data: username={username}, password={password}, password_confirm={password_confirm}")

    # Validate input
    if not username or not password or not password_confirm:
        app.logger.error("Username and passwords are required!")
        return jsonify({'message': 'Username and passwords are required!'}), 400

    if password != password_confirm:
        app.logger.error("Passwords do not match!")
        return jsonify({'message': 'Passwords do not match!'}), 400

    hashed_password = generate_password_hash(password)

    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO users (username, password) VALUES (%s, %s) RETURNING id;", (username, hashed_password))
                user_id = cur.fetchone()[0]
                conn.commit()
                app.logger.info(f"User {username} registered with ID {user_id}")
                return jsonify({'message': 'User registered successfully', 'user_id': user_id}), 201
    except Exception as e:
        app.logger.error(f"Error during registration: {e}")
        return jsonify({'message': 'An error occurred while registering the user', 'error': str(e)}), 500

# Login route for user authentication
@app.route('/api/auth/login', methods=['POST'])
def login():
    app.logger.debug("Login route accessed.")
    data = request.json
    username = data.get('username')
    password = data.get('password')

    app.logger.debug(f"Received data: username={username}, password={password}")

    if not username or not password:
        app.logger.error("Username and password are required!")
        return jsonify({'message': 'Username and password are required!'}), 400

    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, password FROM users WHERE username = %s;", (username,))
                user = cur.fetchone()

                if user and check_password_hash(user[1], password):
                    app.logger.info(f"User {username} authenticated successfully.")
                    return jsonify({'message': 'Authenticated successfully', 'user_id': user[0]}), 200
                else:
                    app.logger.error("Invalid username or password.")
                    return jsonify({'message': 'Invalid username or password'}), 401
    except Exception as e:
        app.logger.error(f"Error during login: {e}")
        return jsonify({'message': 'An error occurred during login', 'error': str(e)}), 500

# Change user credentials (username/password)
@app.route('/api/auth/change', methods=['POST'])
def change_credentials():
    app.logger.debug("Change credentials route accessed.")
    data = request.json
    user_id = data.get('user_id')
    new_username = data.get('new_username')
    new_password = data.get('new_password')
    new_password_confirm = data.get('new_password_confirm')

    app.logger.debug(f"Received data: user_id={user_id}, new_username={new_username}, new_password={new_password}, new_password_confirm={new_password_confirm}")

    if not new_username or not new_password or not new_password_confirm:
        app.logger.error("New username and passwords are required!")
        return jsonify({'message': 'New username and passwords are required!'}), 400

    if new_password != new_password_confirm:
        app.logger.error("New passwords do not match!")
        return jsonify({'message': 'New passwords do not match!'}), 400

    hashed_password = generate_password_hash(new_password)

    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("UPDATE users SET username = %s, password = %s WHERE id = %s;", (new_username, hashed_password, user_id))
                conn.commit()
                app.logger.info(f"User {user_id} credentials updated.")
                return jsonify({'message': 'User credentials updated successfully'}), 200
    except Exception as e:
        app.logger.error(f"Error while updating credentials: {e}")
        return jsonify({'message': 'An error occurred while updating credentials', 'error': str(e)}), 500

# Delete user account
@app.route('/api/auth/delete', methods=['DELETE'])
def delete_account():
    app.logger.debug("Delete account route accessed.")
    data = request.json
    user_id = data.get('user_id')

    app.logger.debug(f"Received data: user_id={user_id}")

    if not user_id:
        app.logger.error("User ID is required!")
        return jsonify({'message': 'User ID is required!'}), 400

    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM users WHERE id = %s;", (user_id,))
                conn.commit()
                app.logger.info(f"User account with ID {user_id} deleted.")
                return jsonify({'message': 'User account deleted successfully'}), 200
    except Exception as e:
        app.logger.error(f"Error while deleting account: {e}")
        return jsonify({'message': 'An error occurred while deleting the account', 'error': str(e)}), 500

# Start the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(config['server']['port']), debug=True)
