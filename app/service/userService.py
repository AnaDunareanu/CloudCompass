import bcrypt
from models.User import User 
from config.__init__ import collection



def generate_password_hash(password):
    bytes = password.encode('utf-8')
    salt = bcrypt.gensalt() 
    hashed_password = bcrypt.hashpw(bytes, salt)
    return salt, hashed_password



def register_user(username, password):
 
    salt, hashed_password = generate_password_hash(password)

    if collection.find_one({'username': username}):
        return 'Username already exists'
    
    new_user = User(username=username, password=hashed_password, salt=salt)

    new_user.save()




def login_user(username, password):

    user = collection.find_one({'username': username})

    if user:
        stored_hashed_password = user.get('password')
        if not bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password):
            return 'Invalid username or password'
    else:
        return 'Invalid username or password'
        