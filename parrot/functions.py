import asyncio

import aiohttp
import requests, datetime

from flask import url_for



def load_tweet_text(tweets):
    tweets = load_media_images(tweets)
    tweets = load_dates(tweets)
    tweets = load_mentions(tweets)
    tweets = load_br(tweets)
    tweets = asyncio.run(load_urls(tweets))
    return tweets


def get_tweets(username, bearer_token, next_token= ''):
    """
    Makes a request to the tweeter API and retrieves a json response
    """
    url = f'https://api.twitter.com/2/tweets/search/recent?query=from:{username}&expansions=attachments.media_keys,entities.mentions.username&media.fields=type,url,preview_image_url&tweet.fields=created_at'
    if next_token:
        url += '&next_token=' + next_token
    headers = {
        'Authorization' : f'Bearer {bearer_token}'
    }
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        return r.json()
    else:
        return {}


def load_media_images(tweets):
    """
    Load media information from the tweeter API response to inside the 
    'data' dictionnary fo easy access in the template.
    """
    if tweets['meta']['result_count'] == 0:
        return tweets
    for tweet in tweets['data']:
        if 'attachments' in tweet.keys():
            media = [
                media for media in tweets['includes']['media'] 
                if media['media_key'] in tweet['attachments']['media_keys']
            ]
            tweet['attachments']['media'] = media
    return tweets


def load_dates(tweets):
    if tweets['meta']['result_count'] == 0:
        return tweets
    for tweet in tweets['data']:
        tweet['created_at'] = convert_date(tweet['created_at'])
    return tweets


def load_br(tweets):
    if tweets['meta']['result_count'] == 0:
        return tweets
    for tweet in tweets['data']:
        tweet['text'] = tweet['text'].replace('\n', '<br>')
    return tweets   


def convert_date(twitter_date):
    return datetime.datetime.strptime(twitter_date[:16], '%Y-%m-%dT%H:%M')


def load_mentions(tweets):
    if tweets['meta']['result_count'] == 0:
        return tweets
    for tweet in tweets['data']:
        if 'entities' in tweet.keys():
            new_text = ''
            cursor = 0
            text = tweet['text']
            for i, mention in enumerate(tweet['entities']['mentions']):
                start = mention['start']
                end = mention['end']
                new_text += text[cursor:start]
                username = mention['username']
                username_hyperlink = f"<a href=\"{url_for('list_tweets', username=username)}\">@{username}</a>" 
                new_text += username_hyperlink
                if i == len(tweet['entities']['mentions']) - 1:
                    new_text += text[end:]
                else:
                    cursor = end
            tweet['text'] = new_text
    return tweets


async def load_urls(tweets):

    async def resolve_short_url(session, short_url):
        async with session.head(short_url) as resp:
            url = resp.headers['location']
            if not url.startswith('https://twitter.com'):
                url_showname = url if len(url) < 50 else f'{url[:47]}...'
                return f'<a href="{url}">{url_showname}</a>'
            else:
                return ''

    async with aiohttp.ClientSession() as session:
        if tweets['meta']['result_count'] == 0:
            return tweets
        for tweet in tweets['data']:
                while parse_url(tweet['text']):
                    short_url = parse_url(tweet['text'])
                    if short_url.endswith('…'):
                        tweet['text'] = tweet['text'].replace(short_url, '')
                    else:
                        tweet['text'] = tweet['text'].replace(short_url, await resolve_short_url(session, short_url))
    
    return tweets       


def parse_url(string):
    start = string.find('https://t.co')
    if string.find(' ',start) >= 0 and string.find('<br>',start) >= 0:
        end = min(string.find(' ',start), string.find('<br>',start))
    elif string.find(' ',start) >= 0:
        end = string.find(' ',start)
    elif string.find('<br>',start) >= 0:
        end = string.find('<br>',start)
    else:
        end = len(string)
    if start >= 0:
        if end >= 0:
            return string[start:end] 
        else:
            return string [start:]
    else:
        return ''