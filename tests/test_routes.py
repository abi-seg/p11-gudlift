import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from server import app,clubs

import pytest

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_invalid_login_email(client):

    """
    Test login with wrong email does not crash.
    
    """
    response = client.post('/showSummary', data={'email': 'wrong@email.com'})
    assert response.status_code in (200, 302)

def test_points_deducted_after_booking(client):
    
    """
     Ensure that club points are lowered after a successful booking.

     """
    # first: get current points
    start_points = int([c for c in clubs if c["name"] == "Simply Lift"][0]["points"])

    #Book 2 places
    client.post('/purchasePlaces', data = {
        'competition': 'Fall Classic',
        'club': 'Simply Lift',
        'places': '2'
    })

    # New points should be start - 2
    end_points = int([c for c in clubs if c["name"] == "Simply Lift"][0]["points"])
    assert end_points == start_points - 2