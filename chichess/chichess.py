# -*- coding:utf-8 -*-

from flask import Flask, render_template

app = Flask(__name__, template_folder="./template/") # create the application instance :)


@app.route('/')
def index():
    return render_template("index.html")
    # return "Hello Chess"


if __name__ == '__main__':
    app.run(debug=True)
