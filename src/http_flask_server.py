from flask import Flask
from flask import render_template
app = Flask(__name__)

# from player import Player

# Player is the database accessor. It is meant to hide the calls to mongodb.
# player_1 = Player("Player1")
# player_2 = Player("Player2")
# ----------------------------------------------------------------------------

@app.route("/")
def hello():
    # We can then pull data out of the database by using the Player object.
    # data = player_1.get_speed()

    return render_template('root.html', value=1)

# ----------------------------------------------------------------------------


def main(mode, port):
    # start opens up the database - not the best name really.
    # player_2.start()
    # player_1.start()

    app.run()


if __name__ == '__main__':
	main()