import sounds
import tools
import sounds
from rpg_keyword import ACT_GAME_START, ACT_GAME_QUIT, ACT_NONE


class Title(object):
    """タイトル画面"""
    START, CONTINUE, EXIT = 0, 1, 2

    def __init__(self, msg_engine):
        self.msg_engine = msg_engine
        self.title_img = tools.load_image("data", "python_quest.png", -1)
        self.cursor_img = tools.load_image("data", "cursor2.png", -1)
        self.menu = self.START
        self._visible = False

    def show(self):
        print('show')
        if not self._visible:
            sounds.play_bgm("title.mp3")
        self._visible = True

    def hide(self):
        print('hide')
        self._visible = False

    def update(self):
        pass

    def key_action(self, player):
        if not self._visible:
            return None
        if self.menu == Title.START:
            return ACT_GAME_START, None
        elif self.menu == Title.EXIT:
            return ACT_GAME_QUIT

    def key_handler(self, event):
        if not self._visible:
            return ACT_NONE
        if tools.is_key_upward(event):
            self.menu -= 1
            if self.menu < 0:
                self.menu = 0
        elif tools.is_key_downward(event):
            self.menu += 1
            if self.menu > 2:
                self.menu = 2
        return ACT_NONE

    def draw(self, screen, offset):
        if not self._visible:
            return None
        screen.fill((0, 0, 128))
        # タイトルの描画
        screen.blit(self.title_img, (20, 60))
        # メニューの描画
        self.msg_engine.draw_string(screen, (260, 240), u"ＳＴＡＲＴ")
        self.msg_engine.draw_string(screen, (260, 280), u"ＣＯＮＴＩＮＵＥ")
        self.msg_engine.draw_string(screen, (260, 320), u"ＥＸＩＴ")
        # クレジットの描画
        self.msg_engine.draw_string(screen, (130, 400), u"２００８　ＰＹＴＨＯＮでゲームつくりますがなにか？")  # noqa
        # メニューカーソルの描画
        if self.menu == self.START:
            screen.blit(self.cursor_img, (240, 240))
        elif self.menu == self.CONTINUE:
            screen.blit(self.cursor_img, (240, 280))
        elif self.menu == self.EXIT:
            screen.blit(self.cursor_img, (240, 320))
