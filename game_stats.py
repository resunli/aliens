
class GameStats():
    # 游戏统计信息
    def __init__(self,ai_setting):
        # 初始化统计信息
        self.ai_setting = ai_setting
        self.ships_left = ai_setting.ship_limit
        self.game_active = False
        self.score = 0
        self.ship_hits = 0
        self.high_score =0
        self.level = 1

    def reset_stats(self):
        # 复位
        self.ships_left = self.ai_setting.ship_limit
        self.game_active = False
        self.score =0

        self.level = 1

        #飞船被外星人击中次数
        self.ship_hits = 0
