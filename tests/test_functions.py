import datetime

from parrot.functions import (
    load_media_images, 
    convert_date, 
    load_dates, 
    load_mentions,
    parse_url,
    get_tweets
)


def test_get_tweets(monkeypatch):

    class MockResponse:
        def __init__(self, status_code):
            self.status_code = status_code

        def json(*args, **kwargs):
            return 'json response'

    class MockRequest:
        
        def get(self, url, headers):
            if 'good token' in headers['Authorization']:
                return MockResponse(200)
            else:
                return MockResponse(403)

    monkeypatch.setattr('parrot.functions.requests', MockRequest())

    assert get_tweets('username','good token') == 'json response'
    assert get_tweets('username', 'wrong token') == {}


def test_parse_url():
    url = 'https://t.co/url'
    string = f'123 {url} 1234'
    assert url == parse_url(string)


def test_load_media_images():
    tweets = {
        'meta': {
            'result_count': 0
        }
    }
    assert load_media_images(tweets) == tweets

    tweets = {
        'meta': {
            'result_count': 1
        },
        'data': [
            {
                'attachments': {
                    'media_keys': ['1', '2']
                }
            },
        ],  
        'includes': {
            'media': [
                {
                    'media_key': '1',
                },
                {
                    'media_key': '2',
                },
            ],
        },
    }
    assert 'media' in load_media_images(tweets)['data'][0]['attachments'].keys()
    assert len(load_media_images(tweets)['data'][0]['attachments']['media']) == 2


def test_load_dates():
    tweets = {
        'meta': {
            'result_count': 0
        }
    }
    assert load_dates(tweets) == tweets
    tweets = {
        'meta': {
            'result_count': 1
        },
        'data': [
            {
                'created_at': '2022-06-01T15:24:24.000Z'
            }
        ]
    }
    assert load_dates(tweets)['data'][0]['created_at'] == datetime.datetime(2022, 6, 1, 15, 24)



def test_convert_date():
    twitter_date = '2022-06-01T15:24:24.000Z'
    assert convert_date(twitter_date) == datetime.datetime(2022, 6, 1, 15, 24)
