import os

# MongoDB Configuration
MONGO_URI = 'mongodb://localhost:27017/chatbot'

# Flask Secret Key for sessions
SECRET_KEY = os.urandom(24)
