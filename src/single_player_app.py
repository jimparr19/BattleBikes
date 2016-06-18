from flask import Flask, Response, stream_with_context

import random
import json
import time

app = Flask(__name__)

def stream_template(template_name, **context):
    app.update_template_context(context)
    t = app.jinja_env.get_template(template_name)
    rv = t.stream(context)
    return rv

@app.route('/stream')
def index():
    def g():
        d = [dict(x=0, y=0)]
        for i in range(1,500):
            time.sleep(random.random())  # an artificial random delay
            d.append(dict(x=i, y=random.random()))
            yield json.dumps(d)
    return Response(stream_template('single_player.html', data=g()))

if __name__ == '__main__':
    app.run(port=9000, debug=True)
