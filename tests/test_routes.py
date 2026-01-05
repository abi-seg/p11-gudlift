import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from server import app

import pytest

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_invalid_login_email(client):
    """Test login with wrong email does not crash."""
    response = client.post('/showSummary', data={'email': 'wrong@email.com'})
    assert response.status_code in (200, 302)