import pygame.font
from pygame.sprite import Group
from ship import Ship


class Scordboard():
    # 显示计分
    def __init__(self, ai_setting, screen, stats):
        # 初始化显示涉及的属性
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_setting = ai_setting
        self.stats = stats

        # 颜色 字体
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont("SimHei",38)

        # 显示得分和最高得分图片
        self.prep_score()
        self.prep_high_score()

        # 等级
        self.prep_level()

        # 飞船剩余

        self.prep_ships()

    def prep_score(self):
        round_score = int(round(self.stats.score,-1))
        score_str = "得分:" +"{:,}".format(round_score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.ai_setting.bg_color)

        # 显示在右上角
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    # 显示得分
    def show_score(self):

        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image,self.level_rect)

        # 绘制剩余飞船
        self.ships.draw(self.screen)

    # 显示最高分
    def prep_high_score(self):

        high_score = int(round(self.stats.high_score, -1))
        high_score_str = "最高分:"+"{:,}".format(high_score)

        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.ai_setting.bg_color)
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    # 显示等级
    def prep_level(self):
        # 图片及rect,位置
        self.level_image = self.font.render("等级:"+str(self.stats.level), True, self.text_color, self.ai_setting.bg_color)
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.screen_rect.right
        self.level_rect.top = self.score_rect.bottom+10

    # 显示剩余飞船
    def prep_ships(self):
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_setting, self.screen)
            ship.rect.x = 10+ ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

        """
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_setting, self.screen)
            ship.rect.x = 10+ ship_number * ship.rect.width
            ship.rect.y = 10
            ships.add(ship)
"""

