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


def test_leaderboard_page_shows_clubs(client):

    """
    Test that the public leaderboard page shows club names and points.
    """
    response = client.get('/leaderboard')
    assert response.status_code == 200
    assert b"Simply Lift" in response.data
    assert b"Iron Temple" in response.data

# Test booking page (valid club + competition)
def test_booking_page_valid(client):
     response = client.get('/book/Fall Classic/Simply Lift', follow_redirects = True)
     assert response.status_code == 200
     assert b'How many places?' in response.data