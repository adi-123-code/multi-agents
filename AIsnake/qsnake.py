# -*- coding:utf-8 -*-
import random
from math import sqrt

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

gamma = 0.9
QTable = np.zeros([2916, 4])


def save_QTable():
    np.save('QTable.npy', QTable)


def load_QTable():
    global QTable
    QTable = np.load('QTable.npy')


class QSnake(object):
    def __init__(self, body):
        self._body = body
        self._previous_tail = None
        self._direction = 'R'
        self.pre_distance = 0
        self.alive = True
        self.time = 1000
        self.score = 0
        self.best_score = 0
        self.state = np.zeros(8)
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

    def get_best_score(self):
        return self.best_score

    def get_previous_tail(self):
        return self._previous_tail

    def move_to_next(self, next_cell):
        next_cell.passable = False
        self._body.insert(0, list(next_cell.position))
        self._previous_tail = self._body.pop()
        cell_map[self._previous_tail[0] // 20][self._previous_tail[1] // 20].passable = True
        self.score -= 1

    # 检查是否到达目标
    def check_eat(self, square_position):
        if self.get_head()[0] == square_position[0] and self.get_head()[1] == square_position[1]:
            # 得到目标，长度增加
            self.get_body().append(self.get_previous_tail())
            cell_map[self._previous_tail[0] // 20][self._previous_tail[1] // 20].passable = False
            self.score += 50
            return True
        return False

    # 重生
    def relive(self, body):
        for position in self._body:
            if position is not None:
                cell_map[position[0] // 20][position[1] // 20].passable = True
        if self.score > self.best_score:
            self.best_score = self.score
        self._body = body
        self._previous_tail = None
        self._direction = 'R'
        self.pre_distance = 0
        self.alive = True
        self.time = 1000
        self.score = 0
        for position in self._body:
            cell_map[position[0] // 20][position[1] // 20].passable = False

    # 根据方向，改变坐标
    def move_by_direction(self):
        if self._direction == 'L':
            next_cell = cell_map[self._body[0][0] // 20 - 1][self._body[0][1] // 20]
            self.move_to_next(next_cell)
        if self._direction == 'R':
            next_cell = cell_map[self._body[0][0] // 20 + 1][self._body[0][1] // 20]
            self.move_to_next(next_cell)
        if self._direction == 'U':
            next_cell = cell_map[self._body[0][0] // 20][self._body[0][1] // 20 - 1]
            self.move_to_next(next_cell)
        if self._direction == 'D':
            next_cell = cell_map[self._body[0][0] // 20][self._body[0][1] // 20 + 1]
            self.move_to_next(next_cell)

    # 根据Q值表移动
    def move(self, goal):
        # 判断蛇头方向
        if self._direction == 'U':
            self.state[0] = 0
            self.state[1] = 0
        elif self._direction == 'D':
            self.state[0] = 0
            self.state[1] = 1
        elif self._direction == 'L':
            self.state[0] = 0
            self.state[1] = 2
        elif self._direction == 'R':
            self.state[0] = 1
            self.state[1] = 0
        # 判断目标位置
        if self.get_head()[0] == goal[0] and self.get_head()[1] > goal[1]:
            self.state[2] = 0
            self.state[3] = 0
        if self.get_head()[0] == goal[0] and self.get_head()[1] < goal[1]:
            self.state[2] = 0
            self.state[3] = 1
        if self.get_head()[0] > goal[0] and self.get_head()[1] == goal[1]:
            self.state[2] = 0
            self.state[3] = 2
        if self.get_head()[0] < goal[0] and self.get_head()[1] == goal[1]:
            self.state[2] = 1
            self.state[3] = 0
        if self.get_head()[0] > goal[0] and self.get_head()[1] > goal[1]:
            self.state[2] = 1
            self.state[3] = 1
        if self.get_head()[0] > goal[0] and self.get_head()[1] < goal[1]:
            self.state[2] = 1
            self.state[3] = 2
        if self.get_head()[0] < goal[0] and self.get_head()[1] > goal[1]:
            self.state[2] = 2
            self.state[3] = 0
        if self.get_head()[0] < goal[0] and self.get_head()[1] < goal[1]:
            self.state[2] = 2
            self.state[3] = 1
        # 判断下一步
        if self.get_head()[1] - 20 <= 0:
            self.state[4] = 2
        else:
            if not cell_map[self._body[0][0] // 20][self._body[0][1] // 20 - 1].passable:
                self.state[4] = 1
            if self.get_head()[0] == goal[0] and self.get_head()[1] - 20 == goal[1]:
                self.state[2] = 2
                self.state[3] = 2
        if self.get_head()[1] + 20 >= HEIGHT:
            self.state[5] = 2
        else:
            if not cell_map[self._body[0][0] // 20][self._body[0][1] // 20 + 1].passable:
                self.state[5] = 1
            if self.get_head()[0] == goal[0] and self.get_head()[1] + 20 == goal[1]:
                self.state[2] = 2
                self.state[3] = 2
        if self.get_head()[0] - 20 <= 0:
            self.state[6] = 2
        else:
            if not cell_map[self._body[0][0] // 20 - 1][self._body[0][1] // 20].passable:
                self.state[6] = 1
            if self.get_head()[0] - 20 == goal[0] and self.get_head()[1] == goal[1]:
                self.state[2] = 2
                self.state[3] = 2
        if self.get_head()[0] + 20 >= WIDTH:
            self.state[7] = 2
        else:
            if not cell_map[self._body[0][0] // 20 + 1][self._body[0][1] // 20].passable:
                self.state[7] = 1
            if self.get_head()[0] + 20 == goal[0] and self.get_head()[1] == goal[1]:
                self.state[2] = 2
                self.state[3] = 2

        # 计算状态id
        state_id = 0
        for i in range(0, 8):
            state_id += self.state[7 - i] * pow(3, i)
        # 选择Q值最大的方向
        q_arr = QTable[int(state_id)]
        max_index = 0
        if q_arr[0] == q_arr[1] == q_arr[2] == q_arr[3]:
            max_index = random.randint(0, 3)
        else:
            for i in range(0, 4):
                if q_arr[i] > q_arr[max_index]:
                    max_index = i

        # 选择动作
        if max_index == 0 and self._direction != 'D':
            self._direction = 'U'
        if max_index == 1 and self._direction != 'U':
            self._direction = 'D'
        if max_index == 2 and self._direction != 'R':
            self._direction = 'L'
        if max_index == 3 and self._direction != 'L':
            self._direction = 'R'

        # 更新Q值表
        if self._direction == 'U':
            # 撞墙
            if self.get_head()[1] - 20 <= 0:
                QTable[int(state_id)][max_index] = gamma * QTable[int(state_id)][max_index] - 10
                self.alive = False
                return
            next_cell = cell_map[self._body[0][0] // 20][self._body[0][1] // 20 - 1]
            # 不可通过
            if not next_cell.passable:
                QTable[int(state_id)][max_index] = gamma * QTable[int(state_id)][max_index] - 10
                self.alive = False
                return
        if self._direction == 'D':
            if self.get_head()[1] + 20 >= HEIGHT:
                QTable[int(state_id)][max_index] = gamma * QTable[int(state_id)][max_index] - 10
                self.alive = False
                return
            next_cell = cell_map[self._body[0][0] // 20][self._body[0][1] // 20 + 1]
            if not next_cell.passable:
                QTable[int(state_id)][max_index] = gamma * QTable[int(state_id)][max_index] - 10
                self.alive = False
                return
        if self._direction == 'L':
            if self.get_head()[0] - 20 <= 0:
                QTable[int(state_id)][max_index] = gamma * QTable[int(state_id)][max_index] - 10
                self.alive = False
                return
            next_cell = cell_map[self._body[0][0] // 20 - 1][self._body[0][1] // 20]
            if not next_cell.passable:
                QTable[int(state_id)][max_index] = gamma * QTable[int(state_id)][max_index] - 10
                self.alive = False
                return
        if self._direction == 'R':
            if self.get_head()[0] + 20 >= WIDTH:
                QTable[int(state_id)][max_index] = gamma * QTable[int(state_id)][max_index] - 10
                self.alive = False
                return
            next_cell = cell_map[self._body[0][0] // 20 + 1][self._body[0][1] // 20]
            if not next_cell.passable:
                QTable[int(state_id)][max_index] = gamma * QTable[int(state_id)][max_index] - 10
                self.alive = False
                return
        self.move_to_next(next_cell)
        distance = sqrt(pow(self.get_head()[0] - goal[0], 2) + pow(self.get_head()[1] - goal[1], 2))
        # 距离变近
        if distance < self.pre_distance:
            QTable[int(state_id)][max_index] = gamma * QTable[int(state_id)][max_index] + 1
        else:
            QTable[int(state_id)][max_index] = gamma * QTable[int(state_id)][max_index] - 0.5
        # 到达目标
        if self.get_head()[0] == goal[0] and self.get_head()[1] == goal[1]:
            QTable[int(state_id)][max_index] = gamma * QTable[int(state_id)][max_index] + 100
            self.time += 100
        # 更新距离
        self.pre_distance = distance
        # 更新时间
        self.time -= 1
        if self.time <= 0:
            QTable[int(state_id)][max_index] = gamma * QTable[int(state_id)][max_index] - 10
            self.alive = False
