from os import getenv

from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv

from .functions import (
    get_tweets, 
    load_tweet_text,
)


load_dotenv()
SECRET_KEY=getenv('SECRET_KEY')
BEARER_TOKEN=getenv('BEARER_TOKEN')


app = Flask(__name__)
app.config.from_mapping(
    SECRET_KEY=SECRET_KEY,
)

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('parrot/home.html')
    elif request.method == 'POST':
        username = request.form['search']
        return redirect(url_for('list_tweets', username=username))


@app.route("/<username>")
def list_tweets(username):
    if request.args.get('cursor'):
        next_token = request.args.get('cursor')
    else:
        next_token = ''
    tweets = get_tweets(username, bearer_token=BEARER_TOKEN, next_token=next_token)
    if tweets:
        tweets = load_tweet_text(tweets)
        return render_template('parrot/index.html', tweets=tweets, username=username)
    else:
        error = f'The user {username} does not exists'
        flash(error)
        return redirect(url_for('index'))

