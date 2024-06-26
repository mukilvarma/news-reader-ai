from flask import Flask, jsonify, render_template
import requests
import openai
from playsound import playsound
import socket

app = Flask(__name__)
# Set your News API key and OpenAI API key
NEWS_API_KEY = 'cbd680a5fef9440a8a2f136569e5be7f'
OPENAI_API_KEY = 'sk-news-reader-xbCP8fEaxFoHfli78bpPT3BlbkFJgFsImfIKqMgd8SuzqfrJ'

# Set OpenAI API key
openai.api_key = OPENAI_API_KEY

def get_ip_address():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return ip_address
    
def get_location():
    try:
        IPAddr = get_ip_address()
        response = requests.get('ipinfo.io/IPAddr?token=d8b62a31ff33cb')
        if response.status_code == 200:
            data = response.json()
            return data.get('city'), data.get('region'), data.get('country')
        else:
            return None, None, None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching location: {e}")
        return None, None, None

def fetch_news_headlines(location, country='us'):
    try:
        url = 'https://newsapi.org/v2/top-headlines'
        params = {
            'apiKey': NEWS_API_KEY,
            'country': country,
            'q': location
        }
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching news: {e}")
        return None

def summarize_article(article_text):
    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"Summarize the following article:\n\n{article_text}",
            max_tokens=150
        )
        return response.choices[0].text.strip()
    except openai.Error as e:
        print(f"OpenAI API error: {e}")
        return "Failed to summarize article."

def text_to_speech(text):
    try:
        response = openai.Completion.create(
            model="text-to-speech",
            inputs=text,
            max_tokens=100
        )
        audio_url = response.choices[0].raw_audio['url']
        playsound(audio_url)
    except openai.Error as e:
        print(f"OpenAI API error: {e}")
        print("Failed to convert text to speech.")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/play_news')
def play_news():
    city, state, country = get_location()
    if city:
        news_data = fetch_news_headlines(city)
    else:
        news_data = fetch_news_headlines('world')

    if news_data:
        articles = news_data.get('articles', [])
        for article in articles:
            title = article['title']
            description = article.get('description', '')
            content = article.get('content', '')
            full_text = f"{description}\n{content}"
            summary = summarize_article(full_text)
            if summary:
                text_to_speech(summary)
            else:
                print(f"Failed to summarize article: {title}")
        return jsonify({'message': 'News playback initiated'})
    else:
        return jsonify({'error': 'Failed to fetch news headlines'})

if __name__ == '__main__':
    app.run(debug=True)
