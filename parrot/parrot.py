from os import environ

from flask import Flask, render_template, request, redirect, url_for, flash

from utils.functions import get_tweets, load_media_images, load_dates

app = Flask(__name__)
app.config.from_mapping(
    SECRET_KEY=environ.get('SECRET_KEY'),
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
    tweets = get_tweets(username, next_token=next_token)
    if tweets:
        tweets = load_media_images(tweets)
        tweets = load_dates(tweets)
        return render_template('parrot/index.html', tweets=tweets, username=username)
    else:
        error = f'The user {username} does not exists'
        flash(error)
        return redirect(url_for('index'))

