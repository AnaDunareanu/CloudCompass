from flask import Flask, request, jsonify, render_template, redirect, url_for
from service.userService import register_user, login_user
from service.searchService import search_flights, log_search_history, get_search_history, get_geocode
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
from flask_cors import CORS
from geopy.geocoders import Nominatim



app = Flask(__name__)
geolocator = Nominatim(user_agent="CloudCompass")
app.config['JWT_SECRET_KEY'] = '6861756d696175'
jwt = JWTManager(app)
CORS(app)


@app.route('/home')
def home():
    return render_template('homePage.html')


@app.route('/register', methods=['POST', 'GET'])
def register():

    if request.method == 'GET':
        # Render the registration form template
        return render_template('register.html')
    elif request.method == 'POST':
        # Extract username and password from the request
        username = request.json.get('username')
        password = request.json.get('password')

        if not username or not password:
            return jsonify({'error': 'Username and password are required'}), 400

        # Call the register_user function
        result = register_user(username, password)

        # Check the result and return appropriate response
        if isinstance(result, str):
            # If result is a string, it's an error message
            return jsonify({'error': result}), 400
        else:
            #Generate access token, registration was successful
            access_token = create_access_token(identity=username)
            return jsonify({'message': 'User registered successfully', 'token': access_token}), 201
    

@app.route('/', methods=['GET'])
def index():
    return render_template('homePage.html', error=None)


@app.route('/login', methods=['POST', 'GET'])
def login():

    if request.method == 'POST':
        # Extract username and password from the form data
        username = request.json.get('username')
        password = request.json.get('password')

        if not username or not password:
            return jsonify({'message': 'Login Fail'}), 401

        # Call the login_user function
        result = login_user(username, password)

        # Check the result and return appropriate response
        if isinstance(result, str):
            # If result is a string, it's an error message
            return jsonify({'message': 'Login Fail'}), 401
        else:
            # Generate access token, login was successful
            access_token = create_access_token(identity=username)
            return jsonify({'message': 'Login successful', 'token': access_token}), 200
    if request.method == 'GET':
        # Render the login form
        return render_template('login.html', error=None)
    
    
@app.route('/get-coordinates', methods=['POST'])
@jwt_required()
def get_coordinates():
    data = request.get_json()
    origin_name = data.get('origin')
    destination_name = data.get('destination')

    # Get coordinates for the origin and destination using the helper function
    origin_coords = get_geocode(origin_name)
    destination_coords = get_geocode(destination_name)

    # Check if there was an error in geocoding and handle it
    if 'error' in origin_coords or 'error' in destination_coords:
        error_message = origin_coords.get('error') or destination_coords.get('error')
        return jsonify({'error': error_message}), 500

    response = {
        'origin': origin_coords,
        'destination': destination_coords
    }
    return jsonify(response)


@app.route('/search', methods=['GET'])
def getSearchPage():
    return render_template('search.html', error=None)

@app.route('/search', methods=['POST'])
@jwt_required()
def search():
    user_id = get_jwt_identity()
    data = request.get_json()
    origin = data.get('origin')
    destination = data.get('destination')
    date = data.get('date')
    airline = data.get('airline')

    if not origin or not destination or not date or not airline:
        return jsonify({'error': 'Missing data, please provide origin, destination, date, and airline'}), 400

    try:
        price = search_flights(origin, destination, date, airline)
        log_search_history(user_id, origin, destination, date, airline)
        return jsonify({'predicted_price': price}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500




@app.route('/history', methods=['GET'])
@jwt_required()
def search_history():
    user_id = get_jwt_identity()
    search_history = get_search_history(user_id)
    return jsonify(search_history)



@app.route('/history-page', methods=['GET'])
def search_history_page():
    return render_template('history.html')


if __name__ == '__main__':
    app.run(port=8000, debug=True)
