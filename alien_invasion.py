
import pygame

from pygame.sprite import Group

import game_functions as gf

from button import Button
from scoreboard import Scordboard

from settings import Settings
from ship import Ship
from game_stats import GameStats
from time import sleep


def run_game():
  
    # 初始化游戏并创建一个屏幕对象
    pygame.init()

    # 声音初始化
    pygame.mixer.init()

    ai_settings = Settings()

    screen = pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))

    pygame.display.set_caption("外星人入侵")

    # 创建按钮
    play_button = Button(ai_settings,screen,"开始")

    # 统计信息
    stats = GameStats(ai_settings)

    stats.high_score = gf.read_setting()

    # 显示得分
    sb = Scordboard(ai_settings, screen, stats)

    # 创建一个飞船
    ship = Ship(ai_settings, screen)

    # 创建存储子弹的编组
    bullets = Group()

    # 创建外星人组
    aliens = Group()

    # 创建外星人群
    gf.create_fleet(ai_settings,screen,ship, aliens)

    # 游戏主循环
    while True:
        sleep(0.001)
        # 监视键盘和鼠标
        gf.check_events(ai_settings, screen, sb, stats, play_button, ship, aliens, bullets)

        if stats.game_active:

            # 检查是否要移动
            ship.update()

            # 更新显示子弹
            # bullets.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)

            # 更新外星人位置
            gf.update_aliens(ai_settings, stats, screen, sb, ship, aliens,bullets)

        # 设置背景颜色 # 让最近绘制的屏幕可见
        gf.update_screen(ai_settings,screen, stats, sb, ship, aliens, bullets, play_button)


# 运行游戏
run_game()