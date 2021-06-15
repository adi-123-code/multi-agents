# -*- coding:utf-8 -*-
# 小方块的类
class Cell(object):

    def __init__(self, position, last=None, distance=0, marked=False, passable=True):
        if last is None:
            last = [-1, -1]
        self._position = position
        self._last_position = last
        self._distance = distance
        self._marked = marked
        self._passable = passable

    @property
    def position(self):
        return self._position

    @property
    def last_position(self):
        return self._last_position

    @property
    def distance(self):
        return self._distance

    @property
    def marked(self):
        return self._marked

    @property
    def passable(self):
        return self._passable

    @last_position.setter
    def last_position(self, value):
        self._last_position = value

    @distance.setter
    def distance(self, value):
        self._distance = value

    @marked.setter
    def marked(self, value):
        self._marked = value

    @passable.setter
    def passable(self, value):
        self._passable = value
