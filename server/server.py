from flask import Flask, request, jsonify
from flask_cors import CORS
from sentiment_analyzer_fb import fetch_comments, analyze_comments

app = Flask(__name__)
CORS(app)

# Fetch comments and analyze them
df = fetch_comments()
negative_count, neutral_count, positive_count = analyze_comments(df)


@app.route('/')
def hello_world():
    return "This is the API for sentiment analysis."


@app.route('/api/sentiment-counts', methods=['GET'])
def get_sentiment_counts():
    try:
        # Return the counts as a JSON response
        return jsonify({
            "negative": negative_count,
            "neutral": neutral_count,
            "positive": positive_count
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
