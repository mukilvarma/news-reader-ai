from flask import Flask, jsonify, render_template
import requests
import openai
import playsound
import socket

app = Flask(__name__)
# Set your News API key and OpenAI API key
NEWS_API_KEY = 'cbd680a5fef9440a8a2f136569e5be7f'
OPENAI_API_KEY = 'sk-news-reader-xbCP8fEaxFoHfli78bpPT3BlbkFJgFsImfIKqMgd8SuzqfrJ'

# Set OpenAI API key
openai.api_key = OPENAI_API_KEY

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/play_news')
def play_news():
    print("Failed to convert text to play news.")

if __name__ == '__main__':
    app.run(debug=True)
