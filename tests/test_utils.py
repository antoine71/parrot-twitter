import datetime

from parrot.functions import (
    load_media_images, 
    convert_date, 
    load_dates, 
    load_mentions,
    parse_url
)

def test_parse_url():
    url = 'https://url.com'
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
