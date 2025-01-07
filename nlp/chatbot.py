import json

# Load FAQ data from JSON file
def load_faq_data():
    with open('data/faq.json', 'r') as file:
        return json.load(file)

# Function to get chatbot response based on user input
def get_response(user_input, faq_data):
    # Basic keyword matching logic to get the most relevant answer
    for faq in faq_data:
        if faq['question'].lower() in user_input.lower():
            return faq['answer']
    return "Sorry, I don't have an answer for that."