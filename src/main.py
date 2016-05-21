import argparse
from flask import Flask
from flask import render_template
app = Flask(__name__)


# ----------------------------------------------------------------------------

@app.route("/")
def hello():
    return render_template('root.html', value=1)

# ----------------------------------------------------------------------------


def main(mode, port):
    app.run()

# ----------------------------------------------------------------------------


def parse_mode(value):
    if value != 'client' and value != 'server':
        raise argparse.ArgumentTypeError('mode must be "client" or "server"')


def parse_port(value):
    number = int(value)
    if number < 1024 or number >= 65535:
        raise argparse.ArgumentTypeError('port number must be greater than 1024 and less than 65535')


# ----------------------------------------------------------------------------

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('mode',
                        type=parse_mode,
                        nargs=1,
                        help='Mode. Either "client" or "server"')

    parser.add_argument('--port',
                        type=parse_port,
                        help='Tcp port number')

    args = parser.parse_args()

    main(args.mode[0], port=args.port)
