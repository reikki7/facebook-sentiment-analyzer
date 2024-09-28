# Facebook Sentiment Analyzer

This project is a web application that performs sentiment analysis using a pre-trained RoBERTa model. The frontend is built with React and Vite, while the backend is powered by Flask. The application allows users to connect their page and receive sentiment analysis results indicating whether their post is received negatively, neutrally, or positively.

## Prerequisites

- Node.js and npm installed
- Python 3.x installed
- pip (Python package installer) installed

## Server

- **Fetch Comments**: Retrieves comments from a specified source.
- **Analyze Comments**: Analyzes the sentiment of the fetched comments using a pre-trained BERT model.
- **API Endpoints**: Provides endpoints to fetch and analyze comments.

1. Navigate to the `server` directory:

```sh {"id":"01J8SFMMBZNYDKC5F8F18WJ7T8"}
cd server
```

2. Install the dependencies:

```sh {"id":"01J8SFKJ9NW9GP6Q0R79W25NGC"}
pip install -r requirements.txt
```

3. Run the Flask server:

```sh {"id":"01J8SFKJ9NW9GP6Q0R7BC9CTSW"}
python server.py
```

A local IP will show up where the server is hosted.

### API Endpoints

- **GET /**: Returns a simple greeting message.
- **GET /api/sentiment-counts**: Returns the counts of negative, neutral, and positive sentiments.

### File Structure

- `server.py`: The main Flask application.
- `sentiment_analyzer_fb.py`: Contains functions to fetch and analyze comments.
- `requirements.txt`: Lists the required Python packages.

## Client

1. Navigate to the `client`

```sh {"id":"01J8SFKJ9NW9GP6Q0R7DEDMAS5"}
cd client
```

2. Install the required npm packages:

```sh {"id":"01J8SFKJ9NW9GP6Q0R7H7PBR3A"}
npm install
```

3. Start the development server:

```sh {"id":"01J8SFKJ9NW9GP6Q0R7KZBSW2Z"}
npm run dev
```

## Running with GPU

If you want to run the backend using GPU for faster performance, make sure that the CUDA toolkit is installed on your machine. You can follow the instructions at [CUDA Toolkit](https://developer.nvidia.com/cuda-toolkit) to install it.

After installing the CUDA toolkit, you need to install the appropriate version of PyTorch that supports CUDA. Visit [PyTorch Get Started](https://pytorch.org/get-started/locally/) and follow the instructions to install PyTorch with CUDA support.

You should uninstall the regular version of torch before installing the GPU version to avoid any conflicts:

```sh {"id":"01J8SFKJ9NW9GP6Q0R7QADVWZ2"}
pip uninstall torch
```

## Project Details

- **Backend**: The backend is implemented using Flask. It loads a pre-trained BERT model for sentiment analysis and provides an API endpoint to analyze the sentiment of the comments.
- **Frontend**: The frontend is built with React, Vite, and Tailwind CSS. It provides a user interface for inputting text and displaying sentiment analysis results.
- **Model**: The sentiment analysis model used is `cardiffnlp/twitter-roberta-base-sentiment`, a RoBERTa model fine-tuned on Twitter data for sentiment classification.

## Changing Access Token, Post ID, and Page ID

If you want to change the Facebook page or post being analyzed, you can update the access token, post ID, and page ID in the `sentiment_analyzer_fb.py` file.

1. __Access Token__: Retrieve a new access token from the [Facebook Developer Portal](https://developers.facebook.com/). Make sure to set the `page_read_engagement` permission for the page access token. Generate a new token each time you update the permissions.
2. __Post ID and Page ID__: Update the `POST_ID` and `PAGE_ID` variables in the `sentiment_analyzer_fb.py` file with the new values. Which can be obtained with the following link format:

```ini {"id":"01J8SGPXV44004QYGHVFD2QWF8"}
PAGE_ID = https://graph.facebook.com/?id={page_url}&access_token={access_token}
POST_ID = https://graph.facebook.com/{page_id}/posts?access_token={access_token}
```
