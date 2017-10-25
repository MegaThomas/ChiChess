#!/usr/bin/python
# -*- coding: utf-8 -*-

import tornado.ioloop
import tornado.web
import tornado.websocket
from tornado.options import options
import signal
import logging
import os
import json
import re
from Chess import Chess
from jinja2 import Environment, FileSystemLoader
import uuid

is_closing = False


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


class WebSocketMessage(object):
    def __init__(self, type, body=None):
        """Constructor for WebSocketMessage"""
        self.message = {
            "type": type,
            "body": body
        }

    def dumps(self):
        return json.dumps(self.message)


class Application(tornado.web.Application):
    """Main application"""

    def __init__(self):
        """Constructor for Application"""
        handlers = [
            (r"/", MainHandler),
            (r"/current/sp-(\d\d)", CurPosHandler),
            (r"/restart", RestartHandler),
            (r"/websocket", WebSocketHandler)
        ]

        settings = {
            "static_path": os.path.join(os.path.dirname(__file__), "static"),
            "debug": True,
        }

        self.code = {
            "player0": "000",
            "player1": "111"
        }

        self.websocketPool = list()
        self.chess = Chess()
        self.player0 = None
        self.player1 = None
        self.spin_lock = 0
        self.template_file = "index.html"
        self.template_loader = FileSystemLoader(os.path.join(os.path.dirname(os.path.abspath(__file__)), "template"))
        self.template_env = Environment(loader=self.template_loader)
        self.template = self.template_env.get_template(self.template_file)

        super(Application, self).__init__(handlers=handlers, **settings)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.application.template = self.application.template_env.get_template(self.application.template_file)
        html_output = self.application.template.render()
        self.write(html_output)


class CurPosHandler(tornado.web.RequestHandler):
    def get(self, pos_id):
        y = int(pos_id[-2])
        x = int(pos_id[-1])
        self.write(self.application.chess.hanzi[self.application.chess.board["grid"][y][x][0]])


class RestartHandler(tornado.web.RequestHandler):
    def get(self):
        self.application.chess.restart()
        self.write(json.dumps(self.application.chess.board["list"]))


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        logging.info("WebSocket opened")
        self.application.websocketPool.append(self)
        self.write_message(WebSocketMessage("move", self.application.chess.board["list"]).dumps())

    def on_message(self, message):
        print(message)
        if message[0:5] == "/move":
            if self.application.spin_lock == 0:
                if self is not self.application.player0:
                    self.write_message(WebSocketMessage("move", "illegal").dumps())
                    return
                else:
                    self.application.spin_lock = 1
            elif self.application.spin_lock == 1:
                if self is not self.application.player1:
                    self.write_message(WebSocketMessage("move", "illegal").dumps())
                    return
                else:
                    self.application.spin_lock = 0
            m = re.match(r"/move\?o=(\d\d)&n=(\d\d)", message)
            old, new = m.group(1, 2)
            y_old = int(old[0])
            x_old = int(old[1])
            y_new = int(new[0])
            x_new = int(new[1])
            eaten = self.application.chess.move(x_old, y_old, x_new, y_new)
            if eaten is None:
                self.write_message(WebSocketMessage("move","illegal").dumps())
            else:
                situation = WebSocketMessage("move", self.application.chess.board["list"]).dumps()
                for ws in self.application.websocketPool:
                        ws.ws_connection.write_message(situation)
        elif message[0:11] == "/validation":
            m = re.match(r"/validation\?code=(.*)", message)
            code = m.group(1)
            if code == self.application.code["player0"]:
                self.application.player0 = self
                self.write_message(WebSocketMessage("validation", "player0").dumps())
            elif code == self.application.code["player1"]:
                self.application.player1 = self
                self.write_message(WebSocketMessage("validation", "player1").dumps())
            else:
                self.write_message(WebSocketMessage("validation", "unvalid").dumps())

    def on_close(self):
        if self in self.application.websocketPool:
            self.application.websocketPool.remove(self)
        logging.info("WebSocket closed")


application = Application()

if __name__ == "__main__":
    options.parse_command_line()
    signal.signal(signal.SIGINT, signal_handler)
    application.listen(5000)
    tornado.ioloop.PeriodicCallback(try_exit, 100).start()
    tornado.ioloop.IOLoop.instance().start()
