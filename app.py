import logging

from flask import Flask, request, jsonify, redirect

from middleware import setup_request_logger
from shortener import Shortener
import ecs_logging

app = Flask(__name__)
shortener = Shortener()

setup_request_logger(app)
logger = logging.getLogger('user_requests')
logger.setLevel(logging.INFO)

handler = logging.StreamHandler()
handler.setFormatter(ecs_logging.StdlibFormatter())
logger.addHandler(handler)


@app.route('/api/url', methods=['PUT'])
def create_short_url():
    """Create a short URL for the given original URL.

    :returns: HTTP 201 Created with a JSON response containing the short URL.
    :raise Exception: If an error occurs during short URL creation, return HTTP 500 with an error message.
    """
    data = request.get_json()
    url = data.get('url')

    try:
        short_code = shortener.create_short_url(url)
        short_url = f"http://127.0.0.1:5000/{short_code}"
        return jsonify({"url": short_url}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/url/<short_code>', methods=['DELETE'])
def delete_short_url(short_code):
    """ Delete the short URL associated with the given short code.

    :param short_code: The short code identifying the short URL to be deleted.
    :return: HTTP 200 OK if deletion is successful.
    :raise ValueError: If the provided short code does not exist, return HTTP 500 with an error message.
    """
    try:
        shortener.delete_short_url(short_code)
        return 'OK', 200
    except ValueError:
        return jsonify({"error": "URL not found"}), 500


@app.route('/<short_code>', methods=['GET', 'POST'])
def redirect_to_original_url(short_code):
    """Provide redirection to original URL according to given short code

    :param short_code: The short code identifying the short URL to be redirected
    """
    redirect_url = shortener.get_redirect_info(short_code)
    if redirect_url is not None:
        return redirect(redirect_url, code=302)
    return jsonify({"error": "URL not found"}), 404


if __name__ == '__main__':
    app.run(debug=True)
