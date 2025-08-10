from flask import Flask, request
import cloudscraper

app = Flask(__name__)

scraper = cloudscraper.create_scraper()

@app.route('/<path:url>', methods=['GET', 'POST'])
def proxy(url):
    full_url = f'https://backend.wplace.live/{url}'
    if request.method == 'POST':
        response = scraper.post(full_url, json=request.json, headers=request.headers)
    else:
        response = scraper.get(full_url, headers=request.headers)
    return response.text, response.status_code, response.headers.items()

if __name__ == '__main__':
    app.run(port=5000)