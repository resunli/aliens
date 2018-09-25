
class Settings():
    # 存储所有设置的类
    def __init__(self):
        # 初始化游戏的设置
        # 屏幕设置
        self.screen_width = 1200
        self.screen_height = 600
        self.bg_color = (230, 230, 230)

        # 飞船移动速度设置
        self.ship_speed_factor = 1.5

        # 飞船数量
        self.ship_limit = 3

        # 外星人移动速度设置
        self.alien_speed_factor = 2
        self.alien_fleet_drop_speed = 10

        # 移动方向 1 右，-1 左
        self.alien_fleet_direction = 1

        # 子弹设置
        self.bullet_speed_factor = 1
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 255,60,60
        self.bullet_allowed = 10

        # 外星人子弹
        self.alien_bullet_speed_factor =1
        self.alien_bullet_width = 2
        self.alien_bullet_height = 8
        self.alien_bullet_color =60,60,60
        self.alien_bullet_allowed = 9

        # 加速
        self.speedup_scale = 1.1

        # 加分速度
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        # 初始化随游戏进行而变化的设置
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor= 3
        self.alien_speed_factor = 1

        # 移动方向 1 右，-1 左
        self.alien_fleet_direction = 1

        # 得分
        self.alien_points = 50

    def increase_speed(self):
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points*self.score_scale)