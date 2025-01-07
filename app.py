from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
from pymongo import MongoClient
from models import User, UserRequest
import json

app = Flask(__name__)
app.secret_key = 'f7a5ea38aa64fc9ea8251e9c904729f0ff13731fa2f4a5c1ac1cc142353aa1f6'  # Secret key for sessions

# Load FAQ data from JSON
with open('data/faq.json') as f:
    faq_data = json.load(f)

# MongoDB setup
client = MongoClient('mongodb://localhost:27017/')
db = client['chatbot']

@app.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    # Fetch previously logged questions for the logged-in user
    logged_questions = UserRequest.get_requests(session['username'])
    
    # Display most asked questions
    most_asked = faq_data[:5]
    return render_template('index.html', most_asked=most_asked, logged_questions=logged_questions)

@app.route('/get_response', methods=['POST'])
def get_bot_response():
    if 'username' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    user_input = request.form['message']
    response = get_response(user_input, faq_data)
    
    # Log the request and response
    UserRequest.log_request(session['username'], user_input, response)
    
    return jsonify({'response': response})

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if User.login(username, password):
            session['username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password!', 'danger')

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
        
        if User.register(username, password):
            flash('Signup successful! Please log in.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Username already exists!', 'danger')

    return render_template('signup.html')

if __name__ == '__main__':
    app.run(debug=True)
