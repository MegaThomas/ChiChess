#!/usr/bin/python
# -*- coding: utf-8 -*-

import tornado.ioloop
import tornado.web
import tornado.websocket
import signal
import logging
import os
import json
import re
from Chess import Chess
from tornado.options import options

is_closing = False
chess = Chess()

def signal_handler(signum, frame):
    global is_closing
    logging.info('exiting...')
    is_closing = True

def try_exit(): 
    global is_closing
    if is_closing:
        # clean up here
        tornado.ioloop.IOLoop.instance().stop()
        logging.info('exit success')

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("./template/index.html")

class CurPosHandler(tornado.web.RequestHandler):
    def get(self, pos_id):
        global chess
        y = int(pos_id[-2])
        x = int(pos_id[-1])
        self.write(chess.hanzi[chess.board["grid"][y][x][0]])

class RestartHandler(tornado.web.RequestHandler):
    def get(self):
        global chess
        chess.restart()
        self.write(json.dumps(chess.board["list"]))

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        logging.info("WebSocket opened")
        self.write_message(json.dumps(chess.board["list"]))

    def on_message(self, message):
        print(message)
        m = re.match(r"/move\?o=(\d\d)&n=(\d\d)", message)
        old, new = m.group(1, 2)
        y_old = int(old[0])
        x_old = int(old[1])
        y_new = int(new[0])
        x_new = int(new[1])
        eaten = chess.move(x_old, y_old, x_new, y_new)
        if eaten == None:
            self.write_message("illegal")
        else:
            self.write_message(json.dumps(chess.board["list"]))

    def on_close(self):
        logging.info("WebSocket closed")

settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static")
}

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/current/sp-(\d\d)", CurPosHandler),
    (r"/restart", RestartHandler),
    (r"/websocket", WebSocketHandler)
], debug=True, **settings)

if __name__ == "__main__":
    tornado.options.parse_command_line()
    signal.signal(signal.SIGINT, signal_handler)
    application.listen(5000)
    tornado.ioloop.PeriodicCallback(try_exit, 100).start() 
    tornado.ioloop.IOLoop.instance().start()