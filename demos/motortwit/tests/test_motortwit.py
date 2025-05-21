import pytest
from aiohttp import web
from bson import ObjectId
from motortwit.main import init
from motortwit.security import generate_password_hash


async def test_user_registration(client):
    """Test user registration endpoint."""
    # Test data
    user_data = {
        'username': 'newuser',
        'email': 'new@example.com',
        'password': 'password123',
        'password2': 'password123'  # Required by the form
    }
    
    # Make registration request with JSON data
    async with client.post('/register', 
                          json=user_data,
                          headers={'Content-Type': 'application/json'}) as resp:
        # Should redirect to login page on success
        assert resp.status == 302
        assert resp.headers['Location'].endswith('/login')