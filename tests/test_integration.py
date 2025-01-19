import pytest
import json
from .test_config import client

def test_register_user(client):
    """Test user registration"""
    response = client.post("/api/auth/register",
        data=json.dumps({"username": "testuser", "password": "testpass", "password_confirm": "testpass"}),
        content_type="application/json"
    )
    data = response.get_json()
    
    assert response.status_code == 201
    assert "access_token" in data  # JWT token should be returned

def test_login_user(client):
    """Test user login"""
    response = client.post("/api/auth/login",
        data=json.dumps({"username": "testuser", "password": "testpass"}),
        content_type="application/json"
    )
    data = response.get_json()
    
    assert response.status_code == 200
    assert "access_token" in data  # JWT token should be returned

def test_update_credentials(client):
    """Test updating user credentials"""
    response = client.post("/api/auth/change", 
        data=json.dumps({"user_id": 1, "new_username": "newuser", "new_password": "newpass", "new_password_confirm": "newpass"}), 
        content_type="application/json"
    )
    
    assert response.status_code == 200
    assert response.get_json()["message"] == "User credentials updated successfully"

def test_delete_user(client):
    """Test deleting a user"""
    response = client.delete("/api/auth/delete", 
        data=json.dumps({"user_id": 1}), 
        content_type="application/json"
    )
    
    assert response.status_code == 200
    assert response.get_json()["message"] == "User account deleted successfully"
