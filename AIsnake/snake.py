# -*- coding:utf-8 -*-

import copy
import math

from setting import *
from cell import *
import numpy as np

# 坐标到小方块的映射
cell_map = []
# 一一对应存放每个小方块
for x in range(0, WIDTH, 20):
    r = []
    for y in range(0, HEIGHT, 20):
        cell = Cell([x, y])
        r.append(cell)
    cell_map.append(r)


class Snake(object):
    def __init__(self, body):
        self._body = body
        self._previous_tail = None
        self.alive = True
        self.score = 0
        self.path_cells = []
        self.goal = [0, 0]
        self.cell_map = []
        for position in self._body:
            cell_map[position[0] // 20][position[1] // 20].passable = False

    def get_head(self):
        return self._body[0]

    def get_body(self):
        return self._body

    def get_tail(self):
        return self._body[-1]

    def get_alive(self):
        return self.alive

    def get_score(self):
        return self.score

    def get_previous_tail(self):
        return self._previous_tail

    def remove_tail(self):
        return self._body.pop()

    def move_to_next(self, next_cell):
        next_cell.passable = False
        self._body.insert(0, list(next_cell.position))
        self._previous_tail = self._body.pop()
        cell_map[self._previous_tail[0] // 20][self._previous_tail[1] // 20].passable = True
        self.score -= 1

    def fake_move_to_next(self, next_cell):
        self._body.insert(0, list(next_cell.position))
        self.cell_map[self.get_head()[0] // 20][self.get_head()[1] // 20].passable = False
        self._previous_tail = self._body.pop()
        self.cell_map[self._previous_tail[0] // 20][self._previous_tail[1] // 20].passable = True
        self.score -= 1

    # def back_to_prev(self):
    #     cell_map[self.get_head()[0] // 20][self.get_head()[1] // 20].passable = True
    #     del self._body[0]
    #     self._body.append(self._previous_tail)
    #     cell_map[self._previous_tail[0] // 20][self._previous_tail[1] // 20].passable = False
    #
    # def move_by_direction(self, direction):
    #     # 根据方向，改变坐标
    #     if direction == 'left':
    #         next_cell = cell_map[self._body[0][0] // 20 - 1][self._body[0][1] // 20]
    #         self.move_to_next(next_cell)
    #     if direction == 'right':
    #         next_cell = cell_map[self._body[0][0] // 20 + 1][self._body[0][1] // 20]
    #         self.move_to_next(next_cell)
    #     if direction == 'up':
    #         next_cell = cell_map[self._body[0][0] // 20][self._body[0][1] // 20 - 1]
    #         self.move_to_next(next_cell)
    #     if direction == 'down':
    #         next_cell = cell_map[self._body[0][0] // 20][self._body[0][1] // 20 + 1]
    #         self.move_to_next(next_cell)

    # 排序的比较函数
    def cmp(self, c):
        return c.distance + math.sqrt(pow(self.goal[0] - c.position[0], 2) + pow(self.goal[1] - c.position[1], 2))
        # return c.distance + abs(g_goal[0] - c.position[0])+abs(g_goal[1] - c.position[1])

    # 判断小方块是否在界面中并且可通过
    def is_valid(self, index_x, index_y, fake=False):
        if fake:
            return 0 <= index_x < WIDTH and 0 <= index_y < HEIGHT and self.cell_map[index_x // 20][
                index_y // 20].passable
        else:
            return 0 <= index_x < WIDTH and 0 <= index_y < HEIGHT and cell_map[index_x // 20][index_y // 20].passable

    # 存放路径
    def fill_path(self, goal):
        self.path_cells.clear()
        c = cell_map[goal[0] // 20][goal[1] // 20]
        while c.last_position[0] != -1:
            self.path_cells.append(c)
            c = cell_map[c.last_position[0] // 20][c.last_position[1] // 20]

    def clear_path(self):
        for x1 in range(0, WIDTH // 20):
            for y1 in range(0, HEIGHT // 20):
                cell_map[x1][y1].distance = 0
                cell_map[x1][y1].last_position = [-1, -1]
                cell_map[x1][y1].marked = False
        self.path_cells.clear()

    # 寻路算法
    def find_path(self, goal, fake=False):
        # 清除标记
        self.clear_path()
        self.goal[0] = goal[0]
        self.goal[1] = goal[1]

        # 将初始位置放入cells
        start_cell = cell_map[self.get_head()[0] // 20][self.get_head()[1] // 20]
        cells = [start_cell]
        start_cell.marked = True

        while len(cells) != 0:
            cells.sort(key=self.cmp, reverse=True)
            # 弹出最近的方块作为当前方块
            now_cell = cells.pop()

            # 到达目标
            if now_cell.position[0] == goal[0] and now_cell.position[1] == goal[1]:
                self.fill_path(goal)
                return True

            # 探索四个方向
            for dire in DIRECTION:
                index_x = now_cell.position[0] + dire[0]
                index_y = now_cell.position[1] + dire[1]
                if self.is_valid(index_x, index_y, fake):
                    c = cell_map[index_x // 20][index_y // 20]
                    # 到起点的距离
                    before_distance = 1 + now_cell.distance
                    # 没走过的放入cells
                    if not c.marked:
                        c.marked = True
                        c.last_position[0] = now_cell.position[0]
                        c.last_position[1] = now_cell.position[1]
                        c.distance = before_distance
                        cells.append(c)
                    else:
                        # 现在到起点的距离比之前短，放入cells
                        if before_distance < c.distance:
                            c.last_position[0] = now_cell.position[0]
                            c.last_position[1] = now_cell.position[1]
                            c.distance = before_distance
        return False

    # 获取下一步
    def get_next_cell(self, square):
        can_find_path = self.find_path(square)
        can_find_tail = False
        if can_find_path:
            copy_snake = copy.deepcopy(self)
            if len(self.path_cells) == 0:
                self.alive = False
                return
            next_cell = copy.deepcopy(self.path_cells[-1])
            copy_snake.cell_map = copy.deepcopy(cell_map)
            # 复制一条蛇模拟寻路
            while len(self.path_cells) > 0:
                copy_snake.fake_move_to_next(self.path_cells.pop())
            # 得到方块，长度增加
            copy_snake.get_body().append(copy_snake.get_previous_tail())
            # 检查是否能找到蛇尾
            can_find_tail = copy_snake.find_path(copy_snake.get_tail(), True)
            if can_find_tail:
                return next_cell

        if not can_find_path or not can_find_tail:
            distance = 0
            max_distance = 0
            safe_cell = None

            for dire in DIRECTION:
                next_cell_x = self.get_head()[0] + dire[0]
                next_cell_y = self.get_head()[1] + dire[1]
                if self.is_valid(next_cell_x, next_cell_y):
                    next_cell = cell_map[next_cell_x // 20][next_cell_y // 20]
                    safe_cell = copy.deepcopy(next_cell)
                    copy_snake = copy.deepcopy(self)
                    copy_snake.cell_map = copy.deepcopy(cell_map)
                    copy_snake.fake_move_to_next(next_cell)
                    if next_cell_x == square[0] and next_cell_y == square[1]:
                        copy_snake.get_body().append(copy_snake.get_previous_tail())
                    can_find_tail = copy_snake.find_path(copy_snake.get_tail(), True)
                    # 走向最远的方向尝试找到蛇尾
                    if can_find_tail:
                        distance = pow(square[0] - next_cell_x, 2) + pow(square[1] - next_cell_y, 2)
                        if distance > max_distance:
                            max_distance = distance
                            safe_cell = next_cell

            return safe_cell

    # 检查是否到达目标
    def check_eat(self, square_position):
        if self.get_head()[0] == square_position[0] and self.get_head()[1] == square_position[1]:
            # 得到目标，长度增加
            self.get_body().append(self.get_previous_tail())
            cell_map[self._previous_tail[0] // 20][self._previous_tail[1] // 20].passable = False
            self.score += 30
            return True
        return False

    def move(self, square_position):
        next_cell = self.get_next_cell(square_position)
        if next_cell is None:
            self.alive = False
            return
        self.move_to_next(next_cell)

    # 重生
    def relive(self, body):
        for position in self._body:
            cell_map[position[0] // 20][position[1] // 20].passable = True
        self._body = body
        self._previous_tail = None
        self.alive = True
        self.score = 0
        self.path_cells = []
        self.goal = [0, 0]
        self.cell_map = []
        for position in self._body:
            cell_map[position[0] // 20][position[1] // 20].passable = False
