from flask import Flask, request
import cloudscraper
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

scraper = cloudscraper.create_scraper()

@app.route('/<path:url>', methods=['GET', 'POST', 'OPTIONS'])
def proxy(url):
    full_url = f'https://backend.wplace.live/{url}'
    headers = dict(request.headers)
    if 'X-Cookie' in headers:
        headers['Cookie'] = headers.pop('X-Cookie')
    if request.method == 'POST':
        data = request.get_data(as_text=True)
        try:
            json_data = json.loads(data)
        except json.JSONDecodeError:
            json_data = None
        response = scraper.post(full_url, json=json_data, headers=headers)
    else:
        response = scraper.get(full_url, headers=headers)
    return response.text, response.status_code, response.headers.items()

if __name__ == '__main__':
    app.run(port=5000)