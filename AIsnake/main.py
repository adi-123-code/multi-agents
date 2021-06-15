# -*- coding:utf-8 -*-
import json
import threading

from mygame import *
# from snake import *
from qsnake import *
import random


# 绘制蛇
def show_snake(snake, game_surface):
    for position in snake.get_body():
        pygame.draw.rect(game_surface, BORDER_COLOUR, (position[0], position[1], 20, 20))
        pygame.draw.rect(game_surface, SNAKE_COLOUR, (position[0] + 1, position[1] + 1, 18, 18))
    pygame.draw.circle(game_surface, HEAD_COLOUR, (snake.get_head()[0] + 10, snake.get_head()[1] + 10), 9, 9)


class PySnake(Mygame):
    def __init__(self):
        super(PySnake, self).__init__("贪吃蛇", WIDTH, HEIGHT, BG_COLOUR, FPS)
        # 初始化蛇
        self.snakes = [QSnake([[100, i], [80, i]]) for i in range(0, 100, 20)]
        # 初始化目标方块的位置
        self.square_position = [40, 40]
        # 初始化一个数来判断目标方块是否存在
        self.square_flag = 1
        # 游戏模式
        self.mode = input('请选择学习模式（1：重新学习，2：继续学习）：')
        # 学习次数
        self.gen = 0
        if self.mode == '2':
            load_QTable()
            with open('gen.txt', 'r') as f:
                self.gen = json.load(f)
        self.add_draw_action(self.draw_snake)
        self.add_draw_action(self.draw_square)

    def loop(self):
        for i, snake in enumerate(self.snakes):
            if snake.get_alive():
                snake.move(self.square_position)
                if snake.check_eat(self.square_position):
                    self.square_flag = 0
                    self.draw_square()
                show_snake(snake, self.surface)
                # 显示分数
                score_font = pygame.font.SysFont("MicrosoftYaHei", 40)
                score_content = score_font.render('snake%d:' % (i + 1), True, (0, 0, 0))
                score_rect = score_content.get_rect()
                score_rect.topleft = (WIDTH, (i + 1) * 40 + 60)
                self.surface.blit(score_content, score_rect)
                score_content = score_font.render('%s' % snake.get_best_score(), True, (0, 0, 0))
                score_rect = score_content.get_rect()
                score_rect.topleft = (WIDTH + 120, (i + 1) * 40 + 60)
                self.surface.blit(score_content, score_rect)
                score_content = score_font.render('%s' % snake.get_score(), True, (0, 0, 0))
                score_rect = score_content.get_rect()
                score_rect.topleft = (WIDTH + 260, (i + 1) * 40 + 60)
                self.surface.blit(score_content, score_rect)

    def draw_snake(self):
        for i, snake in enumerate(self.snakes):
            if not snake.get_alive():
                self.gen += 1
                if self.mode == '2':
                    save_QTable()
                    with open('gen.txt', 'w') as f:
                        json.dump(self.gen, f)
                snake.relive([[100, i * 20], [80, i * 20]])

        # if flag == 0:
        #     self.game_over()
        # 绘制次数
        gen_font = pygame.font.SysFont("MicrosoftYaHei", 40)
        gen_content = gen_font.render('Gen:%d' % self.gen, True, (0, 0, 0))
        gen_rect = gen_content.get_rect()
        gen_rect.topleft = (WIDTH, HEIGHT - 40)
        self.surface.blit(gen_content, gen_rect)
        # 多线程运行贪吃蛇
        t = threading.Thread(target=self.loop)
        t.start()
        t.join()

    def draw_square(self):
        # 重新生成目标方块
        while self.square_flag == 0:
            # 随机生成x,y,扩大二十倍，在窗口范围内
            x = random.randrange(1, WIDTH // 20)
            y = random.randrange(1, HEIGHT // 20)
            if cell_map[int(x)][int(y)].passable:
                self.square_position = [int(x * 20), int(y * 20)]
                self.square_flag = 1

        pygame.draw.rect(self.surface, SQUARE_COLOUR, (self.square_position[0], self.square_position[1], 20, 20))


if __name__ == '__main__':
    PySnake().run()
