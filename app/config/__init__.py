from pymongo import MongoClient

connection_string = "mongodb+srv://AnaDunareanu:8wD0uZWeWz7ldvWZ@cluster0.saszelz.mongodb.net/"
client = MongoClient(connection_string)

# database access
db = client['cloudCompass_db']

# access collection within the database 
collection = db['users']


