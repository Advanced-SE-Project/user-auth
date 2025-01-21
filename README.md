User Authentication Microservice
================================

A microservice for managing user authentication, including user registration, login, and account management(updating credentials, username and). This service is built with Python, Flask, and PostgreSQL, utilizing JWT for authentication and CORS for secure cross-origin requests.

Table of Contents
-----------------

*   [Overview](#overview)
    
*   [Features](#features)
    
*   [Installation](#installation)
    
*   [Environment Variables](#environment-variables)
    
*   [Database Setup](#database-setup)
    
*   [Running the Microservice](#running-the-microservice)
    
*   [API Endpoints](#api-endpoints)
    
*   [Technologies Used](#technologies-used)
    

Overview
--------

This microservice is responsible for **user authentication** in a microservices-based architecture.  
It **manages user registrations, login sessions, credential updates, and account deletion**.  

🔹 The **JWT tokens** issued upon registration and login allow secure **stateless authentication** between the frontend and backend.  
🔹 The **database stores hashed passwords** using **Werkzeug**, ensuring **secure credential management**.  
🔹 The service supports **cross-origin requests (CORS)** to allow frontend applications to communicate with it.

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

1.  git clone https://github.com/Advanced-SE-Project/user-auth.git
    
2.  Create a virtual environment:
    
    *  python -m venv venvvenv\\Scripts\\activate
        
    *  python3 -m venv venvsource venv/bin/activate
        
3.  Install dependencies:

    * pip install -r requirements.txt
    

Environment Variables
---------------------

Create a .env file in the root directory with the following configuration:

   DATABASE_URL=postgresql://postgres:password@localhost:5432/DBname
    JWT_SECRET_KEY=" "

*   Replace with your PostgreSQL password.
    
*   Replace with your PostgreSQL DBname.
    
*   python -c "import secrets; print(secrets.token\_hex(32))"  run this in your terminal to generate a secret key
    
*   If you want to run it with docker you use DATABASE_URL=postgresql://postgres:password@budged_db:5432/DBname
    

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

**Running with Docker**
-----------------------

To run the microservice using Docker, follow these steps:

### **1️⃣ Build the Docker Image**

`   docker build -t user-auth .   `

### **2️⃣ Run PostgreSQL Database Container**

`   docker run --name budget_db -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=PASSWORD -e POSTGRES_DB=budget_db -p 5432:5432 -d postgres   `

### **3️⃣ Run the Microservice Container**

`   docker run --name user-auth-container \    --env-file .env -p 5000:5000 --link budget_db user-auth   `


🔒 JWT Authentication Flow
--------------------------

1️⃣ **User Registers/Login → Server Generates a JWT**
2️⃣ **Frontend Stores the Token (Local Storage or Session Storage)**

🔹 **Example of JWT Token**

`   {    "access_token": "eyJhbGciOiJIUzI1..."  }   `


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
    


🧪 Testing the Microservice
---------------------------

### **1️⃣ Run All Tests**

`   pytest tests/   `

### **2️⃣ Run Only Unit Tests**

`   pytest tests/test_unit.py   `

### **3️⃣ Run Only Integration Tests**

`   pytest tests/test_integration.py   `


Technologies Used
-----------------

*   **Python**: Backend programming language.
    
*   **Flask**: Web framework for API development.
    
*   **PostgreSQL**: Database to store user credentials.
    
*   **JWT (JSON Web Tokens)**: Authentication mechanism.
    
*   **Werkzeug**: For secure password hashing.
    
*   **Flask-CORS**: Enables secure cross-origin communication.



**Author**: Erisa Halipaj  
**Date**: 19/01/2025  

This document provides setup instructions, API documentation, 
and usage details for the authentication microservice.