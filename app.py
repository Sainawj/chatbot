from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
from nlp.chatbot import get_response
from pymongo import MongoClient
import json
from models import User

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Secret key for sessions

# Load FAQ data from JSON
with open('data/faq.json') as f:
    faq_data = json.load(f)

# MongoDB setup
client = MongoClient('mongodb://localhost:27017/')
db = client['chatbot']
collection = db['interactions']

@app.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    # Send only the most asked questions to the frontend
    most_asked = faq_data[:5]  # Adjust the number of most asked questions as needed
    return render_template('index.html', most_asked=most_asked)

@app.route('/get_response', methods=['POST'])
def get_bot_response():
    user_input = request.form['message']
    response = get_response(user_input, faq_data)
    # Save the conversation in MongoDB
    collection.insert_one({"user_input": user_input, "bot_response": response, "username": session.get('username')})
    return jsonify({'response': response})

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Validate login credentials
        user = User.login(username, password)
        if user:
            session['username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password!', 'error')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out!', 'info')
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if 'username' in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Register the new user
        if User.register(username, password):
            flash('Signup successful! Please log in.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Username already exists!', 'error')

    return render_template('signup.html')

if __name__ == '__main__':
    app.run(debug=True)