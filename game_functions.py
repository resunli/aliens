import sys
import pygame
import json
import csv

from bullet import Bullet
from alien import Alien
from time import sleep


# 每行外星人数量
def get_number_aliens_x(ai_setting, alien_width):
    # 计算每行外星人数量
    # 外星人间距为外星人宽度

    available_space_x = ai_setting.screen_width - alien_width
    number_aliens_x = int(available_space_x / (2*alien_width)) # 一行外星人数量
    return number_aliens_x


# 每列外星人数量
def get_number_aliens_y(ai_setting, alien_height, ship_height):
    # 计算每列的数量
    available_space_y = ai_setting.screen_height - 3*alien_height - ship_height
    number_aliens_y = int(available_space_y / (2*alien_height))
    return number_aliens_y


def create_alien(ai_setting,screen, aliens, alien_number, row_number):
    # 创建单个外星人
    alien = Alien(ai_setting, screen)
    alien_width = alien.rect.width
    alien_heght = alien.rect.height
    alien.x = alien_width + 2 * alien_number * alien_width
    alien.y = alien_heght + 2 * alien_heght * row_number

    alien.rect.x = alien.x
    alien.rect.y = alien.y
    aliens.add(alien)


def create_fleet(ai_setting, screen, ship, aliens):
    # 创建外星人组
    # 创建一个外星人，并计算一行可以容纳多少外星人
    alien = Alien(ai_setting,screen)
    number_aliens_x = get_number_aliens_x(ai_setting,alien.rect.width)
    number_rows = get_number_aliens_y(ai_setting,alien.rect.height, ship.rect.height)

    # 创建第一行外星人
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_setting, screen,aliens, alien_number, row_number)  # 全部出来
            # create_alien(ai_setting, screen,aliens, alien_number, row_number-number_rows) # 一行一行出来


# 按下按键
def check_keydown_events(event, ai_setting, screen, ship, bullets):
    # 检查按键 右移 左移
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_UP:
        ship.moving_up = True
    elif event.key== pygame.K_DOWN:
        ship.moving_down = True
    elif event.key == pygame.K_SPACE:
        ship.firing = True
        fire_bullet(ai_setting,screen,ship,bullets)
    elif event.key == pygame.K_LCTRL:
        ai_setting.bullet_width = 100
    elif event.key == pygame.K_q:
        sys.exit()


# 松开按键
def check_keyup_events(event, ai_setting, screen, ship, bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    elif event.key == pygame.K_UP:
        ship.moving_up = False
    elif event.key == pygame.K_DOWN:
        ship.moving_down = False
    elif event.key == pygame.K_SPACE:
        ship.firing = False


# 响应鼠标和按键
def check_events(ai_setting, screen, sb, stats, play_button, ship, aliens, bullets):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_settings(ai_setting)
            sys.exit()

        # 按键检查
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_setting, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)
        #
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event,ai_setting, screen, ship,bullets)
        # 左移
        elif event.type == pygame.KEYUP:
            check_keyup_events(event,ai_setting, screen, ship,bullets)


def update_screen(ai_setting, screen,stats, sb, ship, aliens, bullets, play_button):
    # 更新屏幕上的图像 并切换到新屏幕
    # 每次循环时都重新绘制屏幕

    screen.fill(ai_setting.bg_color)

    # 在飞船和外星人后面重绘所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    ship.blitme()
    aliens.draw(screen)

    # 显示得分
    sb.show_score()

    # 显示按钮
    if not stats.game_active:
        play_button.draw_button()


    # 让最近绘制的屏幕可见
    pygame.display.flip()


# 更新子弹位置
def update_bullets(ai_setting, screen, stats, sb, ship, aliens,bullets):
    # 更新子弹位置，删除已经消失的子弹
    # 删除消失的子弹

    bullets.update()

    for bullet in bullets.copy():
        if bullet.rect.top <= 0:
            bullets.remove(bullet)
        # print(len(bullets))

    check_bullet_alien_collisions(ai_setting, screen, stats, sb, ship, aliens, bullets)


# 发射子弹
def fire_bullet(ai_setting, screen, ship, bullets):
    if len(bullets) < ai_setting.bullet_allowed:
        new_bullet = Bullet(ai_setting, screen, ship)
        bullets.add(new_bullet)


# 飞船撞击外星人
def ship_hit(ai_setting, stats, screen, sb, ship, aliens, bullets):
    if stats.ships_left > 0:
        # 撞击时减少数量
        stats.ships_left -= 1

        # 更新显示
        sb.prep_ships()

        # 清空外星人，重新开始
        aliens.empty()
        bullets.empty()

        #创建新的外星人和飞船
        create_fleet(ai_setting, screen, ship, aliens)
        ship.ship_center()

        # 停顿一下
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def update_aliens(ai_setting,stats, screen, sb, ship, aliens, bullets):

    check_fleet_edges(ai_setting,aliens)
    # 更新外星人所有位置
    aliens.update()

    # 检查外星人飞船碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_setting, stats, screen, sb, ship, aliens, bullets)

    check_aliens_bottom(ai_setting, stats, screen, sb, ship, aliens, bullets)


# 有外星人到达边缘时处理
def check_fleet_edges(ai_setting, aliens):
    for alien in aliens:
        if alien.check_edges():
            change_fleet_direction(ai_setting,aliens)
            break


# 改变方向
def change_fleet_direction(ai_setting,aliens):
    for alien in aliens:
        alien.y += ai_setting.alien_fleet_drop_speed
    # 改变方向
    ai_setting.alien_fleet_direction *= -1


# 检查外星人和子弹碰撞及新建外星人
def check_bullet_alien_collisions(ai_setting, screen, stats, sb, ship, aliens, bullets):
    # 检查是否有子弹碰到外星人
    collisions = pygame.sprite.groupcollide(bullets,aliens,True,True)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_setting.alien_points*(len(aliens))
            sb.prep_score()

        check_high_score(stats,sb)

    # 检查外星人是否全部消灭
    if len(aliens) == 0:
        bullets.empty()
        ai_setting.increase_speed()  # 加速
        create_fleet(ai_setting,screen,ship,aliens)

        stats.level += 1
        sb.prep_level()


# 检查是否有外星人到达屏幕底端
def check_aliens_bottom(ai_setting, stats, screen, sb, ship, aliens, bullets):
    screen_rect = screen.get_rect()
    for alien in aliens:
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_setting, stats, screen, sb, ship, aliens, bullets)
            break


# 开始按钮处理
def check_play_button(ai_setting, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    # 开始事件
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # 重置速度
        ai_setting.initialize_dynamic_settings()

        # 隐藏光标
        pygame.mouse.set_visible(False)

        # 重置统计信息
        stats.reset_stats()

        # 游戏状态
        stats.game_active = True

        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()

        # 重置计分
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        # 创建新的外星人，并让飞船居中
        create_fleet(ai_setting, screen, ship, aliens)
        ship.ship_center()


def check_high_score(stats, sb):
    if stats.score>stats.high_score:
        stats.high_score = stats.score

        sb.prep_high_score()


def save_settings(ai_setting):
    filename = "settings.txt"
    # save_data_file(filename,ai_setting)

    dict = json.dumps(ai_setting, default=lambda obj: obj.__dict__, sort_keys=True, indent = 4)
    with open(filename, 'w') as f_obj:
        json.dump(dict, f_obj)





"""
# 保存文件
def save_data_file(filename = "", datalist = []):
    with open(filename, "w") as csvfile:
        datawriter = csv.writer(csvfile, delimiter='\n',quotechar=" ",quoting=csv.QUOTE_NONNUMERIC)
        datawriter.writerow(datalist)
        csvfile.close()
        print("Data saved!")


def readdata(filename=""):
    with open(filename, "r") as csvfile:
        DataReader = csv.reader(csvfile, delimiter='\n',quotechar=" ",quoting=csv.QUOTE_NONNUMERIC)
        Output = []
        for Item in DataReader:
            Output.append(Item[0])
        csvfile.close()
        print("Data read!")
        return Output
"""