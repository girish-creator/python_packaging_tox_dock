import time
from flask import Flask
import redis

app = Flask('app')
cache = redis.Redis(host='redis', port=6379)


def get_hit_counter():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as cexr:
            if retries == 0:
                raise cexr
            retries -= 1
            time.sleep(0.5)


@app.route('/')
def hello():
    count = get_hit_counter()
    return 'Hello World. I have been hit {} times.\n'.format(count)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
