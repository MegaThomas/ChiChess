# -*- coding:utf-8 -*-

from flask import Flask, render_template, g, flash
from Chess import Chess

app = Flask(__name__, template_folder="./template/") # create the application instance :)
app.config.from_object(__name__) # load config from this file , flaskr.py
g_chess = Chess()

# Load default config and override config from an environment variable
app.config.update(dict(
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/current/<pos>')
def current(pos):
    y = int(pos[-2])
    x = int(pos[-1])
    print(x, y)
    if 0 <= x <= 8 and 0 <= y <= 10:
        flash(u"{}{}".format(x, y), 'info')
        return g_chess.hanzi[g_chess.board["grid"][y][x][0]]
    else:
        flash(u"Illegal", 'error')
        return "Err"

if __name__ == '__main__':
    app.run(debug=True)
