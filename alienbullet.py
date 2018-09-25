import pygame
from pygame.sprite import Sprite


class AlienBullet(Sprite):
    # 一个对飞船发射的子弹进行管理的类

    def __init__(self, ai_setting, screen, alien):
        # 在飞船所处的位置创建一个子弹对象
        # super(Bullet, self).__init__()  #py2.7写法
        super().__init__()
        self.screen = screen

        # 在(0,0)处创建一个表示子弹的矩形 再设置正确的位置
        self.rect = pygame.Rect(0, 0, ai_setting.alien_bullet_width,ai_setting.alien_bullet_height)
        self.rect.centerx = alien.rect.centerx
        self.rect.top = alien.rect.top

        # 存储子弹的位置，小数
        self.y = float(self.rect.y)

        self.color = ai_setting.alien_bullet_color
        self.speed_factor = ai_setting.alien_bullet_speed_factor

    def update(self):
        # 向上移动子弹
        self.y += self.speed_factor
        # 更新表示子弹的rect的位置
        self.rect.y = self.y

    def draw_bullet(self):
        # 在屏幕上绘制子弹
        pygame.draw.rect(self.screen, self.color, self.rect)
