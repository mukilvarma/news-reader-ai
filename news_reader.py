import openai
from gtts import gTTS
import requests
import feedparser
from playsound import playsound
import os

# Set your OpenAI API key
OPENAI_API_KEY = 'sk-news-reader-xbCP8fEaxFoHfli78bpPT3BlbkFJgFsImfIKqMgd8SuzqfrJ'
openai.api_key = OPENAI_API_KEY

def get_location():
    try:
        response = requests.get('https://ipinfo.io')
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
        feed_url = f"https://news.google.com/rss/search?q={location}+news&hl={country}&gl={country}&ceid={country}:en"
        news_feed = feedparser.parse(feed_url)
        return news_feed.entries
    except Exception as e:
        print(f"Error fetching news: {e}")
        return None

def summarize_article(article_text):
    try:
        response = openai.Completion.create(
            model="gpt-3.5-turbo",
            prompt=f"Summarize the following article:\n\n{article_text}",
            max_tokens=150
        )
        return response.choices[0].text.strip()
    except openai.error.OpenAIError as e:
        print(f"OpenAI API error: {e}")
        return "Failed to summarize article."

def text_to_speech(text):
    tts = gTTS(text=text, lang='en')
    tts.save('output.mp3')
    playsound('output.mp3')
    os.remove('output.mp3')

def read_news(location):
    print("Fetching news headlines...")
    articles = fetch_news_headlines(location)
    if articles:
        for article in articles:
            title = article['title']
            summary = article.get('summary', '')
            full_text = f"{summary}"
            summarized_text = summarize_article(full_text)
            print(f"Title: {title}")
            print(f"Summary: {summarized_text}")
            text_to_speech(summarized_text)
    else:
        print("Failed to fetch news headlines.")

if __name__ == '__main__':
    city, state, country = get_location()
    if city:
        print(f"Fetching news headlines for {city}, {state}, {country}...")
        read_news(city)
    else:
        print("Unable to determine location. Fetching global news headlines...")
        read_news('world')
