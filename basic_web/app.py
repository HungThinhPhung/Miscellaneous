import logging
import os

from flask import Flask, render_template

app = Flask(__name__)


@app.route("/", methods=['GET'])
def render():
    return render_template('index.html')


if __name__ == "__main__":
    port = int(os.getenv('PORT', 8111))
    logging.warning("Starting app on port %d" % port)
    app.config['JSON_SORT_KEYS'] = False
    app.run(debug=True, port=port, host='0.0.0.0', threaded=True)
