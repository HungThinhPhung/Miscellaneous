import logging

from flask import Flask, jsonify

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)


@app.route('/', methods=['POST'])
def watch():
    logging.info("OK")
    return jsonify({})


if __name__ == '__main__':
    app.run(host='localhost', port=9001)
