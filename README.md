# Parrot, a lightweight Twitter browser

Parrot is a lightweight application that allows unlimited anonymous browsing through Twitter.

## Status

The project is under development.

## Live preview

Check the live project on [https://parrot.arebillard.fr](https://parrot.arebillard.fr)


## Technical information

The project uses the following technologies:

* [Python 3](https://www.python.org) as the main programming language
* [Flask](https://flask.palletsprojects.com) as back-end framework
* [Pytest](https://pytest.org) and [Coverage](https://pypi.org/project/coverage/) for testing
* A [Startbootstrap theme](https://startbootstrap.com) as front-end

## Local Deployment

1. Clone this repository, navigate to the root folder of the repository, create and activate a virtual environment, install project dependencies :

```
git clone https://github.com/antoine71/basic_blog.git
cd basic_blog
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

2. in the subfolder `parrot`, create a file names `.env` and populate the following environment variables information :

```shell
touch parrot/.env
```

```
# parrot/.env

SECRET_KEY=<your secretvkey>
BEARER_TOKEN=<your Twitter API V2 bearer token>
```

3. 
From the root directory, run the local server
```
flask run
```

## Testing

The test suite can be run using the following command:

```
pytest
```

The coverage report can be generated using the following command:

```
coverage run -m pytest
```

The html report can be generated with the following command

```
coverage html
```

The report will be created in the subfolder `htmlcov/`.

## Todo

Add hyperlink to usernames in the tweet feed
