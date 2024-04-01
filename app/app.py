from flask import Flask, request, jsonify
from service.userService import register_user, login_user
from service.searchService import search_flights, log_search_history, get_search_history
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity


app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = '6861756d696175'
jwt = JWTManager(app)

@app.route('/register', methods=['POST'])
def register():
    # Extract username and password from the request
    username = request.json.get('username')
    password = request.json.get('password')

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
    

    
@app.route('/login', methods=['POST'])
def login():
    # Extract username and password from the request
    username = request.json.get('username')
    password = request.json.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    # Call the login_user function
    result = login_user(username, password)

    # Check the result and return appropriate response
    if isinstance(result, str):
        # If result is a string, it's an error message
        return jsonify({'error': result}), 400
    else:
        #Generate access token, login was successful
        access_token = create_access_token(identity=username)
        return jsonify({'message': 'Login successful', 'token': access_token}), 200
    
    

@app.route('/search', methods=['GET'])
@jwt_required()
def search():
    origin = request.json.get('origin')
    destination = request.json.get('destination') 
    date = request.json.get('date') 
    airline = request.json.get('airline')

    user_id = get_jwt_identity()

    result = search_flights(origin, destination, date, airline)

    log_search_history(user_id, origin, destination, date, airline)

    if isinstance(result, str):
        return jsonify({'error': result}), 400
    else:
        return jsonify(result), 200


@app.route('/history', methods=['GET'])
@jwt_required()
def search_history():

    user_id = get_jwt_identity()

    search_history = get_search_history(user_id)

    if not search_history:
        return jsonify({'message': 'No search history found'}), 404

    return jsonify(search_history), 200



if __name__ == '__main__':
    app.run(debug=True)
