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


if __name__ == '__main__':
	main()