import json
from flask import Flask,render_template,request,redirect,flash,url_for


def loadClubs():

    """
        Load clubs from the JSON file.

        Returns:
            list: A list of club dictionnaries with name, email and endpoints.
    """
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():

    """
        Load competitions from the JSON file.

        Returns:
            list: A list of competition dictionaries with name,date and number of places.
    """
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions


app = Flask(__name__) # Intialize Flask app setup
app.secret_key = 'something_special' # Required for using flash messages

competitions = loadCompetitions() # Load data once at startup
clubs = loadClubs()

@app.route('/') # Home page route
def index():

    """
        Home page route.
        Displays the login form.

     Returns:
        rendered HTML (index.html)

    """
    return render_template('index.html')

@app.route('/showSummary',methods=['POST'])
def showSummary():

    """
        Handle form submission from login.
        
        Looks for a club matching the provided email and returns the welcome page.
    Returns:
        Index error: If no club matches

    """

    email = request.form['email']
    matching_clubs = [club for club in clubs if club['email'] == email]

    if not matching_clubs:
        flash("Email address not found. Please try again.")
        return redirect(url_for('index'))
    club = matching_clubs[0]
    return render_template('welcome.html',club = club, competitions = competitions)

@app.route('/book/<competition>/<club>')

def book(competition,club):

    """
        Show booking page for a specific club and competition.
      Args:
        competition (str): Name of the competition.
        club (str): Name of the club.
      Returns:
        rendered HTML (booking.html or welconme.html)
    """

    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html',club=foundClub,competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    """
    Handle booking submission.
    Deducts requested number of places from competition, and displays confirmation.

    Returns:
        rendered HTML (welcome.html) with flash message
    """
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])
<<<<<<< Updated upstream
    
    #new points check (Prevent booking if not enough points)
    available_points = int(club['points'])
=======

    available_points = int(club['points'])
    available_places = int(competition['numberOfPlaces'])

   


    if placesRequired > available_points:
        flash("You do not have enough points to book these places.")
        return render_template('booking.html', club=club, competition=competition)

    if placesRequired > available_places:
        flash("Not enough places available in the competition.")
        return render_template('booking.html', club=club, competition=competition)

    # Validation passed
    club['points'] = str(available_points - placesRequired)
    competition['numberOfPlaces'] = str(available_places - placesRequired)

    flash('Great - booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions)
>>>>>>> Stashed changes

    if placesRequired > available_points:
        flash ("You do not have enough points to book these places.")
        return render_template('booking.html', club = club, competition = competition)
    
    #check: placesRequired can't exceed remainig competition spots

    if placesRequired > int(competition['numberOfPlaces']):
        flash ("Not enough places available in the competition.")
        return render_template('booking.html', club = club, competition = competition)
    
    # all valid : deduct points and competition places
    club ['points'] = str(available_points - placesRequired)
    competition['numberOfPlaces'] = str(int(competition['numberOfPlaces']) - placesRequired)

    flash('Great - booking complete!')
    return render_template('welcome.html', club = club)

# TODO: Add route for points display


@app.route('/logout')
def logout():

    """
    Logs the user out by redirecting to the homepage.

    Returns:
     redirect to index route
    
     """
    
    return redirect(url_for('index'))