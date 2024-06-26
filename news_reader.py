import requests
import openai
import pyttsx3
import os

# Set your News API key and OpenAI API key
NEWS_API_KEY = 'cbd680a5fef9440a8a2f136569e5be7f'
OPENAI_API_KEY = 'sk-news-reader-xbCP8fEaxFoHfli78bpPT3BlbkFJgFsImfIKqMgd8SuzqfrJ'

# Set OpenAI API key
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

def fetch_news_headlines(location, country):
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
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def read_news(location, country):
    print("Fetching news headlines...")
    news_data = fetch_news_headlines(location, country)
    if news_data:
        articles = news_data.get('articles', [])
        for article in articles:
            title = article['title']
            description = article.get('description', '')
            content = article.get('content', '')
            full_text = f"{description}\n{content}"
            summary = summarize_article(full_text)
            print(f"Title: {title}")
            print(f"Summary: {summary}")
            text_to_speech(summary)
    else:
        print("Failed to fetch news headlines.")

if __name__ == '__main__':
    city, state, country = get_location()
    if city:
        print(f"Fetching news headlines for {city}, {state}, {country}...")
        read_news(city, country)
    else:
        print("Unable to determine location. Fetching global news headlines...")
        read_news('world', 'world')
