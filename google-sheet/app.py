from flask import Flask, render_template, request
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)


@app.route('/', methods=['GET'])
def index():
    return {"data": "Hi there"}


@app.route('/google7a66ddd14b9c82b4.html', methods=['GET'])
def verify():
    return render_template('index.html')


@app.route('/watch', methods=['POST'])
def update():
    logging.info("Data is changed!!!")
    return {}


if __name__ == '__main__':
    app.run(host='localhost', port=8080)
