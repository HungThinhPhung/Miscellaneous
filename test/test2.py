import os

import phthinh.util as util
from flask import Flask

app = Flask(__name__)


@app.route('/', methods=["GET"])
@util.web_service.format_api_result
def example_func():
    return {'b':1, 'a':2}


if __name__ == '__main__':
    port = int(os.getenv("PORT", 17000))
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.config["JSON_SORT_KEYS"] = False
    app.config["JSON_AS_ASCII"] = False
    # regis_consul()
    app.run(debug=True, port=port, host="0.0.0.0", threaded=True)
