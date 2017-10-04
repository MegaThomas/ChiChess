# -*- coding:utf-8 -*-

from __future__ import print_function
import itertools
import string
import re


class Chess(object):
    """Chess Board"""
    bcolors = {
        "LBLUE": "\033[1;34m",
        "LGREEN": "\033[1;32m",
        "LCYAN": "\033[1;36m",
        "LRED": "\033[1;31m",
        "LPURPLE": "\033[1;35m",
        "BLACK": "\033[0;30m",
        "BLUE": "\033[0;34m",
        "GREEN": "\033[0;32m",
        "CYAN": "\033[0;36m",
        "RED": "\033[0;31m",
        "PURPLE": "\033[0;35m",
        "BROWN": "\033[0;33m",
        "YELLOW": "\033[1;33m",
        "WHITE": "\033[1;37m",
        "ENDC": "\033[0m"
    }

    hanzi = {
        'R': bcolors["LRED"] + u'俥' + bcolors["ENDC"],
        'H': bcolors["LRED"] + u'傌' + bcolors["ENDC"],
        'E': bcolors["LRED"] + u'相' + bcolors["ENDC"],
        'A': bcolors["LRED"] + u'仕' + bcolors["ENDC"],
        'G': bcolors["LRED"] + u'帥' + bcolors["ENDC"],
        'C': bcolors["LRED"] + u'炮' + bcolors["ENDC"],
        'S': bcolors["LRED"] + u'兵' + bcolors["ENDC"],
        'r': u'車',
        'h': u'馬',
        'e': u'象',
        'a': u'士',
        'g': u'將',
        'c': u'砲',
        's': u'卒',
    }

    def __init__(self):
        super(Chess, self).__init__()
        self.board = {
            "list": {},
            "grid": []
        }
        self.cmd_reg = re.compile(r"^\s*([a-i])\s*(0?(?:[1-9]|10))\s*([a-i])\s*(0?(?:[1-9]|10))\s*$")
        self.init_board()
        self.eaten_list = []

    def init_board(self):
        self.board["list"] = {
            'R0': [0, 0],
            'H0': [0, 1],
            'E0': [0, 2],
            'A0': [0, 3],
            'G':  [0, 4],
            'A1': [0, 5],
            'E1': [0, 6],
            'H1': [0, 7],
            'R1': [0, 8],
            'C0': [2, 1],
            'C1': [2, 7],
            'S0': [3, 0],
            'S1': [3, 2],
            'S2': [3, 4],
            'S3': [3, 6],
            'S4': [3, 8],
            'r0': [9, 0],
            'h0': [9, 1],
            'e0': [9, 2],
            'a0': [9, 3],
            'g':  [9, 4],
            'a1': [9, 5],
            'e1': [9, 6],
            'h1': [9, 7],
            'r1': [9, 8],
            'c0': [7, 1],
            'c1': [7, 7],
            's0': [6, 0],
            's1': [6, 2],
            's2': [6, 4],
            's3': [6, 6],
            's4': [6, 8],
        }
        self.board["grid"] = [['0'] * 9 for i in range(10)]
        for pid, pos in self.board["list"].items():
            self.board["grid"][pos[0]][pos[1]] = pid

    def display(self):
        text = ["{:3}".format(str(10-idx))+''.join([self.hanzi[x[0]] if x != '0' else u'┼─' for x in row])
                +' '+str(10-idx) for idx, row in enumerate(self.board["grid"][::-1])]
        text[4] = '6  '+u'┴─'*9+' 6'
        text[5] = '5  '+u'┬─'*9+' 5'
        file_tag = "   a b c d e f g h i"
        text = [file_tag] + text + [file_tag]
        for row in text:
            print(row)

    def __move(self, x_old, y_old, x_new, y_new):
        if self.islegal(x_old, y_old, x_new, y_new):
            eaten = self.board["grid"][y_new][x_new]
            piece = self.board["grid"][y_old][x_old]
            self.board["grid"][y_new][x_new] = piece
            self.board["grid"][y_old][x_old] = '0'
            self.board["list"][piece] = [y_new, x_new]
            if eaten != '0':
                self.board["list"][eaten] = [-1, -1]
            return eaten
        else:
            print("WTF: illegal move {}{} {}{}".format(x_old, y_old, x_new, y_new))

    def move(self, command):
        m = re.match(self.cmd_reg, command)
        x_old, y_old, x_new, y_new = m.group(1, 2, 3, 4)
        x_old = ord(x_old) - ord('a')
        x_new = ord(x_new) - ord('a')
        y_old = int(y_old) - 1
        y_new = int(y_new) - 1
        eaten = self.__move(x_old, y_old, x_new, y_new)
        self.eaten_list.append(eaten)

    def islegal(self, x_old, y_old, x_new, y_new):
        piece = self.board["grid"][y_old][x_old]
        if piece == '0':
            print("ERR: move void")
            return False
        elif self.board["grid"][y_new][x_new][1] == piece[1]:
            print("ERR: capture self piece")
            return False
        else:
            p = piece[0].lower()
            side = piece[1]                                      # 0 for red, 1 for black
            dx = abs(x_new - x_old)
            sx = self.__sign(x_new - x_old)
            dy = abs(y_new - y_old)
            sy = self.__sign(y_new - y_old)
            if p == 'r':
                if dx == 0 and dy != 0:
                    if all(x == '0' for x in [row[x_old] for row in self.board["grid"][y_old+sy:y_new:sy]]):
                        return True
                    else:
                        return False
                elif dy == 0 and dx != 0:
                    if all(x == '0' for x in self.board["grid"][y_old][x_old+sx:x_new:sx]):
                        return True
                    else:
                        return False
                else:
                    return False
            elif p == 'h':
                if dx == 1 and dy == 2:
                    if self.board["grid"][y_old+sy][x_old] == '0':  # hobbling the horse's leg
                        return True
                    else:
                        return False
                elif dx == 2 and dy == 1:
                    if self.board["grid"][y_old][x_old+sx] == '0':  # hobbling the horse's leg
                        return True
                    else:
                        return False
                else:
                    return False
            elif p == 'e':
                if dx == 2 and dy == 2:
                    if self.board["grid"][y_old+sx][x_old+sx] == '0':  # blocking the elephant's eye
                        return True
                    else:
                        return False
                else:
                    return False
            elif p == 'a':
                if dx == 1 and dy == 1:
                    if side:
                        if (x_new, y_new) in [(3,9), (3,7), (4,8), (5,9), (5,7)]:
                            return True
                        else:
                            return False
                    else:
                        if (x_new, y_new) in [(3,0), (3,2), (4,1), (5,0), (5,2)]:
                            return True
                        else:
                            return False
                else:
                    return False
            elif p == 'g':
                if dx + dy == 1:
                    if side:
                        if 3 <= x_new <= 5 and 7 <= y_new <= 9:
                            return True
                        else:
                            return False
                    else:
                        if 3 <= x_new <= 5 and 0 <= y_new <= 2:
                            return True
                        else:
                            return False
                else:
                    return False
            elif p == 'c':
                if dx == 0 and dy != 0:
                    if sum(x != '0' for x in [row[x_old] for row in self.board["grid"][y_old+sy:y_new:sy]]) <= 1:
                        return True
                    else:
                        return False
                elif dy == 0 and dx != 0:
                    if sum(x == '0' for x in self.board["grid"][y_old][x_old+sx:x_new:sx]) <= 1:
                        return True
                    else:
                        return False
                else:
                    return False
            elif p == 's':
                if side:
                    if sy == -1 and dx+dy == 1:
                        if y_old <= 4:
                            return True
                        elif dx == 0:
                            return True
                        else:
                            return False
                    else:
                        return False
                else:
                    if sy == 1 and dx+dy == 1:
                        if y_old >= 5:
                            return True
                        elif dx == 0:
                            return True
                        else:
                            return False
                    else:
                        return False
            else:
                print("WTF: impossible")
                return False

    @staticmethod
    def __sign(x):
        return (1, -1)[x < 0]


if __name__ == '__main__':
    chess = Chess()
    chess.move("a1 a09")
    chess.move("a1b2")
    chess.move("a1 e1")
    chess.move("a1 a3")
    chess.move("b1 b2")
    chess.move("b1 d2")
    chess.move("b1 c3")
    chess.move("c3 b5")
    chess.display()
