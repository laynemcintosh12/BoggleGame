from boggle import Boggle
from flask import Flask, session, render_template, request, jsonify


app = Flask(__name__)
app.config['SECRET_KEY'] = "secre233t"

boggle_game = Boggle()


@app.route('/')
def get_home_page():
    board = boggle_game.make_board()
    session['board'] = board
    highscore = session.get("highscore", 0)
    numPlays = session.get("numPlays", 0)
    return render_template('base.html', board=board, highscore=highscore, numPlays=numPlays)

@app.route('/check-guess')
def check_guess():
    guess = request.args["guess"]
    board = session["board"]
    response = boggle_game.check_valid_word(board, guess)
    return jsonify({'result': response})


@app.route("/post-score", methods=["POST"])
def post_score():
    """Receive score, update nplays, update high score if appropriate."""

    score = request.json["score"]
    highscore = session.get("highscore", 0)
    numPlays = session.get("numPlays", 0)
    session['numPlays'] = numPlays + 1
    session['highscore'] = max(score, highscore)
    return jsonify(newHigh=score > highscore)