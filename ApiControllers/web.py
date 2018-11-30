import codecs
from os.path import join as join_paths

import markdown as markdown
from flask import render_template, Markup

from ApiControllers.exceptions import *


def decorate_web_app(flask_app: Flask):
    @flask_app.route("/")
    def home():
        # Receives Token and Message in POST body
        input_file = codecs.open(join_paths("docs", "docs.md"), mode="r",
                                 encoding="utf-8")
        docs_text = input_file.read()
        input_file.close()
        markdown_docs = Markup(markdown.markdown(docs_text))

        return render_template("root.html", markdown_docs=markdown_docs)

    @flask_app.route("/dashboard")
    def dashboard():
        # Receives Token and Message in POST body
        return render_template("dashboard.html")
