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
        return jsonify({'message': result}), 200

if __name__ == '__main__':
    app.run()
