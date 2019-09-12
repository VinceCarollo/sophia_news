import os

from flask import Flask
from bs4 import BeautifulSoup
import requests


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/good_news')
    def hello():
        headlines = []
        def fetch_news():
            source = requests.get('https://www.reddit.com/r/UpliftingNews/').text
            soup = BeautifulSoup(source, 'html.parser')
            links = soup.select('div > a')
            for headline in soup.find_all('h3'):
                headlines.append({ 'headline' : headline.text, 'link': 'https://www.reddit.com/r/UpliftingNews/' })

        while not headlines:
            fetch_news()

        return { 'headlines' : headlines }

    return app
