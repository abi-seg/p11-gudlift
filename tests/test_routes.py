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

# Test login with invalid email address

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

def test_booking_more_than_12_places(client):

        """
        Booking more than 12 places should fail with an error.

        """
        response = client.post('/purchasePlaces', data = {
            'competition' : 'Fall Classic',
            'club' : 'Simply Lift',
            'places' : 13

        }, follow_redirects = True)

        assert b"You cannot book more than 12 places per competition." in response.data

def test_leaderboard_page_shows_clubs(client):
    """
    Test that the public leaderboard page shows club names and points.
    """
    response = client.get('/leaderboard')
    
    assert response.status_code == 200
    assert b'Simply Lift' in response.data  # Club name
    assert b'Iron Temple' in response.data 
    assert b'She Lifts' in response.data

# Test booking page (valid club + competition)
def test_booking_page_valid(client):
     response = client.get('/book/Fall Classic/Simply Lift', follow_redirects = True)
     assert response.status_code == 200
     assert b'How many places?' in response.data

# Test: booking fails with insufficient club points

def test_booking_not_enough_points(client):
     response = client.post('/purchasePlaces', data = {
          'competition': 'Fall Classic',
          'club': 'Iron Temple', # only 4 points in JSON
          'places': 5
     }, follow_redirects = True)
     assert b'You do not have enough points to book these places.' in response.data

# Test: Booking fails if not enough competition places
def test_booking_exceeds_competition_spots(client):
     response = client.post('/purchasePlaces', data = {
          'competition': 'Mini Comp',
          'club': 'Simply Lift',
          'places': '5' # more than 3
     }, follow_redirects = True)
     assert b'There are not enough places left in this competition.' in response.data

# Test: Booking fails if invalid club or competition
def test_booking_invalid_club_or_competition(client):
     response = client.get('/book/FakeCompetition/FakeClub', follow_redirects = True)
     assert response.status_code == 200
     assert b"Something went wrong" in response.data

# Test: Successful booking shows flash confirmation
def test_successful_booking_shows_confirmation(client):
     # visiting booking page to set necessary context
     client.get('/book/Fall Classic/Simply Lift')
     #submitting the booking form
     response = client.post('/purchasePlaces', data = {
          'competition': 'Fall Classic',
          'club': 'Simply Lift',
          'places': '1'
     }, follow_redirects = True)
     assert response.status_code == 200
     assert b"Great - booking complete!" in response.data
     print(response.data.decode())

# Test: Access to root home page
def test_homepage_route(client):
     response = client.get('/')
     assert response.status_code == 200
     assert b"View Club Leaderboard" in response.data

# Test: Logout redirects to home
def tests_logout_redirects_to_home(client):
     response = client.get('/logout', follow_redirects = True)
     assert response.status_code == 200
     assert b"View Club Leaderboard" in response.data
