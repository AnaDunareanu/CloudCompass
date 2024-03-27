from config.__init__ import collection

class User:
    def __init__(self, username, password, salt=None):
        self.username = username
        self.password = password
        self.salt = salt

    def save(self):
        collection.insert_one({'username': self.username, 'password': self.password, 'salt': self.salt})

