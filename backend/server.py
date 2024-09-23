from flask import Flask, request, jsonify 
from flask_cors import CORS
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from scipy.special import softmax

# BERT is a transformer-based machine learning model that has been pre-trained on a large corpus of text data.
# It can be fine-tuned for various natural language processing (NLP) tasks, such as sentiment analysis, text classification, question answering, and more.
# In this example, we will use a pre-trained BERT model for sentiment analysis on user input.

app = Flask(__name__)
CORS(app)  # Enable CORS (Cross-Origin Resource Sharing) for all routes, allowing the API to be accessed from any domain

# Load pre-trained BERT model and tokenizer for sentiment analysis
MODEL = "cardiffnlp/twitter-roberta-base-sentiment"  # Specify the model to be used (Twitter-based RoBERTa sentiment model)
tokenizer = AutoTokenizer.from_pretrained(MODEL)  # Load the pre-trained tokenizer for the specified model
model = AutoModelForSequenceClassification.from_pretrained(MODEL)  # Load the pre-trained model for sequence classification

# Check if GPU is available and set the device accordingly
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")  # Use GPU if available, otherwise default to CPU
model = model.to(device)  # Move the model to the appropriate device (CPU or GPU)

# Function to perform sentiment analysis on the given text
def get_sentiment(text):
    encoded_text = tokenizer(text, return_tensors="pt")  # Tokenize the input text and convert it into PyTorch tensors
    encoded_text = {k: v.to(device) for k, v in encoded_text.items()}  # Move the tokenized text to the correct device (CPU or GPU)
    
    with torch.no_grad():  # Disable gradient calculation for faster inference (no need for backpropagation)
        output = model(**encoded_text)  # Pass the encoded text through the model to get the output (logits)
    
    scores = output.logits[0].cpu().numpy()  # Move the logits to CPU and convert them to a NumPy array
    scores = softmax(scores)  # Apply the softmax function to convert logits into probabilities for each sentiment class
    
    # Return the sentiment scores for negative, neutral, and positive classes
    return {
        "negative": float(scores[0]),  # Probability of the text being negative
        "neutral": float(scores[1]),  # Probability of the text being neutral
        "positive": float(scores[2])  # Probability of the text being positive
    }

# Define an API endpoint for sentiment analysis
@app.route('/analyze', methods=['POST'])  # Define a POST route for analyzing sentiment
def analyze_sentiment():
    data = request.json  # Get the JSON data from the request
    text = data.get('text', '')  # Extract the 'text' field from the JSON data, defaulting to an empty string if not provided

    if not text:  # If no text is provided, return an error response
        return jsonify({"error": "No text provided"}), 400  # Respond with an error message and HTTP status 400 (Bad Request)

    sentiment = get_sentiment(text)  # Call the get_sentiment function to analyze the sentiment of the input text
    return jsonify(sentiment)  # Return the sentiment scores as a JSON response

# Main entry point for the application
if __name__ == '__main__':
    app.run(debug=True)  # Run the Flask app in debug mode (useful for development)
