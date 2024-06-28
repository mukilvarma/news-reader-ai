import os
from flask import Flask, jsonify, render_template
import requests
import openai
import playsound
from gtts import gTTS
import tempfile
import xml.etree.ElementTree as ET
import pygame
import io

app = Flask(__name__, template_folder='templates')

# Set your News API key and OpenAI API key
NEWS_API_KEY = 'cbd680a5fef9440a8a2f136569e5be7f'
OPENAI_API_KEY = 'sk-news-service-NLlhQ6ULVybEEZ7Nj8EuT3BlbkFJZsvRJci1foO7h0GSy3jU'

# Set OpenAI API key
openai.api_key = OPENAI_API_KEY

client = openai.OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key=openai.api_key
)
    
def get_location():
    try:
        response = requests.get('https://ipinfo.io?token=d8b62a31ff33cb')
        if response.status_code == 200:
            data = response.json()
            return data.get('city'), data.get('region'), data.get('country')
        else:
            return None, None, None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching location: {e}")
        return None, None, None

def fetch_news_headliness(query):
    try:
        url = f'https://news.google.com/rss/search?q={' + query + '}'
        response = requests.get(url)
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"Error fetching news: {e}")
        return None
    
def parse_rss_feed(xml_content):
    try:
        root = ET.fromstring(xml_content)
        articles = []
        for item in root.findall('./channel/item'):
            title = item.find('title').text
            description = item.find('description').text
            link = item.find('link').text
            articles.append({'title': title, 'description': description, 'link': link})
        return articles
    except ET.ParseError as e:
        print(f"Error parsing RSS feed: {e}")
        return []
    
def fetch_news_headlines(location, country):
    try:
        url = 'https://newsapi.org/v2/top-headlines'
        params = {
            'apiKey': NEWS_API_KEY,
            'country': country
        }
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching news: {e}")
        return None

def summarize_article(article_text):
    try:
        print("article_text:")
        print(article_text)
        ##prompt=f"Summarize the following news for a headline news reader in 3 - 4 sentences:\n\n{article_text}"
        prompt=f"You are a radio news reader. Read latest news in 4-5 sentences on the topic, and don't add extra like \"for more details..\" or \"the image shows..\" : " + article_text;
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        print("summarized:")
        print(response.choices[0].message.content)
        return response.choices[0].message.content
    except Exception as e:
        print(f"OpenAI API error: {e}")
        return "Failed to summarize article."

def text_to_speech(text):
    # Initialize gTTS with the text and language (English is 'en')
    tts = gTTS(text=text, lang='en')

    # Convert the gTTS object to an in-memory file-like object
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)

    # Initialize Pygame mixer
    pygame.mixer.init()
    pygame.mixer.music.load(fp)
    pygame.mixer.music.play()

    # Wait until the audio has finished playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(5)

@app.route('/')
def index():
    template_path = os.path.join(app.template_folder, 'index.html')
    print(f"Template path: {template_path}")
    return render_template('index.html')

@app.route('/play_news')
def play_news():
    city, state, country = get_location()
    if city and country:
        news_data = fetch_news_headlines(city, country)
    else:
        news_data = fetch_news_headlines('world', 'us')

    if news_data:
        articles = news_data.get('articles', [])
        for article in articles:
            title = article['title']
            #url = article['url']
            description = article.get('description', '')
            content = article.get('content', '')
            full_text = f"{description}"
            if len(full_text.split()) > 5:
                summary = summarize_article(full_text)
                if summary:
                    text_to_speech(summary)
                else:
                    print(f"Failed to summarize article: {title}")
        return jsonify({'message': 'News playback initiated'})
    else:
        return jsonify({'error': 'Failed to fetch news headlines'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

