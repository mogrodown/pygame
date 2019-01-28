# -*- coding: utf-8 -*-
import codecs
import os

import database
import pygame
import tools
from pygame.locals import Rect
from config import FONT_WIDTH, FONT_HEIGHT, LINE_HEIGHT

GAMEINFO_INFOS = ['さくせい　TAKASHI', 'かいはつ　2018', 'ジャンル　RPG']
GAMEINFO_FORM = (Rect(16, 16, 248, 142), 12, len(GAMEINFO_INFOS))
gameinfo = None


def build_infomations(msg_engine):
    global gameinfo
    gameinfo = InfoWindow(GAMEINFO_FORM, GAMEINFO_INFOS, msg_engine=msg_engine)


class Window(object):
    EDGE_WIDTH = 4  # 白枠

    def __init__(self, rect):
        self.rect = rect
        self.inner_rect = self.rect.inflate(
            -self.EDGE_WIDTH * 2, -self.EDGE_WIDTH * 2)
        self._is_visible = False

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 0)
        pygame.draw.rect(screen, (0, 0, 0), self.inner_rect, 0)

    def show(self):
        self._is_visible = True

    def hide(self):
        self._is_visible = False

    def key_handler(self, event):
        pass

    def key_action(self):
        pass

    def update(self):
        pass

class QueryWindow(Window):
    def __init__(self, query_action, msg, x, y, msg_engine):
        Window.__init__(self, Rect(x, y, 400, 120))
        self.text_rect = self.inner_rect.inflate(-32, -32)
        self._msg_engine = msg_engine
        self._query_text = msg
        self.cursol_pos = 0
        self.cursor = tools.load_image("data", "cursor2.png", -1)
        self.query_action = query_action

    def draw(self, screen):
        Window.draw(self, screen)
        self._msg_engine.draw_string(screen, (self.text_rect[0], self.text_rect[1]), self._query_text)

        query = [database.menu_items[database.ACT_YES][0], database.menu_items[database.ACT_NO][0]]
        for index, data in enumerate(query):
            dx = self.text_rect[0] + FONT_WIDTH
            dy = self.text_rect[1] + (LINE_HEIGHT + FONT_HEIGHT) * (index + 1)
            self._msg_engine.draw_string(screen, (dx, dy), data)

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


class InfoWindow(Window):
    def __init__(self, form, texts, msg_engine):
        Window.__init__(self, form[0])
        self.msg_engine = msg_engine
        self.form = form
        self.text_rect = self.inner_rect.inflate(-32, -32)
        self.texts = texts

    def draw(self, screen):
        Window.draw(self, screen)
        for c in range(len(self.texts)):
            dx = self.text_rect[0] + FONT_WIDTH
            dy = self.text_rect[1] + (LINE_HEIGHT + FONT_HEIGHT) * (c % self.form[2])
            self.msg_engine.draw_string(screen, (dx, dy),
                                        self.texts[c])


class BattleCommandWindow(Window):
    LINE_HEIGHT = 8
    ATTACK, SPELL, ITEM, ESCAPE = range(4)
    COMMAND = [u'たたかう', u'じゅもん', u'どうぐ', u'にげる']

    def __init__(self, rect, msg_engine):
        Window.__init__(self, rect)
        self.text_rect = self.inner_rect.inflate(-32, -16)
        self.command = self.ATTACK
        self.msg_engine = msg_engine
        self.cursor = tools.load_image('data', 'cursor2.png', -1)
        self.frame = 0

    def draw(self, screen):
        Window.draw(self, screen)
        for i in range(0, 4):
            dx = self.text_rect[0] + MessageEngine.FONT_WIDTH
            dy = self.text_rect[1] + (self.LINE_HEIGHT + MessageEngine.FONT_HEIGHT) * (i % 4)  # noqa
            self.msg_engine.draw_string(screen, (dx, dy), self.COMMAND[i])

        dx = self.text_rect[0]
        dy = self.text_rect[1] + (self.LINE_HEIGHT + MessageEngine.FONT_HEIGHT) * (self.command % 4)  # noqa
        screen.blit(self.cursor, (dx, dy))

    def show(self):
        self.command = self.ATTACK


class BattleStatusWindow(Window):
    LINE_HEIGHT = 8

    def __init__(self, rect, status, msg_engine):
        Window.__init__(self, rect)
        self.text_rect = self.inner_rect.inflate(-32, -16)
        self.status = status  # status = ["なまえ", HP, MP, LV]
        self.msg_engine = msg_engine
        self.frame = 0

    def draw(self, screen):
        Window.draw(self, screen)
        if not self.is_visible:
            return
        # ステータスを描画
        status_str = [self.status[0], u"H%3d" % self.status[1], u"M%3d" % self.status[2],  # noqa
                      u"%s%3d" % (self.status[0][0], self.status[3])]  # noqa
        for i in range(0, 4):
            dx = self.text_rect[0]
            dy = self.text_rect[1] + (self.LINE_HEIGHT + MessageEngine.FONT_HEIGHT) * (i % 4)  # noqa
            self.msg_engine.draw_string(screen, (dx, dy), status_str[i])
