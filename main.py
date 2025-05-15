"""Main module: starting app."""

import os

from dotenv import load_dotenv
from flask import Flask, render_template, request

import similarity

app = Flask(__name__, template_folder="Templates")


@app.route("/", methods=["GET", "POST"])
def main_page() -> str:
    """Render and return main page."""
    return render_template("index.html")


@app.route("/report", methods=["POST", "GET"])
def report_page() -> str:
    """Render and return report page."""
    result = request.form["text"]
    return render_template("report.html") + similarity.return_table(
        similarity.report(str(result)),
    )


if __name__ == "__main__":
    # Loading consts from .env
    load_dotenv()

    IS_DEBUG = os.getenv("DEBUG").lower() == "true"
    HOST = os.getenv("HOST")
    PORT = os.getenv("PORT")

    # Starting flask app
    app.run(debug=IS_DEBUG, host=HOST, port=PORT)
