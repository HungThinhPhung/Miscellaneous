from functools import wraps

import requests
from pymongo import MongoClient

db_client = MongoClient(host='localhost', port=27017)
webhook_collection = db_client['chatt-store']['webhook']


class Webhook:
    def __init__(self, bot_id: int, watch_url: str, authentication: dict, header: dict, body: dict,
                 method: str = 'POST'):
        self.bot_id = bot_id
        self.watch_url = watch_url
        self.authentication = authentication
        self.header = header
        self.body = body
        self.method = method


class HandleNotification:
    def __init__(self, watch: Webhook, data: dict):
        self.watch = watch
        self.data = data

    def __authentication(self, header, body):
        # Do something base on self.watch.authentication
        authentication = self.watch.authentication
        return header, body

    def __format_header(self):
        return self.watch.header

    def __format_body(self):
        return self.data

    def __send(self, header, body):
        for i in range(5):
            try:
                response = requests.request(self.watch.method, url=self.watch.watch_url, headers=header, json=body,
                                            timeout=3)
            except requests.exceptions.ConnectionError:
                return None
            if response.status_code in [200, 201]:
                return None
            if response.status_code in [400, 500]:
                continue
            return None

    def execute(self):
        header = self.__format_header()
        body = self.__format_body()
        header, body = self.__authentication(header, body)
        self.__send(header, body)


def register(webhook: Webhook):
    webhook_collection.insert_one(webhook.__dict__)


def register_service(data: dict):
    bot_id = data.get('bot_id', 1)
    watch_url = data.get('watch_url', '')
    authentication = data.get('authentication', {})
    header = data.get('header', {})
    body = data.get('body', {})
    method = data.get('method', 'POST')
    wh = Webhook(bot_id, watch_url, authentication, header, body, method)
    register(wh)


def webhook(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        send_notification(int(args[0]), result)
        return result

    return wrapper


def send_notification(bot_id, data):
    watches = list(webhook_collection.find({'bot_id': bot_id}))
    for watch in watches:
        del watch['_id']
        watch = Webhook(**watch)
        handle = HandleNotification(watch, data)
        handle.execute()
    print()


@webhook
def trigger_service(bot_id):
    return {"data": bot_id}
