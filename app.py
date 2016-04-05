from bs4 import BeautifulSoup
from flask import json, Response
from flask.ext.api import FlaskAPI
import requests

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

    return Response(json.dumps(feeds),  mimetype='application/json')

if __name__ == '__main__':
    #app.run(debug=True)
    app.run(host='0.0.0.0')
