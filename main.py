from flask import Flask, render_template, request, redirect, url_for
from yut import search_youtube
from player_main import Player

app = Flask(__name__)
player = Player()


@app.route("/")
async def index():
    term = request.args.get("term")
    results = []
    if term is not None:
        results = await search_youtube(term)
    else:
        term = ""
    return render_template("index.html",
                           term=term,
                           results=results
                           )


@app.route("/play")
def play():
    vid = request.args.get("url")

    player.play(vid)

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run("0.0.0.0", 5000)
