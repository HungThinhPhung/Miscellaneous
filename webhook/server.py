import logging

from flask import Flask, request, jsonify

from webhook.service import register_service, trigger_service

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)


@app.route('/register', methods=['POST'])
def register():
    data = request.json
    register_service(data)
    return jsonify({"message": "Done"})


@app.route('/', methods=['GET'])
def trigger():
    bot_id = request.args.get('bot_id')
    data = trigger_service(bot_id)
    return jsonify(data)


if __name__ == '__main__':
    app.run(host='localhost', port=9000)
