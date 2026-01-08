import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from server import app,clubs
from datetime import datetime
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
    # Get the club before booking
    club = [c for c in clubs if c["name"] == "Simply Lift"][0]
    initial_points = int(club["points"])

    # Make the booking (book 2 places)
    response = client.post('/purchasePlaces', data={
        'competition': 'Fall Classic',
        'club': 'Simply Lift',
        'places': '2'
    }, follow_redirects=True)

    # After booking, points should be deducted
    updated_points = int(club["points"])

    # Assert the updated points = initial - 2
    assert updated_points == initial_points - 2

    # Check that the success message is displayed
    assert b"Great - booking complete!" in response.data

def test_past_competitions_not_shown(client):
    """
     Test that past competitions are not shown on the welcome page after login.

    """
    #simulate login with valid club email
    response = client.post('/showSummary', data = {
        'email': 'john@simplylift.co'
    }, follow_redirects = True)
    #competition in the past
    assert b"Spring Festival" not in response.data

    #checks future competition shows up
    assert b"Fall Classic" in response.data