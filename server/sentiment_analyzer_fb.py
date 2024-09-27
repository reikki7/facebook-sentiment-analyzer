import requests
import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from scipy.special import softmax
from tqdm import tqdm
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Define the post ID and access token for the Facebook post
page_id = "103127515742819"
post_id = "362265946498193"
access_token = os.getenv("ACCESS_TOKEN")

# Load pre-trained BERT model and tokenizer for sentiment analysis
MODEL = "cardiffnlp/twitter-roberta-base-sentiment"
tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForSequenceClassification.from_pretrained(MODEL)

# Check if GPU is available and set the device accordingly
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)


def fetch_comments():
    '''Fetch comments from a Facebook post using the Graph API.'''

    # Initialize an empty list to store all messages
    all_messages = []

    # Start with the initial URL
    url = f"https://graph.facebook.com/v20.0/{page_id}_{post_id}/comments?access_token={access_token}"
    print(url)

    while True:
        response = requests.get(url)
        if response.status_code == 200:
            comments_data = response.json()
            # Extract messages from the current page
            messages = [comment.get('message', 'No message')
                        for comment in comments_data['data']]
            # Append the messages to the list
            all_messages.extend(messages)
            # Check if there is a next page
            if 'paging' in comments_data and 'next' in comments_data['paging']:
                # Update the URL to the next page
                url = comments_data['paging']['next']
            else:
                # No more pages, exit the loop
                break
        else:
            print(
                f"Error fetching comments: {response.status_code}, {response.text}")
            break

    # Create DataFrame with all messages
    df = pd.DataFrame(all_messages, columns=['message'])
    print(df)
    return df


def polarity_scores(text):
    '''Calculate the sentiment scores of a text using a pre-trained sentiment analysis model.'''

    # Tokenize the input text and convert it to tensors
    encoded_text = tokenizer(text, return_tensors="pt",
                             truncation=True, max_length=512)
    # Move the tensors to the appropriate device (GPU or CPU)
    encoded_text = {k: v.to(device) for k, v in encoded_text.items()}
    # Perform a forward pass through the model to get the output
    with torch.no_grad():
        output = model(**encoded_text)
    # Extract the scores from the model output, move them to CPU, and convert to numpy array
    scores = output[0][0].cpu().numpy()
    # Apply softmax to the scores to get probabilities
    scores = softmax(scores)
    # Create a dictionary to map the scores to sentiment labels
    scores_dict = {
        "negative": float(scores[0]),
        "neutral": float(scores[1]),
        "positive": float(scores[2])
    }
    # Return the sentiment scores dictionary
    return scores_dict


def analyze_comments(df):
    '''Analyze the sentiment of comments in a DataFrame using a pre-trained sentiment analysis model.'''

    # Initialize an empty dictionary to store the results
    res = {}

    # Iterate over each row in the DataFrame with a progress bar
    for i, row in tqdm(df.iterrows(), total=len(df)):
        try:
            # Extract the text from the current row
            text = row['message']
            # Calculate the polarity scores for the text
            scores = polarity_scores(text)
            # Store the scores in the results dictionary with the index as the key
            res[i] = scores
        except RuntimeError as e:
            # Print an error message if a RuntimeError occurs
            print(f"Error processing id {i}: {e}")

    # Count the negative, neutral, and positive scores
    negative_count = sum(1 for v in res.values(
    ) if v['negative'] > v['neutral'] and v['negative'] > v['positive'])
    neutral_count = sum(1 for v in res.values(
    ) if v['neutral'] > v['negative'] and v['neutral'] > v['positive'])
    positive_count = sum(1 for v in res.values(
    ) if v['positive'] > v['negative'] and v['positive'] > v['neutral'])

    return negative_count, neutral_count, positive_count
