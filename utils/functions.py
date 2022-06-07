import requests, os, datetime



# set BEARER_TOKEN in then environment variables
BEARER_TOKEN = os.environ.get("BEARER_TOKEN")


def get_tweets(username, next_token= ''):
    """
    Makes a request to the tweeter API and retrieves a json response
    """
    url = f'https://api.twitter.com/2/tweets/search/recent?query=from:{username}&expansions=attachments.media_keys&media.fields=type,url,preview_image_url&tweet.fields=created_at'
    if next_token:
        url += '&next_token=' + next_token
    headers = {
        'Authorization' : f'Bearer {BEARER_TOKEN}'
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


def convert_date(twitter_date):
    return datetime.datetime.strptime(twitter_date[:16], '%Y-%m-%dT%H:%M')

