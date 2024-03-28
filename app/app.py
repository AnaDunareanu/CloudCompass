from flask import Flask, request, jsonify
from service.userService import register_user, login_user

app = Flask(__name__)

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
        # If result is not a string, registration was successful
        return jsonify({'message': 'User registered successfully'}), 201
    

    
@app.route('/login', methods=['POST'])
def login():
    # Extract username and password from the request
    username = request.json.get('username')
    password = request.json.get('password')

    # Call the login_user function
    result = login_user(username, password)

    # Check the result and return appropriate response
    if isinstance(result, str):
        # If result is a string, it's an error message
        return jsonify({'error': result}), 400
    else:
        # If result is not a string, login was successful
        return jsonify({'message': 'Login successfull'}), 200
    

#Mock flights database

flights = [
    {'origin': 'NYC', 'destination': 'LAX', 'date': '2024-04-01', 'airline': 'Delta', 'price': 300},
    {'origin': 'LAX', 'destination': 'NYC', 'date': '2024-04-01', 'airline': 'United', 'price': 350},
    {'origin': 'NYC', 'destination': 'LAX', 'date': '2024-04-02', 'airline': 'Delta', 'price': 320},
]
    

@app.route('/search', methods=['GET'])
def search_flights():
    origin = request.json.get('origin')
    destination = request.json.get('destination') 
    date = request.json.get('date') 
    airline = request.json.get('airline')

    results = []

    if not origin or not destination or not date or not airline:    
        return jsonify({'error': 'All fields are required'}), 400

    for flight in flights:
        if flight['origin'] == origin and flight['destination'] == destination and flight['date'] == date and flight['airline'] == airline:
            results.append(flight)

    if not results:
        return jsonify({'message': 'No flights found'}), 404
    
    return jsonify(results), 200



if __name__ == '__main__':
    app.run(debug=True)
