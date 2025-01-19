User Authentication Microservice
================================

A microservice for managing user authentication, including registration, login, and account management. This service is built with Python, Flask, and PostgreSQL, utilizing JWT for authentication and CORS for secure cross-origin requests.

Table of Contents
-----------------

*   [Features](#features)
    
*   [Installation](#installation)
    
*   [Environment Variables](#environment-variables)
    
*   [Database Setup](#database-setup)
    
*   [Running the Microservice](#running-the-microservice)
    
*   [API Endpoints](#api-endpoints)
    
*   [Technologies Used](#technologies-used)
    

Features
--------

*   **User Registration:** Register a new user with secure password hashing and receive a JWT access token.
    
*   **User Login:** Authenticate a user and issue a JWT access token.
    
*   **Update Credentials:** Change username or password for an existing user.
    
*   **Account Deletion:** Delete a user account by providing the user ID.
    
*   **Cross-Origin Requests:** Secured with CORS for frontend-backend communication.
    
*   **JWT Authentication:** JWT tokens issued during registration and login.
    

Installation
------------

1.  git clone cd user-authentication
    
2.  Create a virtual environment:
    
    *  python -m venv venvvenv\\Scripts\\activate
        
    *  python3 -m venv venvsource venv/bin/activate
        
3.  pip install -r requirements.txt
    

Environment Variables
---------------------

Create a .env file in the root directory with the following configuration:

   DATABASE_URL=postgresql://postgres:@localhost:5432/DBname
    JWT_SECRET_KEY=" "

*   Replace with your PostgreSQL password.
    
*   python -c "import secrets; print(secrets.token\_hex(32))"  run this in your terminal to generate a secret key
    

Database Setup
--------------

1.  psql -U postgres
    
2.  CREATE DATABASE dbname;
    
3.  The initialize\_db() function in the app will automatically create the users table when the app starts.
    

Running the Microservice
------------------------

Start the application locally:

python app.py

The app will run on http://localhost:5000/.

API Endpoints
-------------

### **User Registration**

*   **Endpoint**: /api/auth/register
    
*   **Method**: POST
    
*   { "username": "exampleuser", "password": "examplepass", "password\_confirm": "examplepass"}
    
*   { "message": "User registered successfully", "access\_token": "eyJhbGciOiJIUzI1..."}
    

### **User Login**

*   **Endpoint**: /api/auth/login
    
*   **Method**: POST
    
*   { "username": "exampleuser", "password": "examplepass"}
    
*   { "message": "Authenticated successfully", "access\_token": "eyJhbGciOiJIUzI1..."}
    

### **Update Credentials**

*   **Endpoint**: /api/auth/change
    
*   **Method**: POST
    
*   { "user\_id": 1, "new\_username": "newuser", "new\_password": "newpass", "new\_password\_confirm": "newpass"}
    
*   { "message": "User credentials updated successfully"}
    

### **Delete Account**

*   **Endpoint**: /api/auth/delete
    
*   **Method**: DELETE
    
*   { "user\_id": 1}
    
*   { "message": "User account deleted successfully"}
    

Technologies Used
-----------------

*   **Python**: Backend programming language.
    
*   **Flask**: Web framework for API development.
    
*   **PostgreSQL**: Database to store user credentials.
    
*   **JWT (JSON Web Tokens)**: Authentication mechanism.
    
*   **Werkzeug**: For secure password hashing.
    
*   **Flask-CORS**: Enables secure cross-origin communication.