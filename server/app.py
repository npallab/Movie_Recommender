import sys
from pathlib import Path

import flask

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from server.main import recommend_movies
from src.logger import setup_logger

logger = setup_logger("movie_recommender", level=flask.logging.DEBUG)

app = flask.Flask(__name__, static_folder="../static", template_folder="../static")


@app.route("/")
def index():
    return flask.send_from_directory(app.static_folder, "index.html")


@app.route("/api/recommend", methods=["POST"])
def get_recommendations():
    data = flask.request.get_json()
    movie_name = data.get("movie_name", "")
    top_n = data.get("top_n", 5)
    logger.debug(f"Received request for recommendations for '{movie_name}' with top_n={top_n}")
    recommendations = recommend_movies(movie_name, top_n)
    logger.debug(f"Returning recommendations: {recommendations}")
    return flask.jsonify(recommendations)


if __name__ == "__main__":
    app.run(debug=True)