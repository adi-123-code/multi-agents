# -*- coding:utf-8 -*-
import sys
import time

import pygame
from pygame.locals import *


class Mygame(object):
    def __init__(self, title, width, height, background, fps):
        # 初始化pygame，为使用硬件做准备
        pygame.init()
        self.clock = pygame.time.Clock()
        self.fps = fps
        # 创建一个窗口
        self.width = width
        self.height = height
        self.surface = pygame.display.set_mode((width + 400, height))
        self.background = background
        # 设置窗口的标题
        pygame.display.set_caption(title)
        # 列表，画图有固定顺序
        self.display_update_actions = [self.draw_background]

    def draw_background(self):
        self.surface.fill(self.background)
        for _ in range(20, self.width, 20):
            pygame.draw.line(self.surface, (0, 0, 0), (_, 0), (_, self.height))
        for _ in range(20, self.height, 20):
            pygame.draw.line(self.surface, (0, 0, 0), (0, _), (self.width, _))
        pygame.draw.rect(self.surface, (255, 255, 255), (self.width, 0, 400, self.width))
        score_font = pygame.font.SysFont("MicrosoftYaHei", 60)
        score_content = score_font.render('Score', True, (0, 0, 0))
        score_rect = score_content.get_rect()
        score_rect.centerx = self.width + 200
        self.surface.blit(score_content, score_rect)
        score_font = pygame.font.SysFont("MicrosoftYaHei", 40)
        score_content = score_font.render('Best', True, (0, 0, 0))
        score_rect = score_content.get_rect()
        score_rect.topleft = (self.width+120,60)
        self.surface.blit(score_content, score_rect)
        score_font = pygame.font.SysFont("MicrosoftYaHei", 40)
        score_content = score_font.render('Current', True, (0, 0, 0))
        score_rect = score_content.get_rect()
        score_rect.topleft = (self.width + 260, 60)
        self.surface.blit(score_content, score_rect)

    def update_display(self):
        for action in self.display_update_actions:
            action()
            # 更新整个待显示的Surface对象到屏幕上
        pygame.display.flip()

    def add_draw_action(self, action):
        self.display_update_actions.append(action)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    # 接收到退出事件后，退出程序
                    pygame.quit()
                    sys.exit()
            self.update_display()
            self.clock.tick(self.fps)

    def game_over(self):
        # 设置提示字体的格式
        game_over_font = pygame.font.SysFont("MicrosoftYaHei", 50)
        # 设置提示字体的颜色
        game_over_colour = game_over_font.render('GameOver', True, (150, 150, 150))  # 只能英文
        # 设置提示位置
        game_over_location = game_over_colour.get_rect()
        game_over_location.center = (self.width / 2, self.height / 2)
        # 绑定以上设置到句柄
        self.surface.blit(game_over_colour, game_over_location)
        # 提示运行信息
        pygame.display.flip()
        # 休眠5秒
        time.sleep(2)
        pygame.quit()
        sys.exit()
