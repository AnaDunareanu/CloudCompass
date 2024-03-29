import bcrypt
from models.User import User 
from config.__init__ import collection

def generate_password_hash(password):
    bytes = password.encode('utf-8')
    salt = bcrypt.gensalt() 
    hashed_password = bcrypt.hashpw(bytes, salt)
    return salt, hashed_password

def register_user(username, password):
    user = {
        'username': username,
        'password': password
    }

    salt, hashed_password = generate_password_hash(password)

    if collection.find_one({'username': username}):
        return 'Username already exists'
    
    if not username or not password:
        return 'Username and password are required'
    
    new_user = User(username=username, password=hashed_password, salt=salt)

    new_user.save()

def login_user(username, password):
    user = collection.find_one({'username': username})
    if not user:
        return 'User not found'

    stored_salt = user['salt']
    stored_hashed_password = user['password']

    # Hash the provided password with the stored salt
    provided_hashed_password = bcrypt.hashpw(password.encode('utf-8'), stored_salt)

    # Check if the provided hashed password matches the stored hashed password
    if provided_hashed_password == stored_hashed_password:
        return 'Login successful'
    else:
        return 'Invalid password'
        