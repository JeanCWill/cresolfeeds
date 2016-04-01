from bs4 import BeautifulSoup
from flask import request, url_for
from flask.ext.api import FlaskAPI, status, exceptions
import requests
import json

app = FlaskAPI(__name__)

@app.route('/feeds')
def feeds_list():
    feeds = []
    page = requests.get('http://www.cresol.com.br/site/rss/news2.php?l=20').text
    soup = BeautifulSoup(page, "html.parser")

    for item in soup.find_all('item'):
        feed = {}
        feed['id'] = item.id.string
        feed['title'] = item.title.string
        feed['content'] = str(item.content).replace('<content>', '').replace('</content>', '')
        feed['description'] = item.description.string
        feed['image'] = item.image.string
        feed['link'] = item.link.string
        if item.video is not None:
            feed['video'] = item.video.string
        feeds.append(feed)

    return json.dumps(feeds, ensure_ascii=False)

if __name__ == '__main__':
    app.run(debug=True)
