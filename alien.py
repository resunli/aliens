import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    def __init__(self, ai_setting, screen):
        # 初始化外星人并设置其起始位置
        super().__init__()
        # super(Alien,self).__init__()
        self.screen = screen
        self.ai_setting = ai_setting

        # 加载外星人图像，并设置其rect属性
        self.image = pygame.image.load("images/alien.bmp")
        self.rect = self.image.get_rect()

        # 出现在屏幕左上角  距离左边距离是外星人图片的宽度，距离上边距离为图片的高度，不是0,0位置
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # 存储外星人的准确位置
        self.x = float(self.rect.x)

    def blitme(self):
        # 在指定位置绘制外星人
        self.screen.blit(self.image,self.rect)

    def update(self):
        # 向右移动外星人
        self.x += (self.ai_setting.alien_speed_factor * self.ai_setting.alien_fleet_direction)
        self.rect.x = self.x
        self.rect.y = self.y

    def check_edges(self):
        # 检查是否到边缘
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <=0:
            return True

