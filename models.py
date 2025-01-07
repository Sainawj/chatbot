from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash

# MongoDB Setup
client = MongoClient('mongodb://localhost:27017/')
db = client['chatbot']
user_collection = db['users']

class User:
    @staticmethod
    def register(username, password):
        # Check if username already exists
        if user_collection.find_one({'username': username}):
            return False
        hashed_password = generate_password_hash(password)
        user_collection.insert_one({'username': username, 'password': hashed_password})
        return True

    @staticmethod
    def login(username, password):
        # Check if user exists
        user = user_collection.find_one({'username': username})
        if user and check_password_hash(user['password'], password):
            return True
        return False