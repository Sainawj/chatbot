from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash

# MongoDB setup
client = MongoClient('mongodb://localhost:27017/')
db = client['chatbot']
user_collection = db['users']
request_collection = db['requests']

class User:
    @staticmethod
    def register(username, password):
        if user_collection.find_one({'username': username}):
            return False
        hashed_password = generate_password_hash(password)
        user_collection.insert_one({'username': username, 'password': hashed_password})
        return True

    @staticmethod
    def login(username, password):
        user = user_collection.find_one({'username': username})
        if user and check_password_hash(user['password'], password):
            return True
        return False

class UserRequest:
    @staticmethod
    def log_request(username, question, response):
        request_collection.insert_one({
            'username': username,
            'question': question,
            'response': response
        })

    @staticmethod
    def get_requests(username):
        requests = request_collection.find({'username': username}).sort('_id', -1).limit(10)
        return [{'question': req['question'], 'response': req['response']} for req in requests]
