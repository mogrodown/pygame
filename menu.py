import database
import tools
from message import MessageEngine
from pygame.locals import Rect
from window import Window
from config import (
    FONT_WIDTH, FONT_HEIGHT)

TOPMENU, QUITMENU, STATUSMENU, SAVEMENU, ITEMMENU = range(5)

all_menus = {}

# (Rect, max_str_count, row_count)
TOPMENU_FORM = (Rect(16, 16, 152, 232), 6, 6)
TOPMENU_ACTS = [database.ACT_STATUS, database.ACT_EQUIPMENT, database.ACT_SPELL,
                database.ACT_ITEM, database.ACT_IS_SAVE, database.ACT_QUIT]

ITEMMENU_FORM = (Rect(64, 64, 216, 202), 10, 5)
ITEMMENU_ACTS = []

STATEINFO_FORM = (Rect(64, 64, 248, 172), 12, 4)
STATEINFO_ACTS = []

GAMEINFO_INFOS = ['さくせい　TAKASHI', 'かいはつ　2018', 'ジャンル　RPG']
GAMEINFO_FORM = (Rect(16, 16, 248, 142), 12, len(GAMEINFO_INFOS))
gameinfo = None

QUITMENU_FORM = (Rect(32, 280, 296, 142), 15, 3)
QUITMENU_ACTS = [u'ゲームをしゅうりょうしますか？']

current_menus = []

def build_menus(msg_engine):
    all_menus[TOPMENU] = MenuWindow(TOPMENU_FORM, TOPMENU_ACTS, msg_engine=msg_engine)
    all_menus[QUITMENU] = QueryWindow(
        QUITMENU_FORM, QUITMENU_ACTS, database.ACT_GAME_QUIT, msg_engine=msg_engine)

    """
    menus[STATUSMENU] = MenuWindow(
        actions=[database.ACT_STATUS, database.ACT_EQUIPMENT, database.ACT_SPELL,
                 database.ACT_ITEM, database.ACT_IS_SAVE, database.ACT_QUIT],
        x=16, y=16, str_count=6, column_count=6, row_count=1, msg_engine=msg_engine)
        """

def build_infomations(msg_engine):
    global gameinfo
    gameinfo = InfoWindow(GAMEINFO_FORM, GAMEINFO_INFOS, msg_engine=msg_engine)


def push_menus(menu):
    menu.show()
    current_menus.append(menu)


class InfoWindow(Window):
    LINE_HEIGHT = 8  # 行間の大きさ

    def __init__(self, form, texts, msg_engine):
        Window.__init__(self, form[0])
        self.msg_engine = msg_engine
        self.form = form
        self.text_rect = self.inner_rect.inflate(-32, -32)
        self.texts = texts

    def draw(self, screen):
        fw = FONT_WIDTH
        fh = FONT_HEIGHT

        # Window枠描画
        Window.draw(self, screen)

        # テキスト描画
        # for c in range(self.form[2]):
        for c in range(len(self.texts)):
            dx = self.text_rect[0] + fw
            dy = self.text_rect[1] + (self.LINE_HEIGHT + fh) * (c % self.form[2])
            self.msg_engine.draw_string(screen, (dx, dy),
                                        self.texts[c])

    #override
    def show(self):
        Window.show(self)
        self.cursol_pos = 0

    def key_handler(self, event):
        pass

    def key_action(self):
        pass

    def update(self):
        pass


class ParamWindow(InfoWindow):
    pass


class MenuWindow(InfoWindow):
    def __init__(self, form, actions, msg_engine):
        texts = []
        for action in actions:
            texts.append(database.menu_items[action][0])
        InfoWindow.__init__(self, form, texts, msg_engine)
        self.cursol_pos = 0
        self.cursor = tools.load_image("data", "cursor2.png", -1)
        self.actions = actions

    def draw(self, screen):
        InfoWindow.draw(self, screen)

        dx = self.text_rect[0] + self.form[1] * int(self.cursol_pos / self.form[2])
        dy = self.text_rect[1] + (self.LINE_HEIGHT + FONT_HEIGHT) * (self.cursol_pos % self.form[2])
        screen.blit(self.cursor, (dx, dy))

    def key_handler(self, event):
        if tools.is_key_upward(event):
            if self.cursol_pos == 0 or self.cursol_pos == self.form[2]:
                self.cursol_pos = self.form[2] - 1
            else:
                self.cursol_pos -= 1
        elif tools.is_key_downward(event):
            print('cursol pos = %d' % self.cursol_pos)
            if self.cursol_pos == self.form[2] - 1:
                self.cursol_pos = 0
            else:
                self.cursol_pos += 1

    def key_action(self):
        return self.actions[self.cursol_pos]


class QueryWindow(InfoWindow):
    def __init__(self, form, actions, query_action, msg_engine):
        texts = []
        texts.append(actions[0])
        texts.append('　' + database.menu_items[database.ACT_YES][0])
        texts.append('　' + database.menu_items[database.ACT_NO][0])
        InfoWindow.__init__(self, form, texts, msg_engine)

        self.cursol_pos = 0
        self.cursor = tools.load_image("data", "cursor2.png", -1)
        self.query_action = query_action

    def draw(self, screen):
        InfoWindow.draw(self, screen)

        dx = self.text_rect[0]
        dy = self.text_rect[1] + (self.LINE_HEIGHT + FONT_HEIGHT) * (self.cursol_pos + 1)
        screen.blit(self.cursor, (dx, dy))

    def key_handler(self, event):
        if tools.is_key_quit(event):
            return database.ACT_BACK

        if tools.is_key_upward(event):
            if self.cursol_pos == 0 or self.cursol_pos == 2:
                return
            self.cursol_pos -= 1
        elif tools.is_key_downward(event):
            if self.cursol_pos == 2 - 1:
                self.cursol_pos = 0
            else:
                self.cursol_pos += 1

    def key_action(self):
        if self.cursol_pos == 0:
            return self.query_action
        else:
            return database.ACT_NONE

"""
            MenuStack.SAVEMENU:
                window.MenuWindow(
                    actions=[database.ACT_ADVENTURE_BOOK1, database.ACT_ADVENTURE_BOOK2, database.ACT_BACK],
                    x=96, y=96, str_count=8, column_count=3, row_count=1, msg_engine=msg_engine)
        }
        self._menu_set[MenuStack.TOPMENU].show()
        self._menu_set[MenuStack.QUITMENU].show()
        self._menus = []
"""
