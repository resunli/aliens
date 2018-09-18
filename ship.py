import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    def __init__(self,ai_setting,screen):
        # 初始化初始位置
        super().__init__()
        self.screen = screen
        self.ai_setting = ai_setting

        # 加载飞船图像并获取其外接矩形
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # 将每艘新飞船放在屏幕的底部中央
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # 在飞船的属性center中存储小数值
        self.center = float(self.rect.centerx)
        self.y = float(self.rect.bottom)

        # 设置是否连续移动标志
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

        # 正在开炎
        self.firing = False

    def update(self):
        # 根据移动标志调整飞船的位置 右  左  上  下 移动
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_setting.ship_speed_factor
        elif self.moving_left and self.rect.left >0:
            self.center -= self.ai_setting.ship_speed_factor
        elif self.moving_up and self.rect.top >0:
            self.y -= self.ai_setting.ship_speed_factor
        elif self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.ai_setting.ship_speed_factor

        #
        self.rect.centerx = self.center
        self.rect.bottom = self.y

    def blitme(self):
        # 在指定位置绘制飞船
        self.screen.blit(self.image,self.rect)

    def ship_center(self):
        self.center = self.screen_rect.centerx
        self.y = self.screen_rect.height
