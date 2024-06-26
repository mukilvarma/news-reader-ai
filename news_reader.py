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
        search_query = f"{location} news"
        news_data = googlenews.search(search_query)
        return news_data
    except Exception as e:
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

def read_news(location):
    print("Fetching news headlines...")
    news_data = fetch_news_headlines(location)
    if news_data:
        articles = news_data['entries']
        for article in articles:
            title = article['title']
            summary = article.get('summary', '')
            print(f"Title: {title}")
            print(f"Summary: {summary}")
            text_to_speech(summary)
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
