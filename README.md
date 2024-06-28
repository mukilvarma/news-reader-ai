# News Reader Application

The News Reader Application is a Flask-based web application that fetches top headlines from News API, summarizes them using OpenAI's GPT-3 model, and streams audio summaries to the user.

## Features

- Fetches top headlines based on the user's location (using IP geolocation).
- Summarizes news articles into concise audio summaries using OpenAI's GPT-3 model.
- Streams audio summaries with a 2-second gap between articles for a seamless listening experience.

## Technologies Used

- Python
- Flask
- Requests library (for API requests)
- OpenAI API (for text summarization)
- gTTS (Google Text-to-Speech) library (for audio generation)
- Heroku (for deployment)

## Setup Instructions

### Prerequisites

- Python 3.7 or higher installed on your system.
- Access to the internet for API calls.
- News API key and OpenAI API key (replace placeholders in the code).

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/news-reader-app.git
   cd news-reader-app
   
2. Install dependencies:

  ```bash
  pip install -r requirements.txt

